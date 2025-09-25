import smtplib
# import csv
from datetime import datetime
import re
from email_validator import validate_email, EmailNotValidError
from pathlib import Path
import pandas as pd
from email.message import EmailMessage
from string import Template

FILENAME = "recipients.csv"
FIELDNAMES = ["email", "name"]
LOGFILE = "program.log"


def log_message(message: str):
    """Append a timestamped message to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def input_validator():
    while True:
        try:
            email_input = input("Enter Email Address : ").strip()
          # validate , get info and replace with normalized form
            valid_email = validate_email(email_input).email  # normalized

            # --- Name validation ---
            # remove leading/trailing spaces
            name_input = input("Enter Name : ").strip()
            if not re.fullmatch(r"[A-Za-z\s'-]+", name_input):
                raise ValueError(
                    "Invalid name: must contain only letters, spaces")

            # Normalize capitalization (e.g., "john doe" → "John Doe")
            normal_name = " ".join(word.capitalize()
                                   for word in name_input.split())
            return valid_email, normal_name

        # if invalid, raise ValueError with explanation
        except EmailNotValidError as e:
            print(f"Error: Invalid email format: {e}")
        except ValueError as e:
            print(f"Error: {e}")


# --- CSV Storage with Pandas  ---
def store_in_csv(email, name):
    new_data = pd.DataFrame([{"email": email, "name": name}])
    if Path(FILENAME).exists():  # file exists
        df = pd.read_csv(FILENAME)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data

    before = len(df)
    newdf = df.drop_duplicates(subset=["email", "name"], keep="first")
    after = len(newdf)

    if after < before:
        print(f"⚠️ Duplicate entry ignored: {name} <{email}>")
        log_message(f"Duplicate dropped: {name} <{email}>")
        duplicate = True
    else:
        log_message(f"Stored contact: {name} <{email}>")
        duplicate = False

    newdf.to_csv(FILENAME, index=False)
    return duplicate


# creation of SMTP server
# the reason I use this password is because I generated it with google acounts settings
# https://myaccount.google.com/apppasswords?pli=1&rapt=AEjHL4ONjqTWPWqLUAdPHGVL3c4lLMQkj5qE5VUah3389MXs9-mR-oS1x8Cm-P-WfmfHC4UCJY53MPUDGbebWPkmXvuadSgoaUMBX8pE4GWYQcqmvC6wGx8
def emailCreation():
    html_content = Template(Path("index.html").read_text())

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        addr_email = "sweetfeedback@gmail.com" # add your email address here
        pw = "USE THE TOOL I MENTION ON THE COMMENT TO GENERATE A PASSWORD"
        smtp.login(addr_email, pw)

        df = pd.read_csv(FILENAME)
        names_list = dict(zip(df[FIELDNAMES[0]], df[FIELDNAMES[1]]))

        for email_add, name in names_list.items():
            try:
                email = EmailMessage()
                email["from"] = "Your name"
                email["to"] = email_add
                email["subject"] = "This is a try to send you my CV"
                email.set_content(
                    html_content.substitute({"name": name}), "html")

                smtp.send_message(email)
                print(f"✅ Sent mail to {name} ({email_add})")
                log_message(f"Email sent successfully: {name} <{email_add}>")

            except Exception as e:
                print(f"❌ Failed to send mail to {name} ({email_add})")
                log_message(f"ERROR sending to {name} <{email_add}>: {e}")

    print("✅ All emails processed!")


# --- Example usage ---
if __name__ == "__main__":
    email, name = input_validator()
    is_duplicate = store_in_csv(email, name)

    if not is_duplicate:   # only send email if not duplicate
        emailCreation()
    else:
        print("Skipped sending email to duplicate entry.")
"""
'''
Pros:
    Very lightweight, fast for tiny files.
    Good for projects where you want minimal imports, like this project
Cons 
    Harder to manipulate data (sorting, filtering, removing duplicates).
    Need to manually handle headers, data types, and appending safely.
    No advanced functionality like pivot tables, groupby, etc.
'''
    file_exists = Path(FILENAME).exists()
    write_header = True  # Assume we need a header initially
    if file_exists:
        # Check if file exists and whether header is needed
        with open(FILENAME, 'r', newline="", encoding="utf-8") as f:
            # Grab a sample of the CSV for format detection.
            sample = f.read(1024)
            f.seek(0)  # Rewind
            sniffer = csv.Sniffer()
            if sniffer.has_header(sample):  # If header exists, don’t write again
                write_header = False

    with open(FILENAME, 'a', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()

        writer.writerow({"email": email, "name": name})   # Add new row
"""
