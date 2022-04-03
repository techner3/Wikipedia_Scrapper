import pymongo
import ssl
from logger import getLog

logger=getLog('mongoDB.py')
class MongoDB():

    def __init__(self,username,password):

        try:
            self.username=username
            self.password=password
            self.url=f"mongodb+srv://{self.username}:{self.password}@cluster0.eddrp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            logger.info("DB object has been successfully intialized")
        except Exception as e:
            logger.exception(f"Failed to intialize DB object : \n{e}")
            raise Exception("Failed to intialize DB object")
    
    def openConnection(self):

        try:
            client=pymongo.MongoClient(self.url)
            logger.info("DB connection established")
            return client
        except Exception as e:
            logger.exception(f"Failed to open connection : \n{e}")
            raise Exception("Failed to open connection")

    def closeConnection(self,client):

        try:
            client.close()
            logger.info("DB connection closed")
        except Exception as e:
            logger.exception(f"Failed to close connection : \n{e}")
            raise Exception("Failed to close connection")

    def isDBpresent(self,db_name,client):

        try:
            if db_name in client.list_database_names():
                return True
            else:
                return False
        except Exception as e:
            logger.exception(f"Failed to check if DB is present : \n{e}")
            raise Exception("Failed to check if DB is present")
    
    def createDB(self,db_name,client):

        try:
            db=client[db_name]
            logger.info("Created DB")
            return db
        except Exception as e:
            logger.exception(f"Failed to create DB : \n{e}")
            raise Exception("Failed to create DB")

    def getDB(self,db_name,client):

        try:
            db=client[db_name]
            logger.info("DB retrieved")
            return db
        except Exception as e:
            logger.exception(f"Failed to retrieve DB : \n{e}")
            raise Exception("Failed to retrieve DB")
    
    def dropDB(self,db_name,client):

        try:
            if self.isDBpresent(db_name,client):
                client.drop_database(db_name)
                logger.info(f"{db_name} has been dropped")
        except Exception as e:
            logger.exception(f"Failed to drop DB : \n{e}")
            raise Exception("Failed to drop DB")

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
            logger.exception(f"Failed to check if collection is present : \n{e}")
            raise Exception("Failed to check if collection is present")

    def createCollection(self,db_name,collection_name,client):

        try:
            db=self.createDB(db_name,client)
            collection=db[collection_name]
            logger.info("Collection created")
            return collection
        except Exception as e:
            logger.exception(f"Failed to create collection : \n{e}")
            raise Exception("Failed to create collection")
    
    def getCollection(self,db_name,collection_name,client):

        try:
            db=self.getDB(db_name,client)
            collection=db[collection_name]
            logger.info("Collection retrieved")
            return collection
        except Exception as e:
            logger.exception(f"Failed to retrive collection : \n{e}")
            raise Exception("Failed to retrieve collection")

    def getCollectionData(self,db_name,collection_name,client):

        try:
            collection=self.getCollection(db_name,collection_name,client)
            data=collection.find({},{'_id':0})
            logger.info("Collection data retrieved")
            return data.next()
        except Exception as e:
            logger.exception(f"Failed to retrive collection : \n{e}")
            raise Exception("Failed to retrive collection")
    

    def dropCollection(self,db_name,collection_name,client):

        try:
            if self.isCollectionpresent(db_name,collection_name,client):
                collection=self.createCollection(db_name,collection_name,client)
                collection.drop()
            logger.info(f"{collection_name} has been dropped")
        except Exception as e:
            logger.exception(f"Failed to drop collection : \n{e}")
            raise Exception("Failed to drop collection")

    def insertData(self,db_name,collection_name,data,client):

        try:
            collection=self.createCollection(db_name,collection_name,client)
            collection.insert_one(data)
            logger.info("Data Inserted")
        except Exception as e:
            logger.exception(f"Failed to insert data : \n{e}")
            raise Exception("Failed to insert data")