import pymongo

class MongoDB():

    def __init__(self,username,password):

        try:
            self.username=username
            self.password=password
            self.url=f"mongodb+srv://{self.username}:{self.password}@cluster0.eddrp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        except Exception as e:
            raise Exception(f"Failed to intialize DB object : \n{e}")
    
    def openConnection(self):

        try:
            client=pymongo.MongoClient(self.url)
            return client
        except Exception as e:
            raise Exception(f"Failed to open connection : \n{e}")

    def closeConnection(self,client):

        try:
            client.close()
        except Exception as e:
            raise Exception(f"Failed to close connection : \n{e}")

    def isDBpresent(self,db_name,client):

        try:
            if db_name in client.list_database_names():
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"Failed to check if DB is present : \n{e}")
    
    def createDB(self,db_name,client):

        try:
            db=client[db_name]
            return db
        except Exception as e:
            raise Exception(f"Failed to create DB : \n{e}")
    
    def dropDB(self,db_name,client):

        try:
            if self.isDBpresent(db_name,client):
                client.drop_database(db_name)
        except Exception as e:
            raise Exception(f"Failed to drop DB : \n{e}")

    def isCollectionpresent(self,db_name,collection_name,client):

        try:
            if self.isDBpresent(db_name,client):
                db=self.createDB(db_name,client)
                if collection_name in db.list_collection_names():
                    return True 
                else:
                    return False
            else:
                return False
        except Exception as e:
            raise Exception(f"Failed to check if collection is present : \n{e}")

    def createCollection(self,db_name,collection_name,client):

        try:
            db=self.createDB(db_name,client)
            collection=db[collection_name]
            return collection
        except Exception as e:
            raise Exception(f"Failed to create collection : \n{e}")

    def dropCollection(self,db_name,collection_name,client):

        try:
            if self.isCollectionpresent(db_name,collection_name,client):
                collection=self.createCollection(db_name,collection_name,client)
                collection.drop()
        except Exception as e:
            raise Exception(f"Failed to drop collection : \n{e}")

    def insertData(self,db_name,collection_name,data,client):

        try:
            collection=self.createCollection(db_name,collection_name,client)
            collection.insert_one(data)
            return f"Inserted data"
        except Exception as e:
            raise Exception(f"Failed to insert data : \n{e}")