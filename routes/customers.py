from flask import Blueprint, render_template, request

from database import init_db, reset_customers
from customers_functions import get_all_customers, insert_customer, update_customer

customers_bp = Blueprint('customers', __name__)

@customers_bp.route("/view_customers")
def view():
    rows = get_all_customers()
    return {"customers": rows}

@customers_bp.route("/new_customer", methods=["GET", "POST"])
def new_customer():
    if request.method == "POST":
        data = request.form
        new_data = {}

        if data['new_name'] != "":
            new_data['name'] = data['new_name']
        else:
            new_data['name'] = None
    
        if data['new_email'] != "":
            new_data['email'] = data['new_email']
        else:
            new_data['email'] = None

        if data['new_phone'] != "":
            new_data['phone'] = data['new_phone']
        else:
            new_data['phone'] = None

        # The following syntax is used because the form reports nothing if these boxes are unchecked
        if "new_marketing" in data:
            new_data['marketing'] = True
        else:
            new_data['marketing'] = False

        if "new_newsletter" in data:
            new_data['newsletter'] = True
        else:
            new_data['newsletter'] = False

        insert_customer(new_data)
        
        return "New customer added!"

    return render_template("new.html")

@customers_bp.route("/edit_customer", methods=["GET", "POST"])
def edit_customer():
    customers = get_all_customers()

    if request.method == "POST":
        # A dict with fields: customer_id, updated_name, updated_email, etc...
        data = request.form
        
        customer_id = int(data['customer_id'])
        # Assign existing customer info to `update_data` 
        for customer in customers:
            current_id = customer['id']

            if current_id == customer_id:
                update_data = customer
                break
            else: update_data = "This customer does not exist." # Shouldn't be possible, but error handling

        # Actually update `update_data`
        if data['updated_name'] != "":
            update_data['name'] = data['updated_name']
        
        if data['updated_email'] != "":
            update_data['email'] = data['updated_email']

        if data['updated_phone'] != "":
            update_data['phone'] = data['updated_phone']

        if "updated_marketing" in data:
            update_data['marketing'] = True
        else:
            update_data['marketing'] = False

        if "updated_newsleter" in data:
            update_data['newsletter'] = True
        else:
            update_data['newsletter'] = False
        
        update_customer(update_data)

        return update_data
        
    return render_template("edit.html", customers = customers)


@customers_bp.route("/reset_customers")
def reset():
    reset_customers()
    init_db()
    return "Customers table reset."