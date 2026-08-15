from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_TOKEN = "my-secret-token"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_token(data: dict) -> str:
    data_copy = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_copy.update({"exp": expire})
    encoded_jwt = jwt.encode(data_copy, SECRET_TOKEN, ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> str:
    try:
        decoded_token = jwt.decode(token, SECRET_TOKEN, ALGORITHM)
        return decoded_token
    except JWTError:
        return None


my_encoded_token = create_token({"name": "Sasha", "age": 22})
print(my_encoded_token) # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiU2FzaGEiLCJhZ2UiOjIyLCJleHAiOjE3ODY4MTUwODZ9.5ZN8Qmu0t_ovc2jVNbk9qTQ0Gyd4PX6LUMtJmLspHs4

my_decoded_token = decode_token(my_encoded_token)
my_wrong_decoded_token = decode_token("qwerty.uiop.asdfg")
print(my_decoded_token) # {'name': 'Sasha', 'age': 22, 'exp': 1786815247}
print(my_wrong_decoded_token) # None