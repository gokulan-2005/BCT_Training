from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]
collection = db["students"]

# insert one
collection.insert_one({"name": "Karthikeyan", "age": 21})

# insert many
collection.insert_many([
    {"name": "Alice", "age": 20},
    {"name": "Bob", "age": 23}
])

# read
print("\nAll Data:")
for doc in collection.find():
    print(doc)

# search
print("\nSearch:")
for doc in collection.find({"name": "Alice"}):
    print(doc)

# update
collection.update_one(
    {"name": "Alice"},
    {"$set": {"age": 26}}
)

# delete
collection.delete_one({"name": "Bob"})

print("\nOperations completed!")