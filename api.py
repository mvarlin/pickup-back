import configparser
import MySQLdb.cursors
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, ForeignKey, func
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import Date, Integer, Text

config = configparser.ConfigParser()
config.read('config.ini')

MYSQL_HOST = config['mysqlDB']['host']
MYSQL_PORT = 3306
MYSQL_USER = config['mysqlDB']['user']
MYSQL_PWD = config['mysqlDB']['pass']
MYSQL_DB = config['mysqlDB']['db']
 
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
 
session = Session()
 
Base = declarative_base()

#user
class User(Base): 
    __tablename__= "user"
    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    mail = Column(Date, unique=True, nullable=False)
    birth_date = Column(String(80), nullable=False)
    mdp = Column(Text, nullable=False)
    postal_code = Column(Integer, nullable=False)
 
def add_user(nom, prenom, mail, birth_date, mdp, postal_code):
    try:
        user = User(
        nom=nom,
        prenom=prenom,
        mail=mail,
        birth_date=birth_date,
        mdp=mdp,
        postal_code=postal_code)
        session.add(user)
        session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def get_user_by_id(id):
    try:
        result = session.query(User).filter_by(id=id).first()
        return result
    except Exception as e:
        print(e)
        return False

def update_attribute(id, attributes):
    try:
        user_to_update = get_user_by_id(id)
        if user_to_update :
            for k,v in attributes.items():
                setattr(user_to_update, k, v)
            session.commit()
            return user_to_update
        else:
            return False
    except Exception as e:
        print(e)
        return False

#category
class Category(Base): 
    __tablename__= "category"
    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    nom = Column(String(100), nullable=False)
 
def get_all_category():
    try:
        result = session.query(Category).filter_by()

        return result
    except Exception as e:
        print(e)
        return False

#category_specific
class Specific_category(Base): 
    __tablename__= "specific_category"
    id = Column(Integer, nullable=False, unique=True, primary_key=True)
    name_specific_category = Column(String(100), nullable=False)
    id_category = Column(Integer, ForeignKey('category.id'),nullable=False)
    
def get_all_specific_category():
    try:
        result = session.query(Specific_category) #.order_by(Specific_category.id_category) #join(Category.id)

        return result
    except Exception as e:
        print(e)
        return False