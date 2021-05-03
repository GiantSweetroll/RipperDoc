from flask import Flask, request
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app)

class Home(Resource):
    def get(self):
        return {'scan': "These are not the droids you're looking for"}

class APITest(Resource):
    def get(self):
        return {'about':"Hello World!"}

    def post(self):
        some_json = request.get_json()
        return {'you sent': some_json}, 201

api.add_resource(Home, "/")
api.add_resource(APITest, '/apitest')

if __name__ == '__main__':
    app.run(debug=True)