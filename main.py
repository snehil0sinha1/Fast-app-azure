from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLAlchemy setup
DATABASE_URL = "mssql+pyodbc://snehil:Password123@gradedsqlserver.database.windows.net/ProductDBGraded?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Model for Products Table
class Product(Base):
    __tablename__ = "Products"
    ProductID = Column(Integer, primary_key=True, index=True)
    ProductName = Column(String, nullable=False)
    Description = Column(String, nullable=False)
    Price = Column(DECIMAL(10, 2), nullable=False)
    StockQuantity = Column(Integer, nullable=False)
    ImageURL = Column(String)
    Category = Column(String)

class ProductUpdate(BaseModel):
    ProductName: str
    Description: str
    Price: float
    StockQuantity: int
    ImageURL: str
    Category: str

app = FastAPI()

@app.get("/products")
async def get_products():
    products = session.query(Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products

@app.post("/products/{product_id}")
async def update_product(product_id: int, product_update: ProductUpdate):
    product = session.query(Product).filter(Product.ProductID == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.ProductName = product_update.ProductName
    product.Description = product_update.Description
    product.Price = product_update.Price
    product.StockQuantity = product_update.StockQuantity
    product.ImageURL = product_update.ImageURL
    product.Category = product_update.Category

    session.commit()
    return {"message": "Product updated successfully"}
