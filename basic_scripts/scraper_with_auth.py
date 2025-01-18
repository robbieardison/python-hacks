import requests
import html2text

# Define your login credentials
username = 'your_username'
password = 'your_password'

# Define the Jira login URL and target issue URL
login_url = 'https://your-jira-instance.com/login.jsp'
issue_url = 'https://your-jira-instance.com/browse/PROJECT-123'

# Create a session to maintain authentication
session = requests.Session()

# Perform login
login_payload = {
    'username': username,
    'password': password
}

login_response = session.post(login_url, data=login_payload)

# Check if the login was successful (you should inspect the response for specific indicators)
if 'Login failed' in login_response.text:
    print('Login failed.')
else:
    print('Login successful.')

    # Now, you can make further requests using the authenticated session
    issue_response = session.get(issue_url)

    if issue_response.status_code == 200:
        # Convert the HTML content to Markdown using html2text
        markdown_content = html2text.html2text(issue_response.text)

        # Save the Markdown content to a file or print it
        with open('output2.md', 'w', encoding='utf-8') as file:
            file.write(markdown_content)

        print("Issue page scraped and converted to Markdown!")

    else:
        print(f"Failed to retrieve issue page. Status Code: {issue_response.status_code}")

# Close the HTTP session
session.close()
