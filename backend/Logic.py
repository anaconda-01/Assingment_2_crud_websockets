from sqlalchemy.orm import Session
from Modle import UserDB, RoleDB


def append_data(UserDB, RolesDB, username: str, email: str, password: str, role_name: str, db: Session):
    user_data = UserDB(username=username, email=email, password=password)
    db.add(user_data)
    db.commit()
    db.refresh(user_data)
    u_id = user_data.user_id
    
    role_data = RolesDB(user_id=u_id, role_name=role_name)
    db.add(role_data)
    db.commit()
    
    return user_data, role_data

def get_data_all(db: Session, UserDB, RoleDB, username: str):
    user = db.query(UserDB).filter(UserDB.username == username).first()   
    if user:
        return {"user": user}
    else:
        return {"message": "User not found"}
    
def update_user(db:Session,UserDB, user_id: int, username: str = None, email: str = None, password: str = None, ):
    user = db.query(UserDB).filter(UserDB.user_id == user_id).first()
    
    if user:
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = password
        
        db.commit()
        db.refresh(user)
        return user
    else:
        return {"message": "User not found"}


def update_role(RoleDB, user_id: int, role_name: str, db: Session):
    role = db.query(RoleDB).filter(RoleDB.user_id == user_id).first()

    if role:
        role.role_name = role_name
        db.commit()
        db.refresh(role)
        return role
    else:
        return {"message": "Role not found for this user"}
def delete_user_and_role(UserDB, RoleDB, user_id: int, db: Session):

    user = db.query(UserDB).filter(UserDB.user_id == user_id).first()
    if user:

        role = db.query(RoleDB).filter(RoleDB.user_id == user_id).first()
        if role:
            db.delete(role)
            db.commit()
            
        db.delete(user)
        db.commit()
        return {"message": "User and associated role deleted successfully"}
    else:
        return {"message": "User not found"}
