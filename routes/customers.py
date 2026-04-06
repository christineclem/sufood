from flask import Blueprint, render_template, request

from database_functions import init_db, reset_customers
from customers_functions import get_all_customers, insert_customer, update_customer, value_by_label

customers_bp = Blueprint('customers', __name__)

@customers_bp.route("/view_customers")
def view():
    rows = get_all_customers()
    return {"customers": rows}

@customers_bp.route("/new_customer", methods=["GET", "POST"])
def new_customer():
    if request.method == "POST":
        raw_data = request.json
        # `fields` is a list of dicts
        data = raw_data['data']['fields']
        data_dict = {
            "tally_id": value_by_label("customer_existing", data), # link with our primary keys
            "new_name": value_by_label("customer_new", data),
            "new_email": value_by_label("email_new", data),
            "new_phone": value_by_label("tel_new", data),
            "new_marketing": value_by_label("comms_new (Opt in to marketing communications)", data),
            "new_newsletter": value_by_label("comms_new (Join newsletter mailing list)", data),
            "updated_email": value_by_label("email_update", data),
            "updated_phone": value_by_label("tel_update", data),
            "updated_marketing_in": value_by_label("Marketing Communications (Opt in to marketing communications)", data), # opt-in
            "updated_marketing_out": value_by_label("Marketing Communications (Opt out of marketing communications)", data), # opt-out
            "updated_newsletter_in": value_by_label("Newsletter (Join newsletter mailing list)", data), #opt-in
            "updated_newsletter_out": value_by_label("Newsletter (Unsubscribe from newsletter mailing list)", data), #opt-out
            "elixir_190_amt": value_by_label("Elixir (190mL)", data),
            "elixir_250_amt": value_by_label("Elixir (250mL)", data),
            "delivery": value_by_label("Delivery options", data), # make a table with these values for pickup vs delivery
            "paid": value_by_label("payment", data),
            "payment_method": value_by_label("Payment method", data),
            "payment_plan": value_by_label("Plan for payment", data)
            }
        
        new_data = {}

        if data_dict['new_name'] is None:
            new_data['name'] = data_dict['new_name']
        else:
            new_data['name'] = None
    
        if data_dict['new_email'] is None:
            new_data['email'] = data_dict['new_email']
        else:
            new_data['email'] = None

        if data_dict['new_phone'] is None:
            new_data['phone'] = data_dict['new_phone']
        else:
            new_data['phone'] = None

        if data_dict['new_marketing'] is None:
            new_data['marketing'] = False
        else:
            new_data['marketing'] = True

        if data_dict['new_newsletter'] is None:
            new_data['newsletter'] = False
        else:
            new_data['newsletter'] = True

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

        if "updated_newsletter" in data:
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