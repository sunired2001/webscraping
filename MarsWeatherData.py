from flask import Flask,render_template,redirect
import pymongo
app=Flask(__name__)
import MarsLib as ms
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db=client["MarsDB"]
marscoll=db["MarsCollection"]
@app.route("/")
def indexPage():
    finallist = ms.finalresult()

    marscoll.delete_many({})
    marscoll.insert_many(finallist)
    marsfinallist=list(marscoll.find())

    return render_template("Mars.html",marslist=marsfinallist)
if __name__== "__main__":
    app.run(debug=True)


