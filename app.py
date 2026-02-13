from flask import Flask
from flask import request,jsonify
from datetime import datetime
app=Flask(__name__)

@app.route("/")
def home():
    return "The ledger API is running!"

expenses=[]
def validate_expense(item):
    errors=[]
    if not item.get("amount"):
        errors.append("Amount is required")
    if not item.get("payment_method"):
        errors.append("Payment_method is required")
    return errors

@app.route("/expenses", methods=["POST"])
def add_expense():
    data=request.get_json()
    
    if not data:
        return jsonify({"Error": "No data provided"}),400
   
    items=data if isinstance(data,list) else [data]
    added=[]
    failed=[]

    for item in items:
        errors=validate_expense(item)
        if errors:
            failed.append({"item":item,"errors":errors})
            continue
        expense={"amount":item["amount"],
             "category":item.get("category", "Uncategorized"),
             "payment_method":item["payment_method"],
              "date":item.get("date",datetime.today().strftime("%Y-%m-%d"))}
        expenses.append(expense)
        added.append(expense)        
    status_code=201 if added and not failed else 207 if added and failed else 400
    return jsonify ({"added":added,
                     "failed":failed}),status_code

@app.route("/expenses", methods=["GET"])
def view_expenses():
    return jsonify({"Expenses":expenses,
                    "Count":len(expenses)
                   }),200

    

if __name__=="__main__":
    app.run(debug=True)
   