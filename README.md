# notify_email_send

A simple Python utility that lets users register (name + email), stores the data in a CSV file, and then attempts to send a “welcome” email via SMTP.

---

## Table of Contents

* [Features](#features)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [Configuration](#configuration)
* [How it works](#how-it-works)
* [Validation & Error Handling](#validation--error-handling)
* [Future Improvements / TODOs](#future-improvements--todos)
* [License](#license)

---

## Features

* Prompt user to input **name** and **email** (no hard-coded values).
* Maintains a CSV file (with header) for entries — auto-creates it if missing.
* Validates email addresses using the `email_validator` library.
* Appends new subscriber entries (name + normalized email).
* Attempts to send a welcome email via SMTP.
* Reports status (success/failure) and allows retry or adding more entries.

---

## Prerequisites

* Python 3.7+
* Access to an SMTP server (e.g. Gmail SMTP, or your own mail server)
* Internet connection (for sending emails)
* The `email_validator` Python package

You can install dependencies with:

```bash
pip install email-validator
```

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/VasilikiPapadimou/notify_email_send.git
   cd notify_email_send
   ```

2. (Optional) Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # on Linux / macOS
   venv\Scripts\activate      # on Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   If you do not have a `requirements.txt`, simply:

   ```bash
   pip install email-validator
   ```

---

## Usage

Run the main script:

```bash
python signup_notify.py
```

The program will:

1. Ask for your **name** and **email**.
2. Validate the email format.
3. Ensure the CSV file exists (if not, create it with headers).
4. Append the new entry to the CSV.
5. Attempt to send a welcome email.
6. Report success or failure.
7. Offer options to retry sending or add another subscriber.

---

## Configuration

Before running, you’ll likely need to configure your SMTP settings in the script (or via a config file if you extend it). Typical SMTP parameters include:

* SMTP server host (e.g. `smtp.gmail.com`)
* SMTP server port (e.g. `587` for TLS)
* Username / password for authentication
* Use TLS / SSL settings
* Sender (“from”) email / name
* Email subject / body templates

You should locate the SMTP configuration section in **signup_notify.py** and update those values to match your email provider.

---

## How it works (internals)

Here’s a rough flow of the program:

1. **User Input**
   Prompt for name & email.

2. **Email Validation**
   Use `email_validator` to parse and normalize the email. If invalid, prompt again.

3. **CSV Handling**

   * Check if file `subscribers.csv` (or whichever name you choose) exists.
   * If not, create it and write a header row (e.g. `name,email`).
   * Append the new row (name, normalized email).

4. **Email Sending**

   * Use the SMTP library (e.g. `smtplib`) to connect to the configured SMTP server.
   * Log in (if needed).
   * Format a welcome message (text or HTML).
   * Send the email.

5. **User Feedback / Retry**
   If sending fails, show the error and ask whether to retry. Also, allow entering another name/email to repeat the process.

---

## Validation & Error Handling

* Email validation is delegated to `email_validator`, which handles many edge cases better than a simple regex.
* The library normalizes domains (lowercasing) and strips whitespace.
* The script should catch SMTP / connection / authentication errors and display meaningful messages.
* It should avoid silent failures.
* Duplicate email detection is a possible extension (not currently present) to avoid repeated entries.



