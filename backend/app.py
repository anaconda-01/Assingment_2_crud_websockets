from fastapi import FastAPI, Request, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import Modle
import Logic
from Database import get_db, create_table
import os
from socket_server import sio, socketio  


# Initialize FastAPI application
app = FastAPI()

origins = [
    "http://localhost:8000",  # Allow localhost:8000 for API
    "http://127.0.0.1:8000",  # Allow 127.0.0.1:8000 for API
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow both localhost and 127.0.0.1 as origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Set the templates directory
template = Jinja2Templates(directory=os.path.join(os.pardir, "frontend/templates"))

# Database setup and app startup
ct = ""
@app.on_event("startup")
def startup():
    global ct
    ct = create_table(Modle.Base)

# Home page route
@app.get("/")
def index(request: Request):
    return template.TemplateResponse("index.html", {"request": request})

# Login post route
@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    # Fetch user data based on username
    user_data = Logic.get_data_all(db, Modle.UserDB, Modle.RoleDB, username)
    
    if user_data["user"]:
        if user_data["user"].password == password:
            message = "Login successful"
        else:
            message = "Incorrect password"
    else:
        message = "User not found"
    
    return template.TemplateResponse("index.html", {"request": request, "message": message})

# Get user data route
@app.get("/get_data/{username}")
async def get_user_data(username: str, request: Request, db: Session = Depends(get_db)):
    data = Logic.get_data_all(db, Modle.UserDB, Modle.RoleDB, username)
    if "message" in data:
        raise HTTPException(status_code=404, detail=data["message"])
    return {"data": data}

# Append user data route
@app.post("/append_data/")
async def append_data(username: str, email: str, password: str, role_name: str, db: Session = Depends(get_db)):
    if not username or not email or not password or not role_name:
        raise HTTPException(status_code=400, detail="All fields are required.")

    user_data, role_data = Logic.append_data(Modle.UserDB, Modle.RoleDB, username, email, password, role_name, db)
    return JSONResponse({
        "data": {
            "username": user_data.username,
            "user_id": user_data.user_id,
            "role": role_data.role_name,
        }
    })

# Update user data route
@app.put("/update_data/{user_id}")
async def update_data(user_id: int, username: str = None, email: str = None, password: str = None, db: Session = Depends(get_db)):
    user = db.query(Modle.UserDB).filter(Modle.UserDB.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.password = password

    db.commit()
    db.refresh(user)
    return {"message": "User updated successfully", "user": {"user_id": user.user_id, "username": user.username, "email": user.email}}

# Delete user data route
@app.delete("/delete_data/{user_id}")
async def delete_data(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Modle.UserDB).filter(Modle.UserDB.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    db.query(Modle.RoleDB).filter(Modle.RoleDB.user_id == user_id).delete()
    db.delete(user)
    db.commit()
    return {"message": "User and associated roles deleted successfully"}

# Initialize Socket.IO and wrap FastAPI app with Socket.IO
my_app = socketio.ASGIApp(sio,app)  # Wrap Socket.IO with ASGIApp

# Run the app using Uvicorn
if __name__ == "__main__":
    uvicorn.run(my_app, host="127.0.0.1", port=8000)
