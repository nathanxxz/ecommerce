from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

#Flask shell, usado para criar todos os models em tabela em banco
#db.create_all() usado para criar o banco
#db.session.commit() usado para efetivar as mudancas no banco
# exit() para sair do banco

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)
CORS(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(120), nullable = False)
    price = db.Column(db.Float, nullable = False)
    description = db.Column(db.Text, nullable = True)

@app.route("/api/products/add", methods=["POST"])
def addProduct():
  data = request.json
  if("name" in data and "price" in data):
    product = Product(name =data["name"] , price =data["price"] ,description =data.get("description",""))
    db.session.add(product)
    db.session.commit()
    return jsonify({"message" : "Dados do produto adicionado"})
 
  return jsonify({"message" : "Dados do produto invalido"}),400

@app.route("/api/products/delete/<int:id>",methods=["DELETE"])
def deleteProduct(id):
   product = Product.query.get(id)
   if(product):
       db.session.delete(product)
       db.session.commit()
       return jsonify({"message" : "Produto removido"})
   return jsonify({"message" : "Dados do produto nao encontrado"}),404

@app.route("/api/products/get/<int:id>",methods=["GET"])
def getProduct(id):
   getProduct = Product.query.get(id)
   if(getProduct):
     return jsonify ({
        "id": getProduct.id,
        "name": getProduct.name,
        "price": getProduct.price
    })
   return jsonify({"message": "Produto nao encontrado"}), 404

@app.route("/api/products", methods=["GET"])
def getProducts():
  products = Product.query.all()
  productList = []
  for p in products:
      productDate = {
       "id": p.id,
       "name": p.name,
       "price": p.price
      }
      productList.append(productDate)
  return jsonify(productList)
   

@app.route("/api/products/update/<int:id>",methods=["PUT"])

def updateProduct(id):
   getProduct = Product.query.get(id)

   if(not getProduct):
      return jsonify({"message": "Produto nao encontrado"}), 404
   
   data = request.json

   if("name" in data):
      getProduct.name = data['name']
   
   if("price" in data):
      getProduct.price = data['price']
  
   if("description" in data):
      getProduct.description = data['description']
   
   db.session.commit()
   
   return jsonify({"message": "Produto atualizado"})
      


if(__name__ == "__main__"):
   app.run(debug=True)



