from flask import Flask,request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate,identity

app = Flask(__name__)
app.secret_key = "hems"
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth
items = [{
    "name":"soap",
    "price":20
}]

class Item(Resource):
    @jwt_required()
    def get(self ,name):
        item = next(filter(lambda x:x["name"]==name,items), None)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x:x["name"] == name ,items), None):   
            return { "Message" : "Item '{}' is already exist.".format(name) }, 400

        data = request.get_json()
        item = {"name" : name, "price" : data['price']}
        items.append(item)
        return item, 201

    def delete(self,name):
        global items
        items = list(filter(lambda x:x['name'] != name, items))
        return {"Message" : "Item deleted"}

class ItemList(Resource):
    def get(self):
        return{ "Items": items} 

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")


app.run(port=5000, debug=True) 