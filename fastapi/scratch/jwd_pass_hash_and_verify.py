import bcrypt


# Функция для хэширования пароля
def hash_password(password: str) -> str:
    pwd_bytes = password.encode()
    salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(pwd_bytes, salt)
    return hash_pwd.decode()


# Функция для сравнения планового пароля и хэша
def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_pwd_bytes = plain_password.encode()
    hashed_pwd_bytes = hashed_password.encode()
    return bcrypt.checkpw(plain_pwd_bytes, hashed_pwd_bytes)


my_password = "qwerty"
my_hash_password = hash_password(my_password)

print(f"Мой пароль: {my_password} | Хэш моего пароля: {my_hash_password}") # Мой пароль: qwerty | Хэш моего пароля: $2b$12$9QAKMTf7959E/J.tbjEur.jTGyyMduAvhYBCulZg/2ckPIWy.cnFq
print(verify_password(my_password, my_hash_password)) # True
print(verify_password("wrong_pass", my_hash_password)) # False