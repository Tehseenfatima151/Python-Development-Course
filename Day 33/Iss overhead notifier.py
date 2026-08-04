import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 24.8607   # Replace with your latitude
MY_LONG = 67.0011  # Replace with your longitude
my_email = "your_email@gmail.com"
my_password = "your_app_password"


def is_iss_overhead():
    """Checks whether the ISS is currently within 5 degrees of your location."""
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    return MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5


def is_night():
    """Checks whether it is currently nighttime at your location."""
    parameters = {"lat": MY_LAT, "lng": MY_LONG, "formatted": 0}
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour

    return time_now >= sunset or time_now <= sunrise


def send_alert():
    """Sends an email alert notifying that the ISS is overhead."""
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg="Subject:Look Up!\n\nThe ISS is above you in the sky right now!"
        )


def run_monitor():
    print("ISS Overhead Notifier is running... checking every 60 seconds.")
    while True:
        time.sleep(60)
        if is_iss_overhead() and is_night():
            send_alert()
            print("Alert sent! The ISS is overhead and it's dark.")
        else:
            print("Conditions not met. Checking again in 60 seconds.")


if __name__ == "__main__":
    run_monitor()