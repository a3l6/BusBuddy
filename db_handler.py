import sqlalchemy.exc
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from exceptions import UserAlreadyExists, IncorrectCredentials
from dotenv import load_dotenv
import os
from argon2 import PasswordHasher
import password_hasher as ph


load_dotenv()

# Must be at top of file before classes or anything is loaded
# Prevent some error, I forget
Base = declarative_base()

# Create tables
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    address = Column(String, nullable=False)
    school = Column(String, nullable=False)

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    school = Column(String, nullable=False)

class db_handler:
    @staticmethod
    def register(name: str, email: str, password: str, address: str, school: str):
        try: 
            hashed_passw = ph.hash_pw(password, email)
            user = User(name=name, email=email, password=hashed_passw, account_type="parent", address=address, school=school)
            session.rollback()
            session.add(user)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise UserAlreadyExists("User already exists!", status_code=422)
        return True   # "User Added Successfully"

    @staticmethod
    def admin_register(name: str, email: str, password: str, school: str):
        try: 
            hashed_passw = ph.hash_pw(password, email)
            admin = Admin(name=name, email=email, password=hashed_passw, account_type="admin", school=school)
            session.rollback()
            session.add(admin)
            session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            raise UserAlreadyExists("User already exists!", status_code=422)
        return True   # "User Added Successfully"

    @staticmethod
    def admin_login(email: str, password: str):
        try:
            cursor = session.query(Admin).filter(Admin.email == email)
            for user in cursor:
                print(user.password, str(user.password))
                if ph.verify(user.password, password, email):
                    return True   # "Successfully authenticated"
                raise IncorrectCredentials("Incorrect Credentials")
            raise IncorrectCredentials("Incorrect Credentials")
        except UnboundLocalError:       # No user found
            print("No user found")
            raise IncorrectCredentials("Incorrect Credentials")


    @staticmethod
    def login(email: str, password: str):
        try:
            cursor = session.query(User).filter(User.email == email)
            for user in cursor:
                print(user.password, str(user.password))
                if ph.verify(user.password, password, email):
                    return True   # "Successfully authenticated"
                raise IncorrectCredentials("Incorrect Credentials")
            raise IncorrectCredentials("Incorrect Credentials")
        except UnboundLocalError:       # No user found
            print("No user found")
            raise IncorrectCredentials("Incorrect Credentials")

        



# Sqlalchemy boilerplate
# Generating sqlalchemy stuff
engine = create_engine(os.getenv("DB_URL"))
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()