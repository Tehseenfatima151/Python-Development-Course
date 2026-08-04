from datetime import datetime
import pandas as pd
import random
import smtplib

my_email = "your_email@gmail.com"
my_password = "your_app_password"


def send_birthday_email(recipient_email, personalized_letter):
    """Sends the personalized birthday email via Gmail's SMTP server."""
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=recipient_email,
            msg=f"Subject:Happy Birthday!\n\n{personalized_letter}"
        )


def check_birthdays():
    today = datetime.now()
    today_tuple = (today.month, today.day)

    data = pd.read_csv("birthdays.csv")
    birthdays_dict = {(row.month, row.day): row for (index, row) in data.iterrows()}

    if today_tuple in birthdays_dict:
        birthday_person = birthdays_dict[today_tuple]

        file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
        with open(file_path) as letter_file:
            contents = letter_file.read()

        personalized_letter = contents.replace("[NAME]", birthday_person["name"])

        send_birthday_email(birthday_person["email"], personalized_letter)
        print(f"Birthday email sent to {birthday_person['name']}!")
    else:
        print("No birthdays today.")


if __name__ == "__main__":
    check_birthdays()