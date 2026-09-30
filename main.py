
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product

from sqlalchemy.orm import Session
from database import session, engine
import database_models

app = FastAPI()

app.add_middleware(
     CORSMiddleware,
     allow_origins=["http://localhost:3000"],
     allow_methods=["*"]
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "Welcome to FastAPI"

products = [
    Product(id=1,name="laptop",description="badget laptop",price=999.0, quantity=10),
    Product(id=2, name="mobile", description= "basic mobile", price=699, quantity=30),
    Product(id=3,name="pen",description="blue link pen",price=9.0, quantity=100),
    Product(id=4, name="Table", description= "Wooden table", price=190, quantity=20)
]

def get_db():
    db = session()
    try:
        yield db
    finally:    
        db.close()

def db_init():
     db = session()
     count = db.query(database_models.Product).count
     if count==0 :
        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()


db_init();

@app.get("/products")
def getProducts(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()

    return db_products

@app.get("/products/{id}")
def getProduct(id:int, db: Session = Depends(get_db)):
        db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
        if db_product:
                  return db_product             
        return "product not found"

@app.post("/products")
def addProduct(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    #products.append(product)
    return product 

@app.put("/products/{id}")
def updateProduct(id:int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product updated successfully"
    return "Product not found"

@app.delete("/products/{id}")
def deleteProduct(id:int, db: Session = Depends(get_db)):
    #  for i in range(len(products)):
    #       if (products[i].id==id):
    #            del products[i]
    #            return "Product deleted successfully"

    db_product = db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
         db.delete(db_product)
         db.commit()
         return "Product deleted successfully"
    return "Product not found"
