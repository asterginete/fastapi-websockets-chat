from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.connection import ConnectionManager
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models import User, UserInDB, Token, TokenData
from typing import Optional
from jwt import JWTError

app = FastAPI()
connection_manager = ConnectionManager()

# OAuth2 token endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mock database for demonstration purposes
users_db = {"alice": {"username": "alice", "hashed_password": get_password_hash("secret")}}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(users_db, form_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}

@app.websocket("/ws/{username}/")
async def websocket_endpoint(websocket: WebSocket, username: str, current_user: User = Depends(get_current_user)):
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.broadcast(f"{username}: {data}")
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        await connection_manager.broadcast(f"{username} left the chat")
