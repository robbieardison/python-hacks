import requests
import html2text

url = "https://realpython.com/python-send-email/"  

# Send an HTTP GET request to the URL and get the page content
response = requests.get(url)
html_content = response.text

# Convert the HTML content to Markdown using html2text
markdown_content = html2text.html2text(html_content)

# Save the Markdown content to a file or print it
with open('output.md', 'w', encoding='utf-8') as file:
    file.write(markdown_content)

print("Webpage scraped and converted to Markdown!")

# Close the HTTP response
response.close()
