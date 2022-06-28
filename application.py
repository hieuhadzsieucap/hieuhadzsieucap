from flask import Flask, render_template, request
from package.models import *
from package.convert import convert_str_to_int, convert_int_to_str
from sqlalchemy import or_
# convert_str_to_int use for convert price of product from string to interger to calculate
# convert_int_to_str use for convert the value after calculate from interger to string to display

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:hieu05112003@localhost:5432/Project_final_python"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def home():
    products = Product.query.all()
    origins = []  # empty list which take origin of product then count them so that every origin appear 1 time
    for product in products:
        origins.append(product.origin)

    for origin in origins:
        number_of_origin = origins.count(origin)
        if number_of_origin > 1:
            origins.remove(origin)

    return render_template("1_home.html", products = products, origins = origins)


@app.route("/warehouse")
def warehouse():
    request_minus = request.args.get("minus")
    request_add = request.args.get("add")
    request_delete = request.args.get("button delete")
    infor_product_minus = Product.query.get(request_minus)
    infor_product_add = Product.query.get(request_add)
    infor_product_delete = Product.query.get(request_delete)

    if request_minus != None:
        infor_product_minus.quantity -= 1
        db.session.commit()

    if request_add != None:
        infor_product_add.quantity += 1
        db.session.commit()

    if request_delete != None:
        db.session.delete(infor_product_delete)
        db.session.commit()

    products = Product.query.all()

    return render_template("2_warehouse.html", products = products)


@app.route("/add_to_warehouse")
def add_to_warehouse():
    products = Product.query.all()
    request_name = request.args.get("product_name")
    request_price = request.args.get("price")
    request_quantity = request.args.get("quantity")
    request_origin = request.args.get("origin")
    request_link = request.args.get("link")

    product = Product(product_id = len(products) + 1, product_name = request_name, origin = request_origin,
                      price = request_price, quantity = request_quantity, link_img = request_link)

    db.session.add(product)
    db.session.commit()
    products = Product.query.all()  # load all products again

    return render_template("2_warehouse.html", products = products)


@app.route("/search_by_origin")
def search_by_origin():
    products = Product.query.all()

    # take request then search by filter origin of product = origin of request
    request_filter_origin = request.args.get("filter origin")
    products_display = Product.query.filter_by(
        origin = request_filter_origin).all()
    origins = []

    for product in products:
        origins.append(product.origin)

    for origin in origins:
        number_of_origin = origins.count(origin)
        if number_of_origin > 1:
            origins.remove(origin)

    return render_template("1_home.html",  products = products_display, origins = origins)


@app.route("/add_to_cart")
def add_to_cart():
    products = Product.query.all()
    product_id_request = request.args.get("button add")
    product_infor = Product.query.get(product_id_request)

    origins = []
    for product in products:
        origins.append(product.origin)

    for origin in origins:
        number_of_origin = origins.count(origin)
        if number_of_origin > 1:
            origins.remove(origin)

    # check the product has already exist if it is not None(mean product has been added) the number of products plus 1
    if Cart.query.get(product_id_request) is not None:
        product = Cart.query.get(product_id_request)
        product.quantity += 1
        db.session.commit()
    else:
        infor_product_add = Cart(product_id = product_infor.product_id, product_name = product_infor.product_name,
                                 price = product_infor.price, quantity = 1, link_img = product_infor.link_img)
        db.session.add(infor_product_add)
        db.session.commit()

    return render_template("1_home.html",  products = products, origins = origins)


@app.route("/cart")
def cart():
    # each time button is pressed, the sever recive the id of product beacuse(the button carries the id of the product)
    request_minus = request.args.get("minus")
    request_add = request.args.get("add")
    request_delete = request.args.get("button delete")
    infor_product_minus = Cart.query.get(request_minus)
    infor_product_add = Cart.query.get(request_add)
    infor_product_delete = Cart.query.get(request_delete)

    # code below check which button user pressed and processing user request
    if request_minus != None:
        infor_product_minus.quantity -= 1
        db.session.commit()
    if request_add != None:
        infor_product_add.quantity += 1
        db.session.commit()
    if request_delete != None:
        db.session.delete(infor_product_delete)
        db.session.commit()

    product_sanpham = Product.query.all()
    products = Cart.query.all()
    total_price = 0

    # reload templates and delete product if quantity of product in cart = 0
    for product in products:
        if product.quantity == 0:
            db.session.delete(product)
            db.session.commit()
            return render_template("1_home.html", products = product_sanpham)

        total_price += (convert_str_to_int(product.price) * product.quantity)

    return render_template("3_cart.html", products = products, total_price = convert_int_to_str(total_price))


