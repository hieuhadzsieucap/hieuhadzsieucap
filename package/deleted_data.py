from flask import Flask
from models import *  # import file models.py previously created

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:hieu05112003@localhost:5432/website_ban_hang"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)  # tie db with flask app


def main():
    list_table = [Cart, Product, Receipt, Customer]
    for index in list_table:
        datas = index.query.all()
        for data in datas:
            db.session.delete(data)
            db.session.commit()

if __name__ == "__main__":
    with app.app_context():  # allow developer interact with flask via command line
        main()
