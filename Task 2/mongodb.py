import pandas as pd
from pymongo import MongoClient

# Connecting to MongoDB
client = MongoClient("mongodb://mongo:ZNzVzoQnwpZLkrgrDPoBrflPCpHZAsCq@junction.proxy.rlwy.net:43226")
db = client["shipping_dataset"]

import os
print("Current working directory:", os.getcwd())

# Load the dataset
dataset = pd.read_csv("dataset.csv")
print(dataset)
# Define schemas for collections
customers_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "gender", "priorPurchases"],
        "properties": {
            "_id": {"bsonType": "string", "description": "CustomerID must be a string"},
            "gender": {"bsonType": "string", "enum": ["Male", "Female"], "description": "Gender must be either 'Male' or 'Female'"},
            "priorPurchases": {"bsonType": "int", "minimum": 0, "description": "Prior Purchases must be a non-negative integer"}
        }
    }
}

products_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "cost", "productImportance", "weightInGms"],
        "properties": {
            "_id": {"bsonType": "string", "description": "ProductID must be a string"},
            "cost": {"bsonType": "double", "minimum": 0, "description": "Cost must be a non-negative number"},
            "productImportance": {"bsonType": "string", "enum": ["low", "medium", "high"], "description": "Product Importance must be 'low', 'medium', or 'high'"},
            "weightInGms": {"bsonType": "double", "minimum": 0, "description": "Weight must be a non-negative number"}
        }
    }
}

orders_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "customerId", "orderDate", "discountOffered", "productId"],
        "properties": {
            "_id": {"bsonType": "string", "description": "OrderID must be a string"},
            "customerId": {"bsonType": "string", "description": "CustomerID must be a string"},
            "orderDate": {"bsonType": "string", "description": "Order date must be a string (ISO date format recommended)"},
            "discountOffered": {"bsonType": "double", "minimum": 0, "description": "Discount must be a non-negative number"},
            "productId": {"bsonType": "string", "description": "ProductID must be a string"}
        }
    }
}

shipments_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "orderId", "warehouseBlock", "modeOfShipment", "customerCareCalls", "customerRating", "reachedOnTime"],
        "properties": {
            "_id": {"bsonType": "string", "description": "ShipmentID must be a string"},
            "orderId": {"bsonType": "string", "description": "OrderID must be a string"},
            "warehouseBlock": {"bsonType": "string", "enum": ["A", "B", "C", "D", "E"], "description": "Warehouse block must be one of 'A', 'B', 'C', 'D', or 'E'"},
            "modeOfShipment": {"bsonType": "string", "enum": ["Ship", "Flight", "Road"], "description": "Mode of shipment must be 'Ship', 'Flight', or 'Road'"},
            "customerCareCalls": {"bsonType": "int", "minimum": 0, "description": "Customer care calls must be a non-negative integer"},
            "customerRating": {"bsonType": "int", "minimum": 1, "maximum": 5, "description": "Customer rating must be between 1 and 5"},
            "reachedOnTime": {"bsonType": "int", "enum": [0, 1], "description": "Reached on time must be 0 (on time) or 1 (not on time)"}
        }
    }
}

# Create or update collections with schema validation
def create_or_update_collection(collection_name, schema):
    if collection_name in db.list_collection_names():
        db.command({"collMod": collection_name, "validator": schema})
    else:
        db.create_collection(collection_name, validator=schema)

create_or_update_collection("Customers", customers_schema)
create_or_update_collection("Products", products_schema)
create_or_update_collection("Orders", orders_schema)
create_or_update_collection("Shipments", shipments_schema)

# Define collections
customers_collection = db["Customers"]
products_collection = db["Products"]
orders_collection = db["Orders"]
shipments_collection = db["Shipments"]

print("Data insertion completed successfully!")