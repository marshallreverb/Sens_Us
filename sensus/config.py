import os


class Config:

    SECRET_KEY= os.environ.get('SECRET_KEY',"mysec")  # replace with ssl key
    SQLALCHEMY_DATABASE_URI= 'sqlite:///site.db'
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER',"tadikust@gmail.com")
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')