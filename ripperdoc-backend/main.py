from flask import Flask, request
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app = app,
            version = "1.0",
            title = "RipperDoc API Documentation",
            description = "Upload image of logo to be processed and identified.",
            doc = "/docs/")

name_space = api.namespace('RipperDoc', description='Manage RipperDoc API')

@name_space.route("/")
class Home(Resource):
    def get(self):
        return {'scan': "These are not the droids you're looking for"}

@name_space.route("/apitest")
class APITest(Resource):
    def get(self):
        return {'about':"Hello World!"}

    def post(self):
        some_json = request.get_json()
        return {'you sent': some_json}, 201

if __name__ == '__main__':
    app.run(debug=True)