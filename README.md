# goit_web_hw12
# JSON Web Token
1. poetry shell
2. start docker container with postgres SQL
   and created BD web_hw11
3. alembic upgrade head
4. # (optional) 
   py goit_web_hw12/database/seeds.py
   # - to fill the database with fake data
5. py main.py
6. uvicorn main:app --host localhost --port 8000 --reload
7. http://127.0.0.1:8000/docs

# В базі наявні 3 users та більше 50 контактів
# user                 pasword
  taras@example.com    taras09
  olena@example.com    olena11
  olaf@example.com     viking