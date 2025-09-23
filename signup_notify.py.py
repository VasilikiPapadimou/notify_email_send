import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path
import csv


FILENAME = "recipients.csv"
FIELDNAMES = ["email", "name"]

# Check if CSV exists and read existing rows
def check_csv(filename):
    try:
        with open(filename, "r", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        return True, rows
    except FileNotFoundError:
        return False, []
     
# Ceate CSV with header
def create_csv(filename, fieldnames):
  with open(filename, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

# Append an entry
def append_entry(filename, entry, fieldnames):
    # If file doesn't exist, write header first
    file_exists, _ = check_csv(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)
    
# Input an entry
def input_entry():
    email = input("Enter email: ").strip()
    name = input("Enter name: ").strip()
    return {"email": email, "name": name}

      
#creation of SMTP server
#the reason I use this password is because I generated it with google acounts settings
#https://myaccount.google.com/apppasswords?pli=1&rapt=AEjHL4ONjqTWPWqLUAdPHGVL3c4lLMQkj5qE5VUah3389MXs9-mR-oS1x8Cm-P-WfmfHC4UCJY53MPUDGbebWPkmXvuadSgoaUMBX8pE4GWYQcqmvC6wGx8
def emailCreation(FIELDNAMES):
    html_content = Template(Path("index.html").read_text())

    with smtplib.SMTP(host = "smtp.gmail.com",port = 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        myaccount = smtp.login("1vikpapa1@gmail.com", 'rfde smze dfkc nsrn')
        
        # Loop through all recipients
        for email_add,name in names_list.items(): 
            #email creation
            email = EmailMessage()
            email['from'] = "Your name"
            email['to'] = email_add
            email['subject'] = 'This is a try to send you my CV'
            email.set_content(html_content.substitute({'name': name}),"html")
            smtp.send_message(email)
            print(f"Send mail to {name} ({email})")

    print("✅ All emails sent!")



# -------- Main workflow --------
def main():
    while True:
        entry = input_entry()
        append_entry(FILENAME, entry, FIELDNAMES)
        print("Entry added!")
        
        cont = input("Add another? (y/n): ").strip().lower()
        if cont != "y":
            break
        # Now read recipients and send emails
        with open(FILENAME, "r", newline="") as f:
            reader = csv.DictReader(f)
            recipients = list(reader)

        emailCreation(recipients, FIELDNAMES)
    print("All done! You can now send emails.")
main()