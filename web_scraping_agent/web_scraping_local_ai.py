import os
import datetime
import time
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
from gpt4all import GPT4All  

# Define the Product model for structured data representation
class Product:
    def __init__(self, brand_name, product_name, price=None, rating_count=None):
        self.brand_name = brand_name
        self.product_name = product_name
        self.price = price
        self.rating_count = rating_count

    def to_dict(self):
        return {
            "Brand Name": self.brand_name,
            "Product Name": self.product_name,
            "Price": self.price,
            "Rating Count": self.rating_count,
        }


def fetch_html_text(url):
    """
    Fetches the HTML content from the given URL.

    Args:
        url (str): The URL to fetch the HTML from.

    Returns:
        str: The HTML text, or None if there was an error.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching the HTML from {url}: {e}")
        return None


def ai_process_html(html):
    """
    Uses a local AI model to process and parse the HTML content into structured data.

    Args:
        html (str): The raw HTML content.

    Returns:
        list[Product]: A list of Product objects extracted by the AI.
    """
    # Initialize the GPT4All model (or another local AI model)
    model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")  # Replace with the path to your model file
    
    prompt = f"""
    You are a helpful assistant that extracts product data from HTML content.
    The HTML structure contains product containers with the following details:
    - Brand name
    - Product name
    - Price
    - Rating count

    Please parse the following HTML and return a list of dictionaries with this structure:
    [
        {{"brand_name": "Brand A", "product_name": "Product A", "price": "$10", "rating_count": 100}},
        ...
    ]
    
    HTML content:
    {html}
    """
    
    response = model.generate(prompt)
    print("AI Response:", response)

    # Convert the AI response into Product objects
    try:
        import json
        data = json.loads(response)
        products = [
            Product(
                brand_name=item["brand_name"],
                product_name=item["product_name"],
                price=item.get("price"),
                rating_count=item.get("rating_count")
            )
            for item in data
        ]
        return products
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        return []


def save_to_csv(products, filename_prefix="product_listings"):
    """
    Saves the list of Product objects to a CSV file.

    Args:
        products (list[Product]): The list of Product objects to save.
        filename_prefix (str): The prefix for the filename.
    """
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{filename_prefix}_{timestamp}.csv"
    data = [product.to_dict() for product in products]
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


def main():
    url = "https://www.aliexpress.com/w/wholesale-top-selling-tools.html"
    max_retries = 3
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        html = fetch_html_text(url)
        if html:
            products = ai_process_html(html)
            if products:
                save_to_csv(products)
                break  # Exit retry loop if successful
            else:
                print("No products found in the AI response.")
        else:
            print(f"Attempt {attempt + 1}/{max_retries} failed. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
    else:
        print("Failed to fetch and parse data after multiple attempts.")


if __name__ == "__main__":
    main()
