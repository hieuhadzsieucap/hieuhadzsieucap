from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = "Product"
    product_id = db.Column(db.String, primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    origin = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    link_img = db.Column(db.String, nullable=False)


class Cart(db.Model):
    __tablename__ = "Cart"
    product_id = db.Column(db.String, db.ForeignKey(
        Product.product_id), primary_key=True)
    product_name = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    link_img = db.Column(db.String, nullable=False)


class Receipt(db.Model):
    __tablename__ = "Receipt"
    receipt_id = db.Column(db.String, primary_key=True)
    product_id = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    quantity = db.Column(db.String, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)


class Customer(db.Model):
    __tablename__ = "Customer"
    customer_id = db.Column(db.String, primary_key=True)
    receipt_id = db.Column(db.String, nullable=False)
    customer_name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)

