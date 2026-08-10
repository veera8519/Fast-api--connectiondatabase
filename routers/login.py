

from warnings import deprecated

from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from idna import encode
from product import schema,models

from database import get_db

from passlib.context import CryptContext

from sqlalchemy.orm import Session

from datetime import timedelta,datetime

from jose import JWTError,jwt

from product.schema import TokenData


router=APIRouter()

SECRET_KEY='301a87465ed85d883b53e14662a51e9d759e26c1588c51f7418c511024aa8afe'
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=20

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


@router.post('/login',tags=['LOGIN'])
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    seller=db.query(models.Seller).filter(models.Seller.username==request.username).first()
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user NOT FOUND")
    if not pwd_context.verify(request.password,seller.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="PASSWORD NOT FOUND")  

    access_token = create_access_token(
        data={"sub": seller.username}
    )
    return {'access_token':access_token,"token_type":"bearer"}

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt
