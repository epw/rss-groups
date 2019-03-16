#! /usr/bin/env python3

import requests

def wordpress(url):
    username = "rssgroup@willisson.org"
    password = "RSS Groups will set us free"
    r = requests.post("https://wordpress.com/wp-login.php",
                      data = {"log": username,
                              "pwd": password,
                              "wp-submit": "Log In",
                              "redirect_to": "https://wordpress.com/wp-admin/"})
    r = requests.get(url, cookies=r.cookies)
    return r.text
#    print(r.text)
#    print()
#    print("Cookies")
#    for cookie in r.cookies:
#        print(str(cookie))

if __name__ == "__main__":
    wordpress()
