import datetime
import pandas as pd
from httpx import Client
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.exceptions import UnexpectedModelBehavior
from load_models import OLLAMA_MODEL
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

class Product(BaseModel):
    brand_name: str = Field(title='Brand Name', description='The brand name of the product')
    product_name: str = Field(title='Product Name', description='The name of the product')
    price: str | None = Field(title='Price', description='The price of the product')
    rating_count: int | None = Field(title='Rating Count', description='The number of ratings the product has received')

class Results(BaseModel):
    dataset: list[Product] = Field(title='Dataset', description='The list of products')

web_scraping_agent = Agent(
    name='Web Scraping Agent',
    model=OLLAMA_MODEL,
    system_prompt=("""
        Your task is to convert a data string into a List of dictionaries.
                   
        Step 1. Fetch the HTML text from the given URL using the fetch_html_text() function.
        Step 2. Takes the output from Step 1 and clean it up for the final output.
    """),
    retries=2,
    result_type=Results,
    model_settings=ModelSettings(
        max_tokens=8020,
        temperature=0.1,
    )
)

@web_scraping_agent.tool_plain(retries=1)
def fetch_html_text(url: str) -> str:
    """
    Fetches the HTML text from the given URL

    args:
        url (str): The URL to fetch the HTML text from

    returns:
        str: The HTML text from the given URL
    """
    print('Calling URL:', url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    with Client(headers=headers) as client:
        response = client.get(url, timeout=20)
        if response.status_code != 200:
            raise UnexpectedModelBehavior(f'Failed to fetch the HTML text from the URL: {url}. Status code: {response.status_code}')
        soup = BeautifulSoup(response.text, 'html.parser')
        with open('soup.txt', 'w', encoding='utf-8') as file:
            file.write(soup.get_text())
        print('Soup file saved')
        return soup.get_text().replace('\n', ' ').replace('\r', ' ')

@web_scraping_agent.result_validator
def validate_result(result: Results) -> Results:
    print('Validating results...')
    if isinstance(result, Results):
        print('Validation passed')
        return result
    print('Validation failed')
    return None

def main() -> None:
    prompt = 'https://www.aliexpress.com/w/wholesale-top-selling-tools.html'
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            response = web_scraping_agent.run_sync(prompt)
            if response.data is None:
                # raise UnexpectedModelBehavior('No data returned from the model')
                return None
            print('-' * 50)
            print('Input_tokens:', response.usage().request_tokens)
            print('Output_tokens:', response.usage().response_tokens)
            print('Total_tokens:', response.usage().total_tokens)

            lst = []
            for item in response.data.dataset:
                lst.append(item.model_dump())

            timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            df = pd.DataFrame(lst)
            df.to_csv(f'product_listings_{timestamp}.csv', index=False)
            print(f'CSV file saved as product_listings_{timestamp}.csv')
            break  # Exit the retry loop if successful

        except ConnectionError as e:
            print(f'Connection error occurred: {e}')
            if attempt < max_retries - 1:
                print(f'Retrying in {retry_delay} seconds...')
                time.sleep(retry_delay)
            else:
                print('Max retries reached. Exiting.')
                break

        except UnexpectedModelBehavior as e:
            print(e)
            break

if __name__ == '__main__':
    main()