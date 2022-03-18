#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from colorama import Fore, Style, Back, init

import warnings

import getpass
import pdb
import time
import random
import sys
import os

# Colorama, Windows compatability.
init()

def sleepy_time():
    t = random.uniform(4.40, 5.420)
    print(f"[-] " + Fore.YELLOW + f"Sleeping for " + "{:.2f}".format(t) + " seconds... " + Style.RESET_ALL)
    time.sleep(t)
    

if len(sys.argv) < 3 :
    print("Please provide a client name &  IP list.")
    print(f"Usage: {sys.argv[0]} <client_name> <IP_List.txt>")
    sys.exit(1)


''' Variables '''

url = "https://localhost:8834"
username = "admin"

client_name = sys.argv[1]
ip_list = sys.argv[2]

''' // Variables '''


print(f"""
█▄░█ █▀▀ █▀ █▀ █░█ █▀   ▄▀█ █░█ ▀█▀ █▀█ █▀▄▀█ ▄▀█ ▀█▀ █▀█ █▀█
█░▀█ ██▄ ▄█ ▄█ █▄█ ▄█   █▀█ █▄█ ░█░ █▄█ █░▀░█ █▀█ ░█░ █▄█ █▀▄

                    Written by Jeff Bowie
                    github.com/jeffjbowie
""")

if not os.path.exists(ip_list):
    print(f"[!] " + Fore.RED + f"{ip_list} not found ..." + Style.RESET_ALL )
    sys.exit(1)

# Hide warnings, they kill the vibe.
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", category=UserWarning) 

# Securely obtain Nessus password from user.
password = getpass.getpass(f"[Nessus] {username} Password: ")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

print(f"\n\n[*] " + Fore.GREEN  + f"Browsing to {url}..." + Style.RESET_ALL )

# Start Chrome & browse to Nessus
browser = webdriver.Chrome(options=chrome_options)
browser.get(url)
sleepy_time()


print(f"[*] " + Fore.GREEN  + f"Bypassing invalid SSL ..." + Style.RESET_ALL )

# Click advanced button.
browser.find_element_by_id('details-button').click()
sleepy_time()

# Click Proceed to localhost
browser.find_element_by_id('proceed-link').click()
sleepy_time()

print("[*] " + Fore.GREEN + "Logging into Nessus..." + Style.RESET_ALL)

# Send username to Chrome
browser.find_element_by_class_name('login-username').send_keys(username)
sleepy_time()

# Send password to Chrome
browser.find_element_by_class_name('login-password').send_keys(password)
sleepy_time()

# Click on Sign In
browser.find_element_by_tag_name('button').click()
sleepy_time()


pdb.set_trace()

print("[*] " + Fore.GREEN + f"Starting a new scan for {client_name}..." + Style.RESET_ALL)

# Start a new scan
browser.find_element_by_id('titlebar').find_elements_by_tag_name('a')[0].click()
sleepy_time()

# Select "Advanced Scan"
browser.find_elements_by_class_name('library-item')[2].click()
sleepy_time()

# Enter Client Name
browser.find_element_by_class_name('editor-settings-section').find_elements_by_tag_name('input')[0].send_keys(client_name)
sleepy_time()

print("[*] " + Fore.GREEN + f"Adding targets..." + Style.RESET_ALL)
# Place IP addreses/ranges into "Targets"
with open(ip_list) as f:
   for line in f:
       browser.find_element_by_class_name('editor-settings-section').find_elements_by_tag_name('textarea')[1].send_keys(line)

print("[*] " + Fore.GREEN + f"Modifying scan options..." + Style.RESET_ALL)
# Click on "Discovery"
browser.find_element_by_class_name('scan-editor').find_elements_by_tag_name('li')[4].find_elements_by_tag_name('span')[0].click()
sleepy_time()

# Click on Port Scanning
browser.find_element_by_class_name('scan-editor').find_elements_by_tag_name('li')[6].click()
sleepy_time()

# Enter "all" to scan ports 1-65535.
browser.find_elements_by_class_name('editor-input')[27].clear()
browser.find_elements_by_class_name('editor-input')[27].send_keys('all')
sleepy_time()

# Launch the scan!
print("[*] " + Fore.GREEN + f"Launching scan..." + Style.RESET_ALL )

# Click on dropdown.
browser.find_elements_by_class_name('down')[0].click()

# Click on "Launch"
browser.find_element_by_class_name('dropdown').find_elements_by_tag_name('li')[0].click()
