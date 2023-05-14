from sqlalchemy import and_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from goit_web_hw12.database.models import UserContact, User
from goit_web_hw12.schemas import ContactModel

NEXT_DAYS = 7

async def get_users(limit: int, offset: int, db: Session, user: User):
    contacts = db.query(UserContact).filter_by(user_id=user.id).limit(limit).offset(offset)
    return contacts.all()


async def get_user_by_id(contact_id: int, db: Session, user: User):
    contact = db.query(UserContact).filter(and_(UserContact.user_id==user.id, UserContact.id==contact_id)).first()
    return contact


async def get_search_users(limit: int, offset: int, 
                            db: Session, user: User,
                            contact_name: str | None = None, 
                            contact_surname: str | None = None
                            ):
    contacts = db.query(UserContact).filter_by(user_id=user.id)
    if contact_name:
        contacts = contacts.filter_by(name=contact_name)
    if contact_surname:
        contacts = contacts.filter_by(surname=contact_surname)
    return contacts.limit(limit).offset(offset).all()


async def get_users_by_bithday(limit: int, offset: int, db: Session, user: User):
    current_datetime = datetime.now().date()
    date_end_bithdays = current_datetime + timedelta(days = NEXT_DAYS)
    contacts = db.query(UserContact).filter_by(user_id=user.id).limit(limit).offset(offset).all()
    contacts_bithdays = []
    for contact in contacts:
        contact_bithday = contact.bithday
        bithday_this_year = datetime(
                current_datetime.year, 
                contact_bithday.month, 
                contact_bithday.day
                ).date()
        if current_datetime <= bithday_this_year < date_end_bithdays:
            contacts_bithdays.append(contact)
    return contacts_bithdays



async def get_users_by_email(user_email: str, db: Session, user: User):
    contact = db.query(UserContact).filter(and_(UserContact.user_id==user.id, UserContact.email==user_email)).first()
    return contact


async def create(body: ContactModel, db: Session, user: User):
    contact = UserContact(**body.dict())
    contact.user_id = user.id
    db.add(contact)
    db.commit()
    return contact


async def update(user_id: int, body: ContactModel, db: Session, user: User):
    contact = await get_user_by_id(user_id, db, user)
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.bithday = body.bithday
        contact.user_id = user.id
        contact.information = body.information
        db.commit()
    return contact


async def remove(user_id: int, db: Session, user: User):
    contact = await get_user_by_id(user_id, db, user)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
