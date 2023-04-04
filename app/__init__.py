from flask import Flask
# from models import User
# from os import path
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base


    
    

app = Flask(__name__)
engine = create_engine('mysql://gutowski:C7xTrPPcz8XefYnt@mysql.agh.edu.pl/gutowski')
Base = declarative_base()
Base.metadata.reflect(engine)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    # example of usage for debugging purpose and future users
    # db_session = scoped_session(sessionmaker(bind=engine))
    # for item in db_session.query(User.Username):
        # print(item)
    app.run(debug=True)
