#!/usr/bin/env python3
"""
reCAPTCHA v3 Token Harvester
Author: [Muhammad Sameer]
Description: Tool for harvesting reCAPTCHA v3 tokens using Selenium.
             Intended for authorized security testing only.
"""

import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_URL = "https://example.com/register"
DEFAULT_SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"  # Google test key

class RecaptchaTokenHarvester:
    def __init__(self, url, site_key, headless=False):
        self.url = url
        self.site_key = site_key
        self.headless = headless
        self.driver = self._setup_driver()

    def _setup_driver(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)

        if self.headless:
            options.add_argument('--headless')

        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def get_token(self):
        """Load the page and execute reCAPTCHA v3 to retrieve a token."""
        try:
            print(f"[*] Loading {self.url} ...")
            self.driver.get(self.url)
            time.sleep(3)

            # Wait until grecaptcha is defined
            WebDriverWait(self.driver, 10).until(
                lambda d: d.execute_script("return typeof grecaptcha !== 'undefined'")
            )

            print("[*] Executing reCAPTCHA...")
            token = self.driver.execute_script("""
                return new Promise((resolve) => {
                    if (typeof grecaptcha !== 'undefined') {
                        grecaptcha.ready(function() {
                            grecaptcha.execute(arguments[0], {action: 'submit'})
                                .then(function(token) { resolve(token); })
                                .catch(function(error) {
                                    console.error('reCAPTCHA error:', error);
                                    resolve(null);
                                });
                        });
                    } else {
                        resolve(null);
                    }
                });
            """, self.site_key)

            if token and len(token) > 100:
                print(f"[+] Token obtained (length: {len(token)})")
                return token
            else:
                print("[-] Invalid token received")
                return None

        except Exception as e:
            print(f"[-] Error: {e}")
            return None

    def harvest_multiple(self, count=5, delay=3):
        """Harvest `count` tokens, reloading the page each time."""
        tokens = []
        for i in range(count):
            print(f"\n{'='*50}\nToken {i+1}/{count}\n{'='*50}")
            token = self.get_token()
            if token:
                tokens.append(token)
                fname = f"token_{int(time.time())}.txt"
                with open(fname, "w") as f:
                    f.write(token)
                print(f"[*] Saved to {fname}")
            else:
                print(f"[-] Failed to obtain token {i+1}")
            if i < count - 1:
                time.sleep(delay)
        return tokens

    def close(self):
        if self.driver:
            self.driver.quit()

def main():
    parser = argparse.ArgumentParser(description="reCAPTCHA v3 Token Harvester")
    parser.add_argument("--url", default=DEFAULT_URL, help="Target URL containing reCAPTCHA v3")
    parser.add_argument("--site-key", default=DEFAULT_SITE_KEY, help="reCAPTCHA v3 site key")
    parser.add_argument("--count", type=int, default=1, help="Number of tokens to harvest")
    parser.add_argument("--delay", type=int, default=3, help="Delay between harvests (seconds)")
    parser.add_argument("--headless", action="store_true", help="Run Chrome in headless mode")
    parser.add_argument("--output", default="tokens.txt", help="File to save all tokens")
    args = parser.parse_args()

    harvester = RecaptchaTokenHarvester(args.url, args.site_key, args.headless)

    try:
        if args.count == 1:
            token = harvester.get_token()
            if token:
                print(f"\n[+] Token:\n{token}")
                with open(args.output, "w") as f:
                    f.write(token)
                print(f"[*] Saved to {args.output}")
        else:
            tokens = harvester.harvest_multiple(args.count, args.delay)
            print(f"\n[*] Harvested {len(tokens)} tokens")
            with open(args.output, "w") as f:
                for i, t in enumerate(tokens, 1):
                    f.write(f"--- Token {i} ---\n{t}\n\n")
            print(f"[*] All tokens saved to {args.output}")
    finally:
        harvester.close()

if __name__ == "__main__":
    main()
