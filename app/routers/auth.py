# routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jose import jwt
from datetime import datetime, timedelta
from .. import models, oauth2, schemas, utils, database
from sqlalchemy.orm import Session
from passlib.context import CryptContext

router = APIRouter()


@router.post("/", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token,
            "token_type": "bearer"}
