import os
from storage.db_mock import load_db, save_db
from core.auth import register_user, verify_login

def main():
    db = load_db()
    print("=== Система авторизации Password + TOTP ===")
    
    while True:
        choice = input("\n1. Регистрация\n2. Вход\n3. Выход\nВыберите действие: ")
        
        if choice == '1':
            user = input("Придумайте логин: ")
            pwd = input("Придумайте пароль: ")
            secret, msg = register_user(user, pwd, db)
            if secret:
                save_db(db)
                print(f"{msg}. ВАШ СЕКРЕТНЫЙ КЛЮЧ: {secret}")
                print("Добавьте его в Google Authenticator или используйте для генерации кодов.")
            else:
                print(f"Ошибка: {msg}")

        elif choice == '2':
            user = input("Логин: ")
            pwd = input("Пароль: ")
            otp = input("Введите 6-значный код TOTP: ")
            success, msg = verify_login(user, pwd, otp, db)
            print(msg)

        elif choice == '3':
            break

if __name__ == "__main__":
    main()
