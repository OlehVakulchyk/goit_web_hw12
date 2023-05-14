from typing import Annotated
from pydantic import EmailStr
from fastapi import APIRouter, Depends, HTTPException, Path, status, Query
from sqlalchemy.orm import Session

from goit_web_hw12.database.db import get_db
from goit_web_hw12.database.models import User
from goit_web_hw12.schemas import ContactResponse, ContactModel
from goit_web_hw12.repository import contacts as repository_users
from goit_web_hw12.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["users"])


@router.get("/", response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(10, le=300), offset: int = 0, 
                    db: Session = Depends(get_db), 
                    user: User = Depends(auth_service.get_current_user)):
    users = await repository_users.get_users(limit, offset, db, user)
    return users


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(user_id: int = Path(ge=1), 
                   db: Session = Depends(get_db),
                   user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.get_user_by_id(user_id, db, user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Not found!")
    return user


@router.get("/search_contacts/", response_model=list[ContactResponse])
async def search_contacts(limit: Annotated[int, Query(le=50)] = 10, 
                            offset: int = 0, 
                            db: Session = Depends(get_db),
                            user: User = Depends(auth_service.get_current_user),
                            user_name: Annotated[str | None, 
                                                 Query(description="""_may be empty_ 
                                                 **---to get all users, the following fields must be empty---**""", 
                                                       max_length=20)] = None, 
                            user_surname: Annotated[str | None, 
                                                    Query(description='may be empty', 
                                                          max_length=30)] = None                            
                            ):
    users = await repository_users.get_search_users(limit, 
                                                     offset, 
                                                     db, user,
                                                     user_name,
                                                     user_surname
                                                     )
    return users


@router.get("/contacts_by_email/", response_model=ContactResponse)
async def get_contacts_by_email(user_email: EmailStr,  
                            db: Session = Depends(get_db),
                            user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.get_users_by_email(user_email, db, user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Not found!")
    return user


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.create(body, db, user)
    return user


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, user_id: int = Path(ge=1), 
                      db: Session = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    contact = await repository_users.update(user_id, body, db, user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Not found!")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(user_id: int = Path(ge=1), 
                      db: Session = Depends(get_db),
                      user: User = Depends(auth_service.get_current_user)):
    user = await repository_users.remove(user_id, db, user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Not found!")
    return None


@router.get("/bithday_next_days/", 
            response_model=list[ContactResponse])
async def get_contacts_by_bithday(limit: int = Query(10, le=300), 
                               offset: int = 0, 
                               db: Session = Depends(get_db),
                               user: User = Depends(auth_service.get_current_user)):
    users = await repository_users.get_users_by_bithday(limit, 
                                                        offset, 
                                                        db, user)
    return users
