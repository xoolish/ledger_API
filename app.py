from flask import Flask
from flask import request,jsonify
app=Flask(__name__)

@app.route("/")
def home():
    return "The ledger API is running!"

expenses=[]
@app.route("/expenses",methods=["POST"])
def expense():
    data=request.get_json()

    if not data or not "title" in data or not "amount" in data:
        return jsonify({"Error": "Missing 'title' or'amount'"}),400
    expense={"title":data["title"],
             "amount":data["amount"],
             "category":data.get("category", "Uncategorized")}
    expenses.append(expense)
    return jsonify({"Message":"Expense added","expense":expense}),201
    

if __name__=="__main__":
    app.run(debug=True)
   