# the router use for display products in user cart, the amount user has to pay and the form for user fill out
@app.route("/pay")
def pay():
    products = Cart.query.all()
    number_of_product = 0
    total_price = 0

    for product in products:
        number_of_product += product.quantity
        total_price += (convert_str_to_int(product.price) * product.quantity)

    return render_template("4_pay.html", products = products, number_of_product = number_of_product, total_price = convert_int_to_str(total_price))


# the router add information of user and they purchase to the table customer and table receipt
@app.route("/bill")
def bill():
    # creater the receipt_id
    receipts = Receipt.query.all()
    receipt_id = 0

    if receipts == []:
        receipt_id = "1"
    else:
        receipt_id = str(int(receipts[len(receipts) - 1].receipt_id) + 1)

    # add user purchase to the table Receipt
    products = Cart.query.all()
    list_product_id = []
    list_price = []
    list_product_quantity = []
    total_price = 0

    for product in products:
        total_price += (convert_str_to_int(product.price) * product.quantity)

    for product in products:
        list_product_id.append(product.product_id)
        list_price.append(product.price)
        list_product_quantity.append(str(product.quantity))

    product_id = '/'.join(list_product_id)
    price = '/'.join(list_price)
    quantity = '/'.join(list_product_quantity)

    infor_receipt = Receipt(receipt_id = receipt_id, product_id = product_id, price = price,
                            quantity = quantity, total_price = total_price)
    db.session.add(infor_receipt)
    db.session.commit()

    request_gender = request.args.get("input_gender")
    request_name = request.args.get("input_name")
    request_phone = request.args.get("input_phone")
    request_address = request.args.get("input_address")
    customers = Customer.query.all()

    # create the customer_id
    customer_id = 0
    if customers == []:
        customer_id = "1"
        # add user infomation to the table Customer
        infor_customer = Customer(customer_id = customer_id, receipt_id = receipt_id, customer_name = request_name,
                                  gender = request_gender, address = request_address, phone = request_phone)
        db.session.add(infor_customer)
        db.session.commit()
    else:
        customer_id = str(int(customers[len(customers) - 1].customer_id) + 1)

    # check customer in database
    # check by phone number customer
    for customer in customers:
        if customer.phone == request_phone:
            customer.receipt_id = customer.receipt_id + "/" + receipt_id
            db.session.commit()
            break
        else:
            infor_customer = Customer(customer_id = customer_id, receipt_id = receipt_id, customer_name = request_name,
                                      gender = request_gender, address = request_address, phone = request_phone)
            db.session.add(infor_customer)
            db.session.commit()
            break

    return render_template("5_alert.html")


# the router delete all products in cart after user payment
@app.route("/delete_product_in_cart")
def delete_product():
    products_in_cart = Cart.query.all()
    products_in_warehouse = Product.query.all()

    origins = []  # empty list which take origin of product then count them so that every origin appear 1 time
    for product in products_in_warehouse:
        origins.append(product.origin)

    for origin in origins:
        number_of_origin = origins.count(origin)
        if number_of_origin > 1:
            origins.remove(origin)

    for product in products_in_cart:
        db.session.delete(product)
        db.session.commit()

    return render_template("1_home.html",  products = products_in_warehouse, origins = origins)


# the router change and delete customers
@app.route("/customer")
def customer():
    receipts = [] # empty list carier receipt id
    list_receipts = Receipt.query.all()
    for receipt in list_receipts:
        receipts.append(receipt.receipt_id) # if user don't use filter, receipts always full

    customers = Customer.query.all()
    request_change = request.args.get("button_change")
    request_delete = request.args.get("button_delete")

    if request_change != None:
        request_gender = request.args.get("input_gender")
        request_name = request.args.get("input_name")
        request_phone = request.args.get("input_phone")
        request_address = request.args.get("input_address")

        customer_infor = Customer.query.get(request_change)

        customer_infor.customer_name = request_name
        customer_infor.gender = request_gender
        customer_infor.address = request_address
        customer_infor.phone = request_phone

        db.session.commit()
        customers = Customer.query.all()

        return render_template("6_customer.html", customers = customers, receipts = receipts)

    # delete customer and reload website
    if request_delete != None:
        infor_customer_delete = Customer.query.get(request_delete)
        db.session.delete(infor_customer_delete)
        db.session.commit()
        customers = Customer.query.all()
        return render_template("6_customer.html", customers = customers, receipts = receipts)

    return render_template("6_customer.html", customers = customers, receipts = receipts)


