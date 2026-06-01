# reCAPTCHA v3 Assisted SQLi Validation Framework

A research-driven automation workflow for testing and validating potential SQL injection behavior in web applications protected by **reCAPTCHA v3**.

This project demonstrates how controlled browser automation can be used to handle dynamic client-side validation tokens during authorized security testing.

> ⚠️ **Disclaimer:**
> This project was developed strictly for **authorized VAPT / security research environments only**.
> It is intended for educational and defensive security analysis purposes. Do not use against systems without explicit permission.

---

## 📌 Overview

Modern web applications often combine:

* Input validation + backend database queries
* Bot protection mechanisms (reCAPTCHA v3)
* Session-based request validation

While these controls improve security, they can also make **automated vulnerability validation challenging** during legitimate security assessments.

This project explores a controlled approach to:

* Handling dynamic reCAPTCHA v3 token generation
* Maintaining valid session state during testing
* Enabling structured automation workflows for security validation tools

---

## 🧠 Problem Statement

During security testing, certain endpoints:

* Returned **database-level errors on unexpected input**
* Required **valid reCAPTCHA v3 tokens per request**
* Blocked traditional automation tools (e.g., sqlmap) due to dynamic validation

This created a gap between:

> Manual testing (signal detected) vs Automated validation (blocked by bot protection)

---

## ⚙️ Solution Approach

This framework implements a **browser-driven token acquisition pipeline** that:

1. Launches a real Chrome session via Selenium
2. Loads the target application page
3. Executes reCAPTCHA v3 client-side flow
4. Extracts valid tokens dynamically
5. Feeds tokens into external testing tools (e.g., sqlmap)
6. Maintains session consistency across requests

---

## 🧩 Architecture Flow

```
Browser Automation (Selenium)
        ↓
reCAPTCHA v3 Execution
        ↓
Token Extraction Layer
        ↓
Temporary Token Storage
        ↓
sqlmap / Testing Tool Injection Layer
        ↓
Target Application Validation
```

---

## 📁 Repository Structure

```
.
├── recaptcha_harvester.py     # Token generation automation script
├── sqlmap_command.txt         # Example sqlmap integration command
├── requirements.txt
└── README.md
```

---

## 🚀 Key Features

* Automated reCAPTCHA v3 token generation
* Session-aware browser automation
* Continuous / batch token harvesting modes
* Integration-ready with sqlmap workflows
* File-based token exchange mechanism
* Stable execution under dynamic JS environments

---

## 🧪 Usage Workflow

### 1. Start Token Harvester

```bash
python recaptcha_harvester.py
```

Select mode:

* Single token generation
* Batch token collection
* Continuous token streaming

---

### 2. Run SQLMap with Token Injection

Example integration (sanitized):

```bash
python sqlmap.py \
-u "https://example.com/register" \
--data="username=test&mobile=1*&recaptcha_response=PLACEHOLDER" \
--cookie="SESSION_ID_PLACEHOLDER" \
--eval="
import os,time

def wait_token():
    t=0
    while not os.path.exists('/tmp/current_recaptcha_token.txt'):
        time.sleep(0.2)
        t+=0.2
        if t>60:
            break

wait_token()

if os.path.exists('/tmp/current_recaptcha_token.txt'):
    with open('/tmp/current_recaptcha_token.txt') as f:
        recaptcha_response=f.read().strip()
    os.remove('/tmp/current_recaptcha_token.txt')
"
```

---

## 🔬 Results

* Identified potential SQL injection indicators in input handling
* Successfully validated automated request flow under reCAPTCHA v3 constraints
* Confirmed that bot protection alone does not eliminate backend logic flaws

However:

> The issue was later determined to be **non-exploitable under real-world constraints**, but still valuable from a security analysis perspective.

---

## 🛠️ Future Improvements

### 🔹 Puppeteer-based Migration (Recommended)

A more robust version of this framework can be implemented using **Puppeteer** instead of Selenium.

Advantages:

* Better control over Chrome DevTools Protocol (CDP)
* Improved stability for modern JavaScript-heavy applications
* More reliable async event handling
* Easier request interception and modification
* Reduced flakiness in token generation flows

### 🔹 Suggested Architecture Upgrade

```
Puppeteer Automation Layer
        ↓
Token Management API (Node.js)
        ↓
External Testing Tools (sqlmap / custom scripts)
```

This modular approach improves:

* Scalability
* Reliability
* Maintainability

---

## 📚 Key Learnings

* reCAPTCHA v3 is a **risk signal system**, not a security boundary
* Backend validation flaws can still exist behind strong front-end protections
* Automation in VAPT requires **workflow engineering**, not just tools
* Exploitability must always be separated from detection

---

## 🔗 Related Work

* Medium Writeup: https://medium.com/@sameerimr384/bypassing-recaptcha-v3-during-vapt-a-case-study-in-automated-sqli-validation-a54d259ab1d9
* Author: Muhammad Sameer - InfoSec Consultant (VAPT / Application Security)

---
