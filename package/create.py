from flask import Flask
from models import *  # import file models.py previously created

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:0511@localhost:5432/website_ban_hang"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)  # tie db with flask app


def main():
    db.create_all()
    products = Product.query.all()
    product_id = str(len(products) + 1)
    product_1 = Product(product_id = product_id, product_name = "Samsung S22 Ultra", origin = "Samsung", price = "29.190.000", quantity = 100, link_img = "https://bom.so/YgPmWe")
    product_id = int(product_id) + 1
    product_2 = Product(product_id = str(product_id), product_name = "Iphone 13 Pro max", origin = "Apple", price = "28.990.000", quantity = 100, link_img = "https://bom.so/dNZLeg")
    product_id = int(product_id) + 1
    product_3 = Product(product_id = str(product_id), product_name = "Redmi Note 10 Pro", origin = "Redmi", price = "7.490.000", quantity = 100, link_img = "https://bom.so/vM9E2a")
    product_id = int(product_id) + 1
    product_4 = Product(product_id = str(product_id), product_name = "Vsmart Joy 4", origin = "Vsmart", price = "3.290.000", quantity = 100, link_img = "https://bom.so/T68hLk")
    product_id = int(product_id) + 1
    product_5 = Product(product_id = str(product_id), product_name = "OPPO A16", origin = "OPPO", price = "3.790.000", quantity = 100, link_img = "https://bom.so/RCkDBo")
    product_add_list = [product_1, product_2, product_3, product_4, product_5]

    for product in products:
        for new_product in product_add_list:
            if product.product_id == new_product.product_id:
                product_add_list.remove(new_product)
                break
    for new_product in product_add_list:
        db.session.add(new_product)
    db.session.commit()

    
if __name__ == "__main__":
    with app.app_context():  # allow developer interact with flask via command line
        main()

# more products
# =====================
# APPLE WATCH SERIES 7
# 9.599.000
# 50
# Apple 
# https://bom.so/UYxexT
# =====================
# GALAXY Z FLIP 3
# 19.989.123
# 123
# Samsung
# https://bom.so/6vcig0