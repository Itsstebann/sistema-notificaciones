from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, Token
import app.auth as auth

router = APIRouter(prefix="/auth", tags=["Autenticación"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = auth.verificar_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Token inválido")
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return usuario


@router.post("/registro", response_model=UsuarioResponse)
def registro(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existe = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    nuevo = Usuario(
        email=usuario.email,
        password=auth.hashear_password(usuario.password)
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == form.username).first()
    if not usuario or not auth.verificar_password(form.password, usuario.password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = auth.crear_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}
