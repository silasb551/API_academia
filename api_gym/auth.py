from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

usuarios_temporarios = {
    "usuario1": "senha1",
    "usuario2": "senha2",
    "usuario3": "senha3"
}

SECRET_KEY = "key123"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Função para criar o token JWT com o username
def criar_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para verificar credenciais com usuários temporários
def verificar_credenciais(username: str, password: str):
    if username in usuarios_temporarios and usuarios_temporarios[username] == password:
        return {"username": username}
    return None

# Função para verificar o token JWT
def verificar_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = verificar_credenciais(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Nome de usuário ou senha incorretos"
        )
    token_data = {"sub": user["username"]}
    token = criar_token(token_data)
    return {"access_token": token, "token_type": "bearer"}





