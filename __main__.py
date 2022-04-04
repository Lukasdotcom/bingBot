#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import getpass
import random

# Version stored here
version = "v1.1"
def findElement(by, value): # Short hand to find a element and wait 5 seconds for it to appear
    return WebDriverWait(driver, 30).until(EC.presence_of_element_located((by, value)))

def configUpdate(previousConfig): # Used to update the config
    browser = input("Enter firefox if you are using geckodriver and chrome if you are using chromedriver: ")
    browser_driver = input("Enter the path to the geckodriver/chromedriver: ")
    config = {"version" : version, "driver" : browser_driver, "browser": browser, "users" : []}
    with open(f"{location}.config.json", "w") as f:
        json.dump(config, f)
    return config

# Finds the configuration file for this
try:
    location = __file__[: __file__.rindex("/") + 1]
except:
    location = __file__[:__file__.rindex("\\") + 1]
choice = "n"
if os.path.isfile(f"{location}.config.json"):
    choice = print("Previous config found.")
# Used to check if new config is needed
try:
    with open(f"{location}.config.json") as f:
        config = json.load(f)
except:
    config = {"version" : "notFound"}
if version != config["version"]:
    if config["version"] == "v1.0":
        config = {
            "version" : "v1.1",
            "driver" : config["driver"],
            "browser" : config["browser"],
            "users" : [{
                "username" : config["username"],
                "searches" : config["searches"],
                "passwords" : "" 
        }]}
        with open(f"{location}.config.json", "w") as f:
            json.dump(config, f)
    else:
        print("Config has a different version.")
        config = configUpdate(config)
# Checks which browser to run it on.
while True:
    print("""
Available choices
Print accounts: p
Add account: a
Delete account: d
Run bot and quit afterwards: r
Quit this: q
    """)
    choice = input("What would you like to do: ")
    if choice == "p":
        for id, account in enumerate(config["users"]):
            name = account["username"]
            print(f"id #{id} with username {name}")
            input("Press enter to continue")
    elif choice == "a":
        username = input("Enter the username for this user: ")
        password = input("Enter the password for this user(This will be unencrypted if you do not want to store it just press enter now and you will be asked just before the bot starts): ")
        searches = input("Enter the number of searches for this user: ")
        config["users"].append({"username": username, "password" : password, "searches" : searches})
    elif choice == "d":
        number = input("Enter the id which you would like to remove: ")
        username = config["users"].pop(int(number))
        username = username["username"]
        print(f"Removed entry #{number} which had the username {username}")
    elif choice == "r":
        break
    elif choice == "q":
        exit()
    else:
        print("Not valid choice")
    with open(f"{location}.config.json", "w") as f:
        json.dump(config, f)
if config["browser"] == "firefox":
    from selenium.webdriver.firefox.service import Service
else:
    from selenium.webdriver.chrome.service import Service
try:
    browser_driver = Service(config["driver"])
except WebDriverException:
    print("Could not find your driver please install it and put in the correct path")
print("Reminder to keep the firefox/chrome window open that will pop up after you enter the password.")
# Goes through every user
for userConfig in config["users"]:
    # Checks which browser to start
    if config["browser"] == "firefox":
        driver = webdriver.Firefox(service=browser_driver)
    else:
        driver = webdriver.Chrome(service=browser_driver)
    driver.get("https://login.live.com/login.srf?id=264960")
    # Does the login
    time.sleep(1)
    element = findElement(By.ID, "i0116")
    element.send_keys(userConfig["username"])
    element = findElement(By.ID, "idSIButton9")
    element.click()
    time.sleep(1)
    element = findElement(By.ID, "i0118")
    if userConfig["password"]:
        enterPassword = userConfig["password"]
    else:
        username = userConfig["username"]
        print(f"Enter microsoft password for {username} shown in the browser")
        enterPassword = getpass.getpass()
    element.send_keys(enterPassword)
    element = findElement(By.ID, "idSIButton9")
    element.click()
    element = findElement(By.ID, "idBtn_Back")
    element.click()
    # Loads the wordlist
    with open(f"{location}wordlist.json") as f:
        words = json.load(f)
    for x in range(int(userConfig["searches"])):
        driver.get(f"http://www.bing.com/search?q={random.choice(words)}")
        time.sleep(random.randint(1, 5))
    driver.quit()
print("Finished")
