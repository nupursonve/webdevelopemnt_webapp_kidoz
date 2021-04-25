from app import db
import datetime

class Products(db.Model):
  __tablename__ = "products" # Defining table name

  productID = db.Column(db.Integer, primary_key=True, autoincrement=True)
  productImage = db.Column(db.String(200))
  productName = db.Column(db.String(100))
  price = db.Column(db.Float)
  productAddedOn = db.Column(db.DateTime, default=datetime.datetime.utcnow)

  @classmethod
  def getProducts(self):
    return Products.query.all()