# the router search by filter of table customers and table receipt
@app.route("/search_by_filter_customer")
def search_by_filter_customer():
    receipts = [] # empty list carier receipt id satisfy
    request_price_less_than = request.args.get("checkbox_less_than")
    request_price_greater_than = request.args.get("checkbox_greater_than")

    if request_price_less_than and request_price_greater_than != None:
        receipts_satisfy_the_condition = Receipt.query.filter(or_(Receipt.total_price < int(request_price_less_than)
        , Receipt.total_price > int(request_price_greater_than)))
        for receipt in receipts_satisfy_the_condition:
            receipts.append(receipt.receipt_id)
    
    elif request_price_less_than != None:
        receipts_satisfy_the_condition = Receipt.query.filter(
            Receipt.total_price < int(request_price_less_than)).all()
        for receipt in receipts_satisfy_the_condition:
            receipts.append(receipt.receipt_id)
    
    elif request_price_greater_than != None:
        receipts_satisfy_the_condition = Receipt.query.filter(
            Receipt.total_price > int(request_price_greater_than)).all()
        for receipt in receipts_satisfy_the_condition:
            receipts.append(receipt.receipt_id)
    
    if receipts == []:
        list_receipts = Receipt.query.all()
        for receipt in list_receipts:
            receipts.append(receipt.receipt_id)

    customers = []  # empty list carier customers satify
    request_male = request.args.get("checkbox_male")
    request_female = request.args.get("checkbox_female")
    
    if request_male and request_female != None:
        customers = Customer.query.filter(or_(Customer.gender == "Male", Customer.gender == "Female"))
    
    elif request_male != None:
        customers = Customer.query.filter_by(gender = "Male").all()
    
    elif request_female != None:
        customers = Customer.query.filter_by(gender = "Female").all()

    if customers == []:
        customers = Customer.query.all()

    return render_template("6_customer.html", customers = customers, receipts = receipts)


# the router change and delete receipt
@app.route("/receipt")
def receipt():
    # code below use for change receipt
    request_change = request.args.get("button_change")
    request_product_quantity = request.args.get("product_quantity")
    
    infor_receipt_request_change = Receipt.query.get(request_change)
     
    if request_change != None:
        infor_receipt_request_change.quantity = request_product_quantity
        quantity = request_product_quantity.split('/')
        price = infor_receipt_request_change.price.split('/')
        total_price = 0
        
        for index in range(len(quantity)):
            total_price += int(quantity[index]) * convert_str_to_int(price[index])
        infor_receipt_request_change.total_price = total_price
        db.session.commit()

    # code below use for delete receipt
    request_delete = request.args.get("button_delete")
    infor_receipt_request_delete = Receipt.query.get(request_delete)

    if request_delete != None:
        db.session.delete(infor_receipt_request_delete)
        db.session.commit()

    receipts = Receipt.query.all()
    return render_template("7_receipt.html", receipts = receipts, test = infor_receipt_request_change)


# search by receipt id
@app.route("/search_receipt")
def search_receipt():
    list_receipts = []
    receipts = Receipt.query.all()
    for receipt in receipts:
        list_receipts.append(receipt.receipt_id)
    receipts_satify = "/".join(list_receipts)
    return render_template("8_search.html", receipts = receipts_satify)


# the router return result of the search
@app.route("/search_result")
def search_result():
    search_request = request.args.get("request_id_receipt")
    receipt = Receipt.query.get(search_request)
    quantity = receipt.quantity.split("/")
    
    total_price = 0
    products = []
    products_id = receipt.product_id.split("/")
    for index in range(len(products_id)):
        product = Product.query.get(products_id[index])
        products.append(product)
        total_price += int(convert_str_to_int(product.price) * int(quantity[index]))

    customers = Customer.query.all()
    customer_satisfies_the_condition = None
    for customer in customers:
        if str(search_request) in customer.receipt_id:
            customer_satisfies_the_condition = customer
    
    return render_template("9_display_search_result.html", receipt = receipt, customer = customer_satisfies_the_condition, products = products, total_price = convert_int_to_str(total_price))


if __name__ == "__main__":
    app.run(debug = True)
