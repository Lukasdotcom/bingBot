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
version = "v1.0"
def findElement(by, value): # Short hand to find a element and wait 5 seconds for it to appear
    return WebDriverWait(driver, 30).until(EC.presence_of_element_located((by, value)))

# Finds the configuration file for this
try:
    location = __file__[: __file__.rindex("/") + 1]
except:
    location = __file__[:__file__.rindex("\\") + 1]
choice = "n"
if os.path.isfile(f"{location}.config.json"):
    choice = input("Previous config found press enter to use and enter n and then press enter to use a new config")
# Used to check if new config is needed
if choice:
    username = input("Enter here the username for your microsoft account: ")
    searches = int(input("Enter the number of searches you want to do 30 is the recommendation: "))
    browser_driver = input("Enter the path to the geckodriver: ")
    browser = input("Enter firefox if you are using geckodriver and chrome if you are using chromedriver")
    config = {"version" : version, "username" : username, "searches" : searches, "driver" : browser_driver, "browser": browser}
    with open(f"{location}.config.json", "w") as f:
        json.dump(config, f)
else:
    with open(f"{location}.config.json") as f:
        config = json.load(f)
# Checks which browser to run it on.
if config["browser"] == "firefox":
    from selenium.webdriver.firefox.service import Service
else:
    from selenium.webdriver.chrome.service import Service
try:
    browser_driver = Service(config["driver"])
except WebDriverException:
    print("Could not find your driver please install it and put in the correct path")
print("Reminder to keep the firefox window open that will pop up after you enter the password.")
print("Enter your microsoft password.")
enterPassword = getpass.getpass()
# Checks which browser to start
if config["browser"] == "firefox":
    driver = webdriver.Firefox(service=browser_driver)
else:
    driver = webdriver.Chrome(service=browser_driver)
time.sleep(2)
driver.get("https://login.live.com/login.srf?id=264960")

# Does the login
time.sleep(1)
element = findElement(By.ID, "i0116")
element.send_keys(config["username"])
element = findElement(By.ID, "idSIButton9")
element.click()
time.sleep(1)
element = findElement(By.ID, "i0118")
element.send_keys(enterPassword)
element = findElement(By.ID, "idSIButton9")
element.click()
element = findElement(By.ID, "idBtn_Back")
element.click()
# Loads the wordlist
with open(f"{location}wordlist.json") as f:
    words = json.load(f)
for x in range(config["searches"]):
    driver.get(f"http://www.bing.com/search?q={random.choice(words)}")
    time.sleep(random.randint(0, 5))
driver.quit()
print("Finished")
