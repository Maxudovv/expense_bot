import Database
import pickle

id = '1235544532'
db = Database.Database()
class User:
    def __init__(self):
        self.expansion = 0
        self.user_id = id

db.add_user(user_id=int(id), data=pickle.dumps(User))

