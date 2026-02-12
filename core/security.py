import os 
from passlib.context import CryptContext
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

# cargamos las variables de entorno
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN = int(os.getenv('ACCESS_TOKEN'))

# configurar bcryt 
password_context = CryptContext(schemes=["argon2"], deprecated="auto")

# funcion para hashear el password
def hash_password(password: str):
    return password_context.hash(password)

# funcion para verificar el password
def verify_password(plaintext_password: str, hashed_password: str):
    return password_context.verify(plaintext_password, hashed_password)

# funcion para crear el token
def create_token(data: dict):
    datacopy_to_enconde = data.copy()
    # expiracion del token
    expire =datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN)
    #actualizamos el dict con la fecha expiracion
    datacopy_to_enconde.update({'expire': int(expire.timestamp())})
    # codificar token
    return jwt.encode(datacopy_to_enconde, SECRET_KEY, algorithm=ALGORITHM)

# funcion decodificar el token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except JWTError:
        return None