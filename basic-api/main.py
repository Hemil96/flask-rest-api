from flask import Flask, redirect, url_for, render_template, request,jsonify
app = Flask(__name__)

stores =[
    {
        'name' : "My wonderful Store",
        'items' : [
            {
                "name":"soap",
                "price": 15
            }
        ]
    }
]

@app.route("/")
def hello():
    return render_template("index.html")


# POST /store data: name
@app.route("/store", methods=['POST'])
def creat_store():
    request_data = request.get_json()
    new_store = {
        "name" : request_data["name"],
        "items" :  []
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET store/<name>
@app.route("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify(store )
        else:
            jsonify({"msg":"not found"})


# GET /store
@app.route("/store")
def get_stores():
    return jsonify({"stores" : stores})


# POST /store/<string:name>/item
@app.route("/store/<string:name>/item",methods=["POST"])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {
                "name" : request_data["name"],
                "price" :  request_data["price"]
            }
        store['items'].append(new_item)
        return jsonify(new_item)
    return jsonify({"MSG":"Not Found"})


# GET /store/<string:name>/item
@app.route("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items":store["items"]})
        else:
            jsonify({"msg":"not found"})
    
    
if __name__ == "__main__":  
    app.run(debug=True)
