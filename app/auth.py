from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30


def hashear_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verificar_password(password: str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))


def crear_token(data: dict) -> str:
    datos = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    datos.update({"exp": expiracion})
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None
