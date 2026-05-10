import os
import requests
import random

def get_low_entropy_seed():
    """Использование Random API (погода/числа) если системная энтропия мала."""
    try:
        # апишка для получения случайных чисел как доп. источник
        response = requests.get("https://random.org", timeout=2)
        if response.status_code == 200:
            return response.text.strip()
    except:
        return str(random.random())

def get_secure_secret():
    """Проверка энтропии на хосте (Linux) и генерация ключа."""
    entropy_val = 1000 # для винды и мака, НЕЕЕЕ Linux
    
    if os.path.exists("/proc/sys/kernel/random/entropy_avail"):
        with open("/proc/sys/kernel/random/entropy_avail", "r") as f:
            entropy_val = int(f.read().strip())
    
    if entropy_val < 200:
        print(f"[!] Низкая энтропия ({entropy_val}). Используем Random API...")
        seed = get_low_entropy_seed()
        random.seed(seed)
    
    # генерим рандомную строку для секрета
    import pyotp
    return pyotp.random_base32()
