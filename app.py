import model
from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import stripe
stripe.api_key = 'sk_test_51Ik6dMLoCCUJNLQCcWBIMdPeHUQmQurbFZtr97mmpq2af6WlLh4Pv6x8Nu9s013rL3rZS4uCkrhFoVYzyGkPQuo700Fk5DZ9x0'
app = Flask(__name__)
app.config.from_pyfile("config.cfg") # Configuration file
app.secret_key = 'sessionKey'
db = SQLAlchemy(app) # Connecting to SQLAlchemy
from model.contactUs import *
from model.products import *
from model.login import *
from model.orders import *
from passlib.hash import pbkdf2_sha256 as sha256

def generateHash(password):
  return sha256.hash(password)

def verifyHash(password, hash):
  return sha256.verify(password, hash)

@app.route('/')
def home():
  return render_template("home.html")

@app.route('/shop')
def shop():
  return render_template("shop.html")

@app.route('/about-us')
def aboutUs():
  return render_template("aboutUs.html")

@app.route('/contact-us')
def contactUs():
  return render_template("contactUs.html")

@app.route('/save-contact-us', methods = ['POST'])
def saveContactUs():
  if(request.method == "POST"):
    dbObj = ContactUs(
      name=request.form["name"],
      emailID=request.form["emailID"],
      mobileNumber=request.form["mobileNumber"],
      message=request.form["message"]
    )
    response = dbObj.createContactUs()  # Create a new contact us
    if (response.contactUsID > 0):
      return jsonify("Success")
    else:
      return jsonify("Error")

@app.route('/sign-in')
def signIn():
  return render_template("signIn.html")

@app.route('/get-user', methods = ['POST'])
def validateUser():
  if(request.method == "POST"):
    emailID = request.form["emailID"]
    password = request.form["password"]
    loginObj = Login.validateUser(emailID) #call validateLogin function from dbConnection file
    if (len(loginObj) > 0):
      for keys, values in enumerate(loginObj):
        if (verifyHash(password, values.password)):
          session["userID"] = values.userID
          session["fullName"] = values.fullName
          session["emailID"] = values.emailID
          return jsonify("Success")
        else:
          return jsonify("Error")
    else:
      return jsonify("Invalid")

@app.route('/logout', methods = ['POST'])
def logout():
  session.clear() # Destroy session..
  return jsonify("Success")

@app.route('/signup')
def signup():
  return render_template("signup.html")

@app.route('/create-user', methods = ['POST'])
def createUser():
  if(request.method == "POST"):
    dbObj = Login(
      fullName=request.form["fullName"],
      emailID=request.form["emailID"],
      password=generateHash(request.form["password"])
    )
    response = dbObj.createUser()
    if (response.userID > 0):
      session["userID"] = response.userID
      session["fullName"] = request.form["fullName"]
      session["emailID"] = request.form["emailID"]
      return jsonify("Success")
    else:
      return jsonify("Error")

@app.route('/get-products')
def getProducts():
  productObj = Products.getProducts()
  products = []  # Empty list
  for keys, values in enumerate(productObj):
    print (values.productImage)
    products.append({
      "productID": values.productID,
      "productImage": values.productImage,
      "productName": values.productName,
      "price": values.price,
      "productAddedOn": str(
        values.productAddedOn),  # Convert date to string
    })
  return jsonify({
    "data": products,
    "message": "success",
  })
@app.route('/checkout')
def checkout():
  return render_template("checkout.html")

# YOUR_DOMAIN = 'http://127.0.0.1:5000'
YOUR_DOMAIN = 'http://34.244.137.44'
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
  try:
    # len(request.form["products"].split(","))
    session["products"] = request.form["products"]
    checkout_session = stripe.checkout.Session.create(
      payment_method_types=['card'],
      line_items=[
        {
          'price_data': {
            'currency': 'eur',
            'unit_amount': int(request.form["totalAmount"])*100,
            'product_data': {
              'name': 'Kidoz Toys',
            },
          },
          'quantity': 1,
        },
      ],
      mode='payment',
      success_url=YOUR_DOMAIN + '/thank-you',
      cancel_url=YOUR_DOMAIN + '/cancel',
    )
    return jsonify({'id': checkout_session.id})
  except Exception as e:
    return jsonify(error=str(e)), 403

@app.route('/thank-you')
def thankyou():
  products = session["products"].split(",")
  for values in products:
    # print (values)
    dbObj = Orders(
      userID=session["userID"],
      productID=values
    )
    response = dbObj.createOrder()
  session.pop("products")
  return render_template("thankyou.html")

@app.route('/cancel')
def cancelDonation():
  return render_template("cancel.html")

if __name__ == '__main__':
  app.run(debug=True)