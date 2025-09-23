# notify_email_send

I create a program that will :

- Ask the user to enter an email and a name (no values hard-coded).
- Ensure a CSV exists with a header row (create it if missing).
- Validate the email (basic check).
- Append the new entry (email, name) to the CSV.
- After successful storage, attempt to send a welcome email via SMTP.
- Report success/failure and allow retry or add another entry

---

## Main Process:
✅ Create the format of the columns I want the csv to have
✅ check if the csv exists and : 1. → if the csv doesn't exist then create it with the given format 2. → if the csv exists then append the new lines of data below the last entry
✅ create the smtp server to send the emails

Get input → validate → ensure storage → optional duplicate check → write row → confirm write → send email → report + log.

## Validation

1. The reason I used emailValidator is that it validates emails much more accurately than writing a regex, and can handle edge cases more efficiently.

2. <em>Syntax:</em> email parts in <b>email_validator library</b>:
   - valid.email → normalized email, ready for storage/comparison.
   - valid.local_part → the part before @.
   - valid.domain → the domain part after @.

3. What <b>"valid.email"</b> actually is:

- Lowercases the domain only (per RFC, domains are case-insensitive).

- Preserves the local part case (most providers treat local part case-insensitive, but technically it’s case-sensitive).

- Strips surrounding whitespace.

- Corrects minor formatting issues (if safe to do so).
