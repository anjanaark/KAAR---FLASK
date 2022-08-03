import logging

from flask_pymongo import pymongo
from flask import jsonify, request

con_string = "mongodb+srv://anjana_k:raksha17@cluster0.xqpimiv.mongodb.net/?retryWrites=true&w=majority"
client=pymongo.MongoClient(con_string)
db=client.get_database('firstdatabase')
user_collection=pymongo.collection.Collection(db,'firstcollection')
print("MongoDB Connection Success")

def project_api_routes(endpoints):
    @endpoints.route("/hello",methods=['GET'])
    def hello():
        res = 'hello world'
        print("hello world")
        return res

    @endpoints.route("/register-user",methods=['POST'])
    def register_user():
        resp={}
        try:
            req_body = request.json
            user_collection.insert_one(req_body)
            print("User data stored sucessfully in database")
            status ={
                "statusCode":"200",
                "statusMessage":"User data stored sucessfully in database"
            }
        except Exception as e:
            print(e)
            status ={
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"]=status
        return resp

    @endpoints.route('/read-users',methods=['GET'])
    def read_users():
        resp={}
        try:
            users=user_collection.find({})
            print(users)
            users = list(users)
            status = {
                "statusCode":"200",
                "statusMessage":"User data retrived sucessfully in database"
            }
            output =[{'Name':user['name'],'Email':user['email']} for user in users]
            resp['data'] = output
        except Exception as e:
            print(e)
            status={
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] = status
        return resp
    
    @endpoints.route("/update-users",methods=['PUT'])
    def update_users():
        resp={}
        try:
            req_body = request.json
            user_collection.update_one({"id":req_body['id']},{"$set":req_body['update_user_body']})
            print("user data updated sucessfully in database")
            status={
                "statusCode":"200",
                "statusMessage":"user data updated sucessfully in database"
            }
        except Exception as e:
            print(e)
            status={
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"]=status
        return resp

    @endpoints.route("/delete",methods=['DELETE'])
    def dele_te():
        resp={}
        try:
            delete_id=request.args.get('delete_id')
            user_collection.delete_one({"id":delete_id})
            print("user data updated sucessfully in database")
            status={
                "statusCode":"200",
                "statusMessage":"user data deleted sucessfully in database"
            }
        except Exception as e:
            print(e)
            status={
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"]=status
        return resp

    return endpoints