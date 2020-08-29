import time
import datetime
import schedule
from subprocess import Popen, PIPE
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

#Creation of headless chromedriver for get_schedule(), fill in your own USER_AGENT
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920x1080")
options.add_argument("user-agent=USER_AGENT")
driver = webdriver.Chrome(options=options, executable_path='./chromedriver')

#Asks for user input of zoom links for class_num classes
def get_classes(class_num):
    id_and_pwd = [""]
    for i in range(1,class_num+1):
        response = input(f"Zoom Link for Period {i}?\n")
        pwd = response[(response.index("=")+1):]
        try:
            id = response[(response.index("j/")+2):(response.index("=")-4)]
        except:
            id = response[(response.index("my/") + 3):(response.index("=") - 4)]
        id_and_pwd.append(id + " " + pwd)
    return id_and_pwd

#Gets the day's schedule, redacted website
def get_schedule(today):
    driver.get(website)
    text = driver.find_element_by_xpath("//div[@class='Rotation']").text
    ind1 = text.index("it's")
    ind2 = text.index("rotation")
    rotation = text[ind1+5:ind2-1]
    if today.weekday() > 4:
        print("NO SCHOOL")
        return []
    if rotation == "Day 1":
        print(rotation + "\n")
        return ["1 08:40", "2 09:40", "3 10:40", "4 12:55", "5 13:55"]
    elif rotation == "Day 2":
        print(rotation + "\n")
        return ["6 08:40", "7 09:40", "1 010:40", "2 12:55", "3 13:55"]
    elif rotation == "Day 3":
        print(rotation + "\n")
        return ["4 08:40", "5 09:40", "6 010:40", "7 12:55", "1 13:55"]
    elif rotation == "Day 4":
        print(rotation + "\n")
        return ["2 08:40", "3 09:40", "4 10:40", "5 12:55", "6 13:55"]
    elif rotation == "Day 5":
        print(rotation + "\n")
        return ["7 08:40", "1 09:40", "2 10:40", "3 12:55", "4 13:55"]
    elif rotation == "Day 6":
        print(rotation + "\n")
        return ["5 08:40", "6 09:40", "7 10:40", "1 12:55", "2 13:55"]
    elif rotation == "Day 7":
        print(rotation + "\n")
        return ["3 08:40", "4 09:40", "5 10:40", "6 12:55", "7 13:55"]
    elif rotation == "A_Block":
        print(rotation + "\n")
        return ["1 08:40", "2 10:00", "3 12:35", "4 13:55"]
    elif rotation == "Late_B_Block":
        print(rotation + "\n")
        return ["5 10:10", "6 12:35", "7 13:55"]
    else:
        print("NO SCHOOL + \n")
        return []

#Logins into zoom with class pwd and id using AppleScript
def login(list,class_num):
    scpt = f'''
        try
            tell application "zoom.us" to quit
                on error error_message number error_number
                    if error_number is equal to -128 then
                    --Keep Calm and Carry On
                    else
                        display dialog error_message
                    end if
        end try
        delay 2
        tell application "zoom.us" to activate
        tell application "System Events" to tell process "zoom.us"
            delay 3
            click menu item "Join Meeting..." of menu "Zoom.us" of menu bar 1
            delay 3
            keystroke "{list[class_num].split(" ")[0]}"
            click checkbox 1 of window 1
            click button 2 of window 1
            delay 3
            keystroke "{list[class_num].split(" ")[1]}"
            click button 2 of window 1
        end tell
        '''
     
    args = ['2', '2']
    p = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(scpt)
    print(p.returncode, stdout, stderr)

#Schedules classes for the day, runs in the background for multiple days
def main(today,list):
    class_schedule = get_schedule(today)
    try:
        for period in class_schedule:
            print("Scheduling... " + period)
            schedule.every().day.at(period.split(" ")[1]).do(login, [list, int(period.split(" ")[0])])
    finally:
        while True:
            schedule.run_pending()
            time.sleep(1)
            if datetime.date.today() > today:
                schedule.clear()
                break

if __name__ == "__main__":
    num_days = 0
    class_list = get_classes(7)
    while True:
        num_days += 1
        print(f"\nNew Day! We're on day {num_days} of the program. Today's schedule is:")
        main(datetime.date.today(), class_list)
