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
