import json
from pathlib import Path
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")

DATA_DIR = Path(__file__).parent.parent / "data"


def load_json(filename):
    """Load a JSON file from the data folder."""
    with open(DATA_DIR / filename, "r", encoding="utf-8") as file:
        return json.load(file)


def find_record(records, field, value):
    """Find a record by a specific field."""
    for record in records:
        if record.get(field) == value:
            return record
    return None


def get_customer_details(customer_id):
    """Retrieve customer details."""
    customers = load_json("customers.json")
    return find_record(customers, "customerId", customer_id)


def get_account_details(account_id):
    """Retrieve account details."""
    accounts = load_json("accounts.json")
    return find_record(accounts, "accountId", account_id)


def get_bill_details(bill_id):
    """Retrieve bill details."""
    bills = load_json("bills.json")
    return find_record(bills, "billId", bill_id)


def get_bill_items(bill_id):
    """Retrieve all bill items for a bill."""
    bill_items = load_json("bill_items.json")

    return [
        item
        for item in bill_items
        if item.get("billId") == bill_id
    ]


def get_events(bill_item_id):
    """Retrieve all events associated with a bill item."""
    events = load_json("events.json")

    return [
        event
        for event in events
        if event.get("billItemId") == bill_item_id
    ]


def get_billing_information(bill_id):
    """
    Retrieve a bill and its related bill items and events.
    """
    bill = get_bill_details(bill_id)

    if not bill:
        return {
            "error": f"Bill {bill_id} not found"
        }

    bill_items = get_bill_items(bill_id)
    bill_items_with_events = []

    for bill_item in bill_items:
        bill_item_id = bill_item.get("billItemId")

        events = get_events(bill_item_id) if bill_item_id else []

        bill_items_with_events.append({
            "billItem": bill_item,
            "events": events
        })

    return {
        "bill": bill,
        "bill_items_with_events": bill_items_with_events
    }


def get_customer_accounts(customer_id):
    """Retrieve all accounts belonging to a customer."""
    accounts = load_json("accounts.json")

    return [
        account
        for account in accounts
        if account.get("customerId") == customer_id
    ]


def get_account_products(account_id):
    """Retrieve all products belonging to an account."""
    products = load_json("products.json")

    return [
        product
        for product in products
        if product.get("accountId") == account_id
    ]


def get_product_billing_information(product_id):
    """Retrieve a product and its related bills, bill items, and events."""
    products = load_json("products.json")

    product = find_record(products, "productId", product_id)

    if not product:
        return {
            "error": f"Product {product_id} not found"
        }

    bill_items = load_json("bill_items.json")

    bill_ids = {
        item.get("billId")
        for item in bill_items
        if item.get("productId") == product_id
    }

    bills_with_details = []

    for bill_id in bill_ids:
        billing_information = get_billing_information(bill_id)

        if "error" not in billing_information:
            bills_with_details.append(billing_information)

    return {
        "product": product,
        "bills": bills_with_details
    }


def get_customer_billing_information(customer_id):
    """Retrieve all billing information for a customer."""
    customer = get_customer_details(customer_id)

    if not customer:
        return {
            "error": f"Customer {customer_id} not found"
        }

    accounts = get_customer_accounts(customer_id)
    account_information = []

    for account in accounts:
        account_id = account["accountId"]
        products = get_account_products(account_id)
        product_information = []

        for product in products:
            product_id = product["productId"]

            billing_information = get_product_billing_information(
                product_id
            )

            product_information.append(billing_information)

        account_information.append({
            "account": account,
            "products": product_information
        })

    return {
        "customer": customer,
        "accounts": account_information
    }

def search_billing_knowledge(query: str):
    try:
        response = client.vector_stores.search(
            vector_store_id=VECTOR_STORE_ID,
            query=query
        )

        return {
            "files": [r.filename for r in response.data],
            "results": [
                item.text
                for r in response.data
                for item in r.content
                if hasattr(item, "text")
            ]
        }

    except Exception as e:
        return {
            "files": [],
            "results": [],
            "error": str(e)
        }