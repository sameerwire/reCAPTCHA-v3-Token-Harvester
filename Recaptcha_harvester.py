#!/usr/bin/env python3
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RecaptchaTokenHarvester:
    def __init__(self):
        self.driver = None
        self.setup_driver()

    def setup_driver(self):
        """Setup Chrome driver with proper options"""
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/144.0.0.0 Safari/537.36'
        )
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        # options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

    def get_token(self):
        """Get a fresh token by reloading the page"""
        try:
            print(f"\n[*] Loading page at {time.strftime('%H:%M:%S')}...")
            self.driver.get("https://example.com/register")  # DUMMY TARGET

            time.sleep(3)

            wait = WebDriverWait(self.driver, 10)
            wait.until(lambda d: d.execute_script("return typeof grecaptcha !== 'undefined'"))

            print("[*] Executing reCAPTCHA...")

            token = self.driver.execute_script("""
                return new Promise((resolve) => {
                    if (typeof grecaptcha !== 'undefined') {
                        grecaptcha.ready(function() {
                            grecaptcha.execute('SITE_KEY_PLACEHOLDER', {action: 'submit'})
                                .then(function(token) {
                                    resolve(token);
                                })
                                .catch(function(error) {
                                    console.error('reCAPTCHA error:', error);
                                    resolve(null);
                                });
                        });
                    } else {
                        resolve(null);
                    }
                });
            """)

            if token and len(token) > 100:
                print(f"[+] Token obtained! Length: {len(token)} chars")
                return token
            else:
                print("[-] Invalid token received")
                return None

        except Exception as e:
            print(f"[-] Error: {e}")
            return None

    def get_multiple_tokens(self, count=5):
        tokens = []

        for i in range(count):
            print(f"\n{'=' * 60}")
            print(f"Getting token {i + 1}/{count}")
            print(f"{'=' * 60}")

            token = self.get_token()
            if token:
                tokens.append(token)

                filename = f"token_{int(time.time())}.txt"
                with open(filename, "w") as f:
                    f.write(token)

                print(f"[*] Token saved to {filename}")
            else:
                print(f"[-] Failed to get token {i + 1}")

            if i < count - 1:
                time.sleep(3)

        return tokens

    def cleanup(self):
        if self.driver:
            self.driver.quit()


def main():
    print("=" * 60)
    print("reCAPTCHA Token Harvester - Demo Version")
    print("=" * 60)

    harvester = RecaptchaTokenHarvester()

    try:
        while True:
            print("\n------------------------------")
            print("1. Get one token")
            print("2. Get 5 tokens")
            print("3. Continuous mode")
            print("4. Exit")

            choice = input("\nChoice: ").strip()

            if choice == "1":
                token = harvester.get_token()
                if token:
                    print(f"\nTOKEN:\n{token}\n")

            elif choice == "2":
                tokens = harvester.get_multiple_tokens(5)
                print(f"\n[*] Got {len(tokens)} tokens")

            elif choice == "3":
                print("\n[*] Continuous mode (Ctrl+C to stop)")
                try:
                    i = 0
                    while True:
                        i += 1
                        token = harvester.get_token()
                        if token:
                            print(f"[Token {i}] {token[:80]}...")
                        time.sleep(10)
                except KeyboardInterrupt:
                    print("\n[*] Stopped")

            elif choice == "4":
                break

            else:
                print("[-] Invalid choice")

    finally:
        harvester.cleanup()
        print("\n[*] Done")


if __name__ == "__main__":
    main()
