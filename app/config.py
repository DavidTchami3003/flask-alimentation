from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY=os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SESSION_TYPE='filesystem'
    SESSION_PERMANENT=False
    
