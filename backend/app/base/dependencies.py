from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from backend.app.database import get_db
from backend.app.base.models.user import User
from backend.app.base.models.group import Group
from backend.app.base.models.group_access_right import GroupAccessRight
from backend.app.base.models.access_right import AccessRight
from backend.app.base.models.user_group import UserGroup
from backend.app.base.schemas.token import TokenData
from backend.app.base.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

def has_permission(model_name: str, permission_type: str):
    def permission_checker(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        access_right = db.query(AccessRight).filter(AccessRight.name == model_name).first()
        if not access_right:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Access right for model {model_name} not found")

        for user_group in current_user.groups:
            group = user_group.group
            for group_access_right in group.access_rights:
                if group_access_right.access_right_id == access_right.id:
                    if permission_type == "read" and group_access_right.can_read:
                        return True
                    if permission_type == "create" and group_access_right.can_create:
                        return True
                    if permission_type == "update" and group_access_right.can_update:
                        return True
                    if permission_type == "delete" and group_access_right.can_delete:
                        return True
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to {permission_type} {model_name}")
    return permission_checker
