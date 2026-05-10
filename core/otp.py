import pyotp

def generate_totp_secret():
    """Генерирует новый секретный ключ в формате Base32."""
    return pyotp.random_base32()

def verify_totp_code(secret, code):
    """
    Проверяет 6-значный код. 
    valid_window=1 позволяет небольшое расхождение во времени (±30 сек).
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)

def get_current_otp(secret):
    """Вспомогательная функция для получения текущего кода (для тестов)."""
    totp = pyotp.TOTP(secret)
    return totp.now()
