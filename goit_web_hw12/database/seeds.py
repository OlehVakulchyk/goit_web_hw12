from random import randint, choice
from faker import Faker

from models import UserContact
from db import SessionLocal

 # Создаем объект библиотеки Faker. В качестве параметра передаем local 'uk-UA'
    # Больше - https://faker.readthedocs.io/en/master/locales.html
fake = Faker('uk-UA')
NUMBER_OF_USERS = 50

def seed_users():
        db = SessionLocal()
        for i in range(NUMBER_OF_USERS):
            phone_1 = str('+380(' + str(randint(10,99)) + ')' + 
                          str(randint(100,999)) + '-' + 
                          str(randint(10,99)) + '-' + 
                          str(randint(10,99)))
            phone_2 = str('+380(' + str(randint(10,99)) + ')' + 
                          str(randint(100,999)) + '-' + 
                          str(randint(1,9)) + '-' +
                          str(randint(100,999)))
            contact = UserContact(
                  name = fake.first_name(),
                  surname = fake.last_name(),
                  email = fake.email(),
                  phone = choice([phone_1, phone_2]),
                  bithday = fake.date(),
                  user_id = choice([1,2,3]),
                  information = str(i)
                  )
            db.add(contact)
        db.commit()

if __name__ == '__main__':
    seed_users()