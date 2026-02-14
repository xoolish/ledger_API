from flask import Flask
from flask import request,jsonify
from datetime import datetime
from functools import wraps
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

users= [{"id":1,
         "username":"xoolish",
         "password":"1234"
         },
        {"id":2,
         "username":"abba",
         "password":"abcd"
        }
]

@app.route("/login", methods=["POST"])
def login():
    data=request.get_json()
    username=data.get("username")
    password=data.get("password")

    user=next((u for u in users if u["username"]==username and u["password"]==password),None)
    if user:
        token=str(user["id"])
        return jsonify({"Message":"Login Sucessful", "token":token}),200
    return jsonify({"Message":"Invalid Username/Password"}),401

def require_auth(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=request.headers.get("Authorization")
        if not token:
            return jsonify({"Message":"missing token"})
        current_user=next((u for u in users if str(user["id"])==token))
        if not current_user:
            return jsonify({"Message":"invalid token"})
        request.current_user=current_user
        return f(*args,**kwargs)
    return decorated

 



@app.route("/expenses", methods=["POST"])
@require_auth
def add_expense():
    current_user=request.current_user
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
        expense={"user_id":current_user["id"],
                 "amount":item["amount"],
                 "category":item.get("category", "Uncategorized"),
                 "payment_method":item["payment_method"],
                 "date":item.get("date",datetime.today().strftime("%Y-%m-%d"))}
        expenses.append(expense)
        added.append(expense)        
    status_code=201 if added and not failed else 207 if added and failed else 400
    return jsonify ({"added":added,
                     "failed":failed}),status_code

@app.route("/expenses", methods=["GET"])
@require_auth
def view_expenses():
    current_user=request.current_user
    user_expenses=[e for e in expenses if e["user_id"] == current_user["id"]]
    return jsonify({"Expenses":user_expenses,
                    "Count":len(expenses)
                   }),200

    

if __name__=="__main__":
    app.run(debug=True)
   