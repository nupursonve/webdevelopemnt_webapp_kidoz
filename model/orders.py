from app import db
import datetime

class Orders(db.Model):
  __tablename__ = "orders" # Defining table name

  orderID = db.Column(db.Integer, primary_key=True, autoincrement=True)
  productID = db.Column(db.Integer)
  userID = db.Column(db.Integer)
  orderAddedOn = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  def createOrder(self):
    db.session.add(self)
    db.session.commit()
    db.session.flush()
    return self