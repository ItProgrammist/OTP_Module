import os
import hashlib
import pyotp
from core.entropy import get_secure_secret

def hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(16).hex()
    pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return pwd_hash, salt

def register_user(username, password, db):
    if username in db:
        return None, "Пользователь уже существует"
    
    pwd_hash, salt = hash_password(password)
    totp_secret = get_secure_secret() # бонусики для генерации TOTP-секрета с учетом энтропии
    
    db[username] = {
        "hash": pwd_hash,
        "salt": salt,
        "totp_secret": totp_secret
    }
    return totp_secret, "Регистрация успешна"

def verify_login(username, password, otp_code, db):
    user = db.get(username)
    if not user:
        return False, "Пользователь не найден"
    
    # чекаем хеша пароля
    check_hash, _ = hash_password(password, user["salt"])
    if check_hash != user["hash"]:
        return False, "Неверный пароль"
    
    # чекаем TOTP
    totp = pyotp.TOTP(user["totp_secret"])
    if totp.verify(otp_code):
        return True, "Успешный вход!"
    else:
        return False, "Неверный OTP-код (истек или ошибочен)"
