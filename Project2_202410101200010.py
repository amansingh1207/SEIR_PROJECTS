# Count the frequency of every word (a word is a sequence of alphanumeric characters, case does NOT matter) in the body of your document
# Write a 64 bit hash function for a word using polynomial rolling hash function

# hash(s) = s[0] + s[1]*p + s[2]*(p)**2 +....+ s[n-1]*(p)**(n-1) (mod m)

# Here s[i] is the ASCII for letter i in a word, use p = 53 and m = 264
# Compute Simhash for the document (as shown in slide 52)
# Modify your program to take two URLs from the web on the command line, print how many bits are common in their simhashes.

import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import re

def get_rolling_hash(word):
    p = 53
    m = 2**64
    h_val = 0
    p_pow = 1
    for char in word:
        h_val = (h_val + ord(char) * p_pow) % m
        p_pow = (p_pow * p) % m
    return h_val

def extract_body(url, driver):
    driver.get(url)
    time.sleep(4)
    return driver.find_element(By.TAG_NAME, "body").text

def find_simhash(text):
    words = re.findall(r'\w+', text.lower())
    count_dict = {}
    for word in words:
        if word not in count_dict:
            count_dict[word] = 1
        else:
            count_dict[word] += 1

    arr = [0] * 64
    for word, freq in count_dict.items():
        word_hash = get_rolling_hash(word)
        for i in range(64):
            if (word_hash >> i) & 1:
                arr[i] += freq
            else:
                arr[i] -= freq

    simhash = 0
    for i in range(64):
        if arr[i] > 0:
            simhash |= (1 << i)
    return simhash


def main():
    if len(sys.argv) < 3:
        print("Enter both the url that you want to compare")
        return
    url1 = sys.argv[1]
    url2 = sys.argv[2]
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service = s)

    try:
        t1 = extract_body(url1, driver)
        hash1 = find_simhash(t1)

        t2 = extract_body(url2, driver)
        hash2 = find_simhash(t2)

        diff = hash1 ^ hash2
        common_bits = 64 - bin(diff).count('1')

        print(f"\nSimhash 1: {bin(hash1)}")
        print(f"Simhash 2: {bin(hash2)}")
        print(f"Common Bits: {common_bits} / 64")

    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()
if __name__ == "__main__":
    main()