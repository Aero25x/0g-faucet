[![Join our Telegram RU](https://img.shields.io/badge/Telegram-RU-03A500?style=for-the-badge&logo=telegram&logoColor=white&labelColor=blue&color=red)](https://t.me/hidden_coding)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/aero25x)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=x&logoColor=white)](https://x.com/aero25x)
[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@flaming_chameleon)
[![Reddit](https://img.shields.io/badge/Reddit-FF3A00?style=for-the-badge&logo=reddit&logoColor=white)](https://www.reddit.com/r/HiddenCode/)
[![Join our Telegram ENG](https://img.shields.io/badge/Telegram-EN-03A500?style=for-the-badge&logo=telegram&logoColor=white&labelColor=blue&color=red)](https://t.me/hidden_coding_en)

# 0G Faucet Automation

An automated script designed to simplify claiming tokens from the 0G Faucet, solving hCaptcha using 2Captcha integration, and supporting proxies with authentication.

## Features

- Automated hCaptcha solving via 2Captcha
- Proxy support including authenticated proxies (`ip:port:user:pass`)
- Automatic logging of successful claims with transaction URLs
- Flexible wallet address configuration (supports both `.txt` and `.json` wallet files)

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/0g-faucet-automation.git
cd 0g-faucet-automation
```

### Install Dependencies

```bash
pip install requests colorama
```

## Configuration

Before running, configure the following:

### 1. `wallet.txt`
Add wallet addresses, one per line:

```text
0xYourWalletAddress1
0xYourWalletAddress2
```

### 2. `proxy.txt`
Proxies must be in the following formats:

- IP without authentication:

```text
192.168.1.100:8080
```

- IP with authentication:

```text
185.171.255.72:6125:hxjsvept:3pzgwox5suvu
```

### 3. Wallet JSON (Optional)
To load wallets from a JSON file, create `wallets.json`:

```json
[
    {"address": "0xYourWalletAddress3"},
    {"address": "0xYourWalletAddress4"}
]
```

Wallet addresses from `wallets.json` will be added to those from `wallet.txt`.

### 4. Update `CAPTCHA_API_KEY` and `HCAPTCHA_SITE_KEY` in `main.py`

Replace placeholders with your actual keys:

```python
CAPTCHA_API_KEY = 'Your_2Captcha_API_Key'
HCAPTCHA_SITE_KEY = 'Target_Site_hCaptcha_Sitekey'
```

## Running the Script

Execute:

```bash
python main.py
```

### Example Run:

```
Processing wallet [1/2]: 0xYourWalletAddress1 | Proxy: 185.171.255.72:****:****:**** | Attempt: 1
Requesting captcha solution from 2Captcha...
Captcha ID obtained: 1234567890
Captcha solved successfully.
Submitting faucet claim for wallet 0xYourWalletAddress1...
Successfully claimed faucet! Transaction link: https://chainscan-newton.0g.ai/tx/transaction_hash_here
```

## Logs

Successful claims are logged in `log.txt`:

```
0xYourWalletAddress1,185.171.255.72:****:****:****,transaction_hash_here,https://chainscan-newton.0g.ai/tx/transaction_hash_here
```

## Contribution

Feel free to contribute by opening issues or pull requests.

## Disclaimer

Use responsibly. The developer is not responsible for any misuse of this script.
[![Join our Telegram RU](https://img.shields.io/badge/Telegram-RU-03A500?style=for-the-badge&logo=telegram&logoColor=white&labelColor=blue&color=red)](https://t.me/hidden_coding)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/aero25x)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=x&logoColor=white)](https://x.com/aero25x)
[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@flaming_chameleon)
[![Reddit](https://img.shields.io/badge/Reddit-FF3A00?style=for-the-badge&logo=reddit&logoColor=white)](https://www.reddit.com/r/HiddenCode/)
[![Join our Telegram ENG](https://img.shields.io/badge/Telegram-EN-03A500?style=for-the-badge&logo=telegram&logoColor=white&labelColor=blue&color=red)](https://t.me/hidden_coding_en)


