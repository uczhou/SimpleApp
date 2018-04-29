
db_addr = '<addr>:<port>'
db_user = '<user>'
db_pwd = '<password>'
db_name = 'testDB'
SECRET_KEY = 'super secret key'
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(db_user, db_pwd, db_addr, db_name)
SQLALCHEMY_TRACK_MODIFICATIONS = False