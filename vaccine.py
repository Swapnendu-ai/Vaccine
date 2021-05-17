import requests
import time
from datetime import date, datetime
from playsound import playsound
import json

URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/"
BY_PIN = "calendarByPin"
BY_DISTRICT = "findByDistrict"
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

def myInput(inputQuery:str,errorQuery:str,convertFunc):
    while True:
        try:
            return convertFunc(input(inputQuery+": "))
        except:
            print(errorQuery)

def placeQuery(url,query):
    url = url + '?'
    for key, value in query.items():
        url += f"{key}={value}&"

    return url[:-1]


currentDate = date.today()
query = {
    "date" : f"{currentDate.day}-{currentDate.month}-{currentDate.year}"
}
pincodes = [831001,831003,831004,831011,831012,831013]
# numberOfPincodes = myInput("How many pincodes do you wanna check?","Please enter a number",lambda x : int(x))
# for i in range(numberOfPincodes):
#     pincodes.append(myInput(f"Enter pincode {i+1}","Your pincode is not a number lol",lambda x : str(int(x))))
age = 23# myInput("Enter your age","Your age is not a number lol",lambda x : int(x))
run = 0
while True:
    query["pincode"] = pincodes[run%len(pincodes)]
    run += 1
    try:
        response = requests.get(placeQuery(URL+BY_PIN,query),headers=HEADER)
        if response.status_code == 200:
            data = response.json()
            found = False
            centerFound = None
            for center in data["centers"]:
                for session in center["sessions"]:
                    found |= age >= session["min_age_limit"] and session["available_capacity_dose1"] > 1
                if found and centerFound is None:
                    centerFound = {center["name"]:center["sessions"]}
                # print(age,center)
            if found:
                import webbrowser
                webbrowser.open("https://selfregistration.cowin.gov.in/")
                while True:
                    print(f"VACCINE FOUND IN {query['pincode']} {json.dumps(centerFound,indent=4)}")
                    try:
                        playsound("mixkit-arcade-retro-game-over-213.wav")
                    except:
                        print("\a")
            else:
                print(f"No vaccinces available in {query['pincode']} at {datetime.now()}".split('.')[0])
    except:
        print("Could not make a request. Please check your internet connection \a")
    time.sleep(4)
# print(data.text)
    # time.sleep(5)


