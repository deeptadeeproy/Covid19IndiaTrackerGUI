#Covid19IndiaTrackerGUI has been created by Deeptadeep Roy.
#This program along with its source code can be distributed, manipulated and used in any way someone sees fit.
#Made available by Deeptadeep Roy at Github.

import pip

# Checking and installing dependencies
def install(package):
    pip.main(['install', package])

if __name__ == '__main__':
    try:
        import PySimpleGUI as sg
    except ImportError:
        install('PySimpleGUI')
        import PySimpleGUI as sg

import json
import urllib.request
import urllib.error

sg.theme('DarkAmber')

# Globals
success = False
jsonData = ""
state = ""
district = ""
address = ""

# All url requests go through here
def get_data(url):
    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            global success
            global jsonData
            success = True
            jsonData = json.loads(response.read())
        else:
            sg.popup("Data not recieved. Unknown failure occurred.")
    except urllib.error.URLError as err:
        print(err)
        sg.popup("Failed to connect to the intenet.")

# Digit counter to validate PIN code
def countDigit(n):
    count = 0
    while n != 0:
        n //= 10
        count += 1
    return count

# Arraanging address for PIN code
def arrange_address():
    # print(jsonDataOne)
    global address
    if jsonData[0]["PostOffice"]:
        address = jsonData[0]["PostOffice"][0]["Block"] + ", " + jsonData[0]["PostOffice"][0][
            "District"] + ", " +\
                  jsonData[0]["PostOffice"][0]["State"]
        #print(f"\nYou searched for {address}.")
        global state
        global district
        state = jsonData[0]["PostOffice"][0]["State"]
        district = jsonData[0]["PostOffice"][0]["District"]
    else:
        sg.popup("Error: Invalid PIN Code")

# PIN code search
def pinSearch():
    global jsonData
    key = sg.popup_get_text("Enter PIN")
    if key:
        if key.isnumeric() and len(key) == 6:
            get_data("https://api.postalpincode.in/pincode/" + key)
            if success:
                sg.popup_timed("Please wait...")
                arrange_address()
                get_data("https://api.covid19india.org/state_district_wise.json")
                confirmed = jsonData[state]["districtData"][district]["confirmed"]
                del jsonData
                sg.popup("Confirmed positive cases of COVID19 in " + address, confirmed)
            else:
                sg.popup("Error: Invalid PIN Code")
        else:
            sg.popup("Error: Invalid PIN Code")

# India's Status Report
def status_ind():
    global jsonData
    sg.popup_timed("Please wait. Requesting data...")
    get_data("https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise")
    if success:
        lastRefreshed = jsonData["data"]["lastRefreshed"]
        confirmed = jsonData["data"]["total"]["confirmed"]
        recovered = jsonData["data"]["total"]["recovered"]
        deaths = jsonData["data"]["total"]["deaths"]
        active = jsonData["data"]["total"]["active"]
        sg.popup("Status as of " + str(lastRefreshed) + " :\n" + "Confirmed : " + str(confirmed) + "\n" + "Recovered : " + str(recovered) + "\n" +
        "Deaths : " + str(deaths) + "\n" +
        "Active : " + str(active) + "\n")
    else:
        sg.popup("Task failed.")

# World's Status Report
def status_world():
    global jsonData
    sg.popup_timed("Please wait. Requesting data...")
    get_data("https://covidapi.info/api/v1/global")
    if success:
        lastRefreshed = jsonData["date"]
        confirmed = jsonData["result"]["confirmed"]
        recovered = jsonData["result"]["recovered"]
        deaths = jsonData["result"]["deaths"]
        active = confirmed - (recovered + deaths)
        sg.popup("Status as of " + str(lastRefreshed) + " :\n" + "Confirmed : " + str(confirmed) + "\n" + "Recovered : " + str(recovered) + "\n" +
        "Deaths : " + str(deaths) + "\n" +
        "Active : " + str(active) + "\n")

