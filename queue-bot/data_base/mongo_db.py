import pymongo
from config.config import load_data

# получаем сслыку на базу данных
db_uri = load_data(".env").mongo_db.db_uri

# инициализация базы данных
client = pymongo.MongoClient(db_uri)
db = client.queue
coll = db.users
requests_coll = db.requests

# добавление новых индексов в базу данных
coll.create_index([("user_id", pymongo.DESCENDING)], unique=True)
coll.create_index([("queue_number", pymongo.DESCENDING)], unique=False)


def find_the_last_one(coll=coll):
    user = coll.find_one(sort=[("queue_number", -1)])
    if user:
        return user["queue_number"]
    return 0


def get_in_line(message, coll=coll):
    queue_number = find_the_last_one() + 1
    data = {
        "queue_number": queue_number,
        "name": message.from_user.full_name,
        "user_id": message.from_user.id,
    }
    coll.insert_one(data)


def get_out_of_the_line(user_id, coll=coll):
    queue_number = coll.find_one({"user_id": user_id})["queue_number"]
    coll.delete_one({"user_id": user_id})
    current = {"queue_number": {"$gt": queue_number}}
    new = {"$inc": {"queue_number": -1}}
    coll.update_many(current, new)


def admin_swap(queue_number1, queue_number2):
    user1 = coll.find_one({"queue_number": queue_number1})["user_id"]
    user2 = coll.find_one({"queue_number": queue_number2})["user_id"]
    coll.update_one({"user_id": user1}, {"$set": {"queue_number": queue_number2}})
    coll.update_one({"user_id": user2}, {"$set": {"queue_number": queue_number1}})


def get_user_id(queue_number):
    return coll.find_one({"queue_number": queue_number})["user_id"]


def get_user_queue_number(user_id):
    return coll.find_one({"user_id": user_id})["queue_number"]


def insert_request(user1_id, user2_id):
    requests_coll.insert_one({"sender": user1_id, "recipient": user2_id})


def delete_request(user1_id, user2_id):
    requests_coll.delete_one({"sender": user1_id, "recipient": user2_id})


def get_request_ids(recipient_id):
    request = requests_coll.find_one({"recipient": recipient_id})
    return [request["sender"], request["recipient"]]


def show(coll=coll):
    return coll.find().sort("queue_number", 1)


def show_me(user_id, coll=coll):
    return coll.find_one({"user_id": user_id})
