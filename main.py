import requests
from datetime import datetime
import time
import smtplib

MY_EMAIL = "dummy@gmail.com"
MY_PASSWORD = 'dummypassword'
MY_LAT = 51.919437 # Your latitude
MY_LONG = 19.145136 # Your longitude

def getISScoord():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return iss_latitude, iss_longitude

#Your position is within +5 or -5 degrees of the ISS position.

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

def nearISS(my_lat, my_lng, iss_lat, iss_lng):
    if (iss_lat >= my_lat-5 and iss_lat <= my_lat+5) and (iss_lng >= my_lng-5 and iss_lng <= my_lng+5):
        return True
    else:
        return False
    
def isDark():
    parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()
    curr_hr = time_now.hour
    if curr_hr < sunrise and curr_hr > sunset:
        return True
    else:
        return False

while True:
    time.sleep(1)
    iss_latitude, iss_longitude = getISScoord()
    print(iss_latitude, iss_longitude)
    if nearISS(MY_LAT,MY_LONG, iss_lat=iss_latitude,iss_lng=iss_longitude) and isDark():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs="target@gmail.com", msg="Subject: ISS is near you\n\nLook up right now and you may see the ISS!")
    else:
        print("Not yet!")