# Statewise Report
def statewise():
    global jsonData
    key = sg.popup_get_text("Enter name of state or union territory: ")
    if key:
        sg.popup_timed("Please wait. Requesting data...")
        get_data("https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise")
        if success:
            boolFound = False
            for i in range(len(jsonData["data"]["statewise"])):
                if jsonData["data"]["statewise"][i]["state"].title() == key.title():
                    key = jsonData["data"]["statewise"][i]["state"]
                    boolFound = True
                    confirmed = jsonData["data"]["statewise"][i]["confirmed"]
                    recovered = jsonData["data"]["statewise"][i]["recovered"]
                    deaths = jsonData["data"]["statewise"][i]["deaths"]
                    active = jsonData["data"]["statewise"][i]["active"]
                    key = str(key)
                    key = key.upper()
                    sg.popup("STATUS OF " + key + "\n" + "Confirmed : " + str(confirmed) + "\n" + "Recovered : " + str(recovered) + "\n" +
                    "Deaths : " + str(deaths) + "\n" +
                    "Active : " + str(active) + "\n")
                if i == 35 and boolFound == False:
                    sg.popup("Error: Please check spelling.")

# Helpline number search
def help_num():
    global jsonData
    jsonData = {
        "Andhra Pradesh" : "08662410978", "Arunachal Pradesh" : "9436055743", "Assam" : "6913347770",
        "Bihar" : "104", "Chhattisgarh" : "104", "Goa" : "104",
        "Gujarat" : "104", "Haryana" : "8558893911", "Himachal Pradesh" : "104",
        "Jharkhand" : "104", "Karnataka" : "104", "Kerala" : "04712552056",
        "Madhya Pradesh" : "104", "Maharashtra" : "02026127394", "Manipur" : "3852411668",
        "Meghalaya" : "108", "Mizoram" : "102", "Nagaland" : "7005539653",
        "Odisha" : "9439994859", "Punjab" : "104", "Rajasthan" : "01412225624",
        "Sikkim" : "104", "Tamil Nadu" : "04429510500", "Telangana" : "104",
        "Tripura" : "03812315879", "Uttarakhand" : "104", "Uttar Pradesh" : "18001805145",
        "West Bengal" : "1800313444222", "Andaman And Nicobar Islands" : "03192232102", "Chandigarh" : "9779558282",
        "Dadra And Nagar Haveli" : "104", "Daman And Diu" : "104", "Delhi" : "01122307145",
        "Jammu And Kashmir" : "01912520982", "Ladakh" : "01982256462", "Lakshadweep" : "104",
        "Puducherry" : "104"
    }
    key = sg.popup_get_text("Enter name of state or union territory: ")
    if key:
        if key.title() in jsonData.keys():
            sg.popup("Helpline number for " + key.title().upper() + ": \n" + jsonData[key.title()])
        else:
            sg.popup("Error: Please check spelling.")
        del jsonData

# Main Menu creation
buttons = ["Search by PIN code", "View India's status report", "View World's status report", "View statewise report", "Search helpline number (statewise)", "Exit"]
layout = [[sg.Text("Please choose an option from the menu: \n")], [sg.Button(buttons[0], size = (30, 1))], [sg.Button(buttons[1], size = (30, 1))], [sg.Button(buttons[2], size = (30, 1))], [sg.Button(buttons[3], size = (30, 1))], [sg.Button(buttons[4], size = (30, 1))] ,[sg.Button(buttons[5], button_color = ('white', 'red'))]]
window = sg.Window("COVID19 Tracker India", layout, margins = (75, 50))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == buttons[5]:
        break
    elif event == buttons[0]:
        pinSearch()
    elif event == buttons[1]:
        status_ind()
    elif event == buttons[2]:
        status_world()
    elif event == buttons[3]:
        statewise()
    elif event == buttons[4]:
        help_num()
