from flask import Flask,render_template, request
from flask_cors import  cross_origin
from utils import Dict_DF
from WikipediaScrapper import Scrapper
from mongoDB import MongoDB
from logger import getLog

logger=getLog('App.py')


app = Flask(__name__,template_folder='template')

@app.route('/')
@cross_origin()
def home():
    return render_template('Index.html')

@app.route('/scrap',methods=['GET','POST'])
@cross_origin()
def scrap():
    if request.method == 'POST':
        try:
            db_name='Scrapper'
            searchString=request.form['searchString'].replace(" ", "")
            if searchString=="":
                logger.info("No search string found")
                return render_template('Index.html')
            else:
                data=""
                collection_name=searchString.capitalize()
                scrapper_obj=Scrapper(searchString)
                db_obj=MongoDB(username='Techner',password='Techner!3')
                cursor=db_obj.openConnection()
                if db_obj.isCollectionpresent(db_name,collection_name,cursor):

                    collection=db_obj.getCollectionData(db_name,collection_name,cursor)
                    data=collection
                    logger.info("Data already present in database")

                else:
                    html=scrapper_obj.getContent()
                    logger.info("Data collection Started")
                    textdata=scrapper_obj.getTextdata(html)
                    logger.info("Text data obtained")
                    linkdata=scrapper_obj.getReference(html)
                    logger.info("Links data obtained")
                    imagedata=scrapper_obj.getImages(html)
                    logger.info("Image data obtained")
                    logger.info("Data collection Finished")
                    data={"Text":textdata,"Links":linkdata,"Images": imagedata}
                    db_obj.insertData(db_name,collection_name,data,cursor)
                    logger.info("Data stored in database")
                    db_obj.closeConnection(cursor)
                    return render_template('Result.html',result=data)
        except Exception as e:
            return render_template('Index.html',result=data)

if __name__ =="__main__":
    app.run()