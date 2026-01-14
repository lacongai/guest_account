import requests
import json
from colorama import Fore, init

init(autoreset=True)

API_TOKEN_URL = "https://jwt-token-api-six.vercel.app/token"
API_DECODE_URL = "https://shiny-couscous-nu.vercel.app/decode"
API_BIO_URL = "https://shiny-couscous-nu.vercel.app/checkbio"

DECODE_KEY = "hentaiz"


def pretty_print(title, data):
    print(Fore.GREEN + f"\n===== {title} =====\n")
    print(json.dumps(data, indent=4, ensure_ascii=False))
    print(Fore.GREEN + "\n========================\n")


def get_token(uid, password):
    r = requests.get(
        API_TOKEN_URL,
        params={"uid": uid, "password": password},
        timeout=10
    )
    return r.status_code, r.json()


def decode_token(token):
    r = requests.get(
        API_DECODE_URL,
        params={"token": token, "key": DECODE_KEY},
        timeout=10
    )
    return r.status_code, r.json()


def check_bio(account_id):
    # API 3: ID gắn trực tiếp sau ?
    url = f"{API_BIO_URL}?{account_id}"
    r = requests.get(url, timeout=10)
    return r.status_code, r.json()


if __name__ == "__main__":
    print(Fore.MAGENTA + "=== ALL IN ONE TOOL (3 APIs) ===\n")

    uid = input(Fore.YELLOW + "Nhập UID: ").strip()
    password = input(Fore.YELLOW + "Nhập PASSWORD: ").strip()

    if not uid or not password:
        print(Fore.RED + "[-] UID hoặc PASSWORD không được để trống")
        exit()

    try:
        # -------- API 1 --------
        print(Fore.CYAN + "[*] API 1: Lấy token...")
        status1, api1 = get_token(uid, password)
        print(Fore.YELLOW + f"[+] Status Code: {status1}")
        pretty_print("API 1 RESULT (GET TOKEN)", api1)

        token = api1.get("token")
        if not token:
            print(Fore.RED + "[-] Không lấy được token → dừng")
            exit()

        # -------- API 2 --------
        print(Fore.CYAN + "[*] API 2: Decode token...")
        status2, api2 = decode_token(token)
        print(Fore.YELLOW + f"[+] Status Code: {status2}")
        pretty_print("API 2 RESULT (DECODE)", api2)

        account_id = api2.get("payload", {}).get("account_id")
        if not account_id:
            print(Fore.RED + "[-] Không tìm thấy account_id → dừng")
            exit()

        # -------- API 3 --------
        print(Fore.CYAN + "[*] API 3: Check bio...")
        status3, api3 = check_bio(account_id)
        print(Fore.YELLOW + f"[+] Status Code: {status3}")
        pretty_print("API 3 RESULT (CHECK BIO)", api3)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[-] Lỗi kết nối API: {e}")
    except json.JSONDecodeError:
        print(Fore.RED + "[-] API trả về dữ liệu không phải JSON")