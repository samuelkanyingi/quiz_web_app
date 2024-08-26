class Config:
    """
    Configuration settings from the flask application 
    """
    SECRET_KEY = 'sammy'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/quiz_db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'samuelkanyingi2016@gmail.com'
    MAIL_PASSWORD= 'tkih fuut pegn eyuw'
    MAIL_USE_TLS = True #secure connecttion
    MAIL_USE_SSL = False #less secure connection