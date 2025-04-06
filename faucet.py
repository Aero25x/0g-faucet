import json

import requests
import time
from colorama import init, Fore




print("""



  _    _ _     _     _             _____          _
 | |  | (_)   | |   | |           / ____|        | |
 | |__| |_  __| | __| | ___ _ __ | |     ___   __| | ___
 |  __  | |/ _` |/ _` |/ _ \ '_ \| |    / _ \ / _` |/ _ \\
 | |  | | | (_| | (_| |  __/ | | | |___| (_) | (_| |  __/
 |_|  |_|_|\__,_|\__,_|\___|_| |_|\_____\___/ \__,_|\___|

               0G Faucet by Aero25x
            https://t.me/hidden_coding


    """)



# Initialize terminal color output
init(autoreset=True)

# User settings
CAPTCHA_API_KEY = ''  # Replace with your 2Captcha API key
HCAPTCHA_SITE_KEY = '1230eb62-f50c-4da4-a736-da5c3c342e8e'
FAUCET_ENDPOINT = 'https://992dkn4ph6.execute-api.us-west-1.amazonaws.com/'
MAX_RETRY = 2
REQUEST_DELAY = 10

def read_lines(filepath):
    """Read non-empty lines from a file."""
    try:
        with open(filepath, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except:
        return []

def format_proxy(proxy_str):
    """Convert proxy from 'ip:port:user:pass' format to requests format."""
    parts = proxy_str.strip().split(':')
    if len(parts) == 4:
        ip, port, user, passwd = parts
        formatted = f"http://{user}:{passwd}@{ip}:{port}"
        return {'http': formatted, 'https': formatted}
    elif len(parts) == 2:
        ip, port = parts
        formatted = f"http://{ip}:{port}"
        return {'http': formatted, 'https': formatted}
    else:
        raise ValueError(f"Invalid proxy format: {proxy_str}")

def mask_proxy(proxy_str):
    """Hide proxy credentials for safe logging."""
    parts = proxy_str.split(':')
    if len(parts) == 4:
        return f"{parts[0]}:****:****:****"
    elif len(parts) == 2:
        return f"{parts[0]}:****"
    return "****"

def solve_hcaptcha(proxy):
    """Request captcha solving via 2Captcha."""
    try:
        captcha_request = {
            'key': CAPTCHA_API_KEY,
            'method': 'hcaptcha',
            'sitekey': HCAPTCHA_SITE_KEY,
            'pageurl': FAUCET_ENDPOINT,
            'json': 1
        }
        print(Fore.YELLOW + "Requesting captcha solution from 2Captcha...")
        initial_resp = requests.get(
            'http://2captcha.com/in.php', params=captcha_request, proxies=proxy
        ).json()

        if initial_resp.get('status') != 1:
            print(Fore.RED + f"Captcha request error: {initial_resp.get('request')}")
            return None

        captcha_id = initial_resp.get('request')
        print(Fore.GREEN + f"Captcha ID obtained: {captcha_id}")

        solution_request = {
            'key': CAPTCHA_API_KEY,
            'action': 'get',
            'id': captcha_id,
            'json': 1
        }
        time.sleep(10)

        while True:
            solution_resp = requests.get(
                'http://2captcha.com/res.php', params=solution_request, proxies=proxy
            ).json()

            if solution_resp.get('status') == 1:
                print(Fore.GREEN + "Captcha solved successfully.")
                return solution_resp.get('request')
            elif solution_resp.get('request') == 'CAPCHA_NOT_READY':
                print(Fore.YELLOW + "Captcha still pending...")
                time.sleep(5)
            else:
                print(Fore.RED + f"Captcha error: {solution_resp.get('request')}")
                return None
    except requests.RequestException as e:
        print(Fore.RED + f"Network error solving captcha: {e}")
        return None

def claim_faucet(wallet, captcha_token, proxy):
    """Claim the faucet using provided details."""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Origin': 'https://hub.0g.ai',
        'Referer': 'https://hub.0g.ai/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
    }

    payload = {
        'address': wallet,
        'hcaptchaToken': captcha_token,
        'token': 'A0GI'
    }

    print(Fore.CYAN + f"Submitting faucet claim for wallet {wallet}...")
    try:
        resp = requests.post(
            FAUCET_ENDPOINT, json=payload, headers=headers, proxies=proxy
        )

        if resp.ok:
            result = resp.json()
            tx_hash = result.get('message')
            if tx_hash:
                explorer_url = f"https://chainscan-newton.0g.ai/tx/{tx_hash}"
                print(Fore.GREEN + f"Successfully claimed faucet! Transaction link: {explorer_url}")
                with open('log.txt', 'a') as log:
                    log.write(f"{wallet},{mask_proxy(proxy['http'])},{tx_hash},{explorer_url}\n")
                return True
            else:
                print(Fore.RED + "Transaction hash missing in response.")
        else:
            print(Fore.RED + f"Failed to claim faucet: HTTP {resp.status_code} - {resp.text}")
    except requests.RequestException as e:
        print(Fore.RED + f"Network error during faucet claim: {e}")
    return False

def main_process():
    wallets = read_lines('wallet.txt')

    try:
        with open("wallets.json") as f:
            wallets_json = json.load(f)
            addrs = [w['address'] for w in wallets_json][::-1]
            wallets.extend(addrs)
    except:
        pass

    proxies_raw = read_lines('proxy.txt')[::-1]

    wallets_len = len(proxies_raw)
    wallets = wallets[0:wallets_len]

    if len(wallets) != len(proxies_raw):
        print(Fore.RED + "Number of wallets and proxies must be equal.")
        return

    for idx, wallet in enumerate(wallets):
        proxy_str = proxies_raw[idx]
        try:
            proxy = format_proxy(proxy_str)
        except ValueError as e:
            print(Fore.RED + str(e))
            continue

        attempts = 0
        while attempts < MAX_RETRY:
            print(Fore.YELLOW +
                  f"\nProcessing wallet [{idx + 1}/{len(wallets)}]: {wallet} | Proxy: {mask_proxy(proxy_str)} | Attempt: {attempts + 1}")

            captcha_solution = solve_hcaptcha(proxy)
            if captcha_solution:
                if claim_faucet(wallet, captcha_solution, proxy):
                    break
                else:
                    attempts += 1
                    if attempts < MAX_RETRY:
                        print(Fore.YELLOW + "Retrying faucet claim...")
                        time.sleep(REQUEST_DELAY)
            else:
                print(Fore.RED + "Skipping wallet due to captcha failure.")
                break

        time.sleep(REQUEST_DELAY)

if __name__ == "__main__":
    main_process()
