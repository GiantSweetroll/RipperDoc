from flask import Flask, request
from flask_restx import Resource, Api, fields

app = Flask(__name__)
api = Api(app = app,
            version = "1.0",
            title = "RipperDoc API Documentation",
            description = "Upload image of logo to be processed and identified.",
            doc = "/docs/")

name_space = api.namespace('api-backend', description='Manage RipperDoc API')       # Set up name space

# Model for input from front-end
model = api.model("Image Model",
    {"image" : fields.String(required = True,
        description = "Image bits",
        help = "Image cannot be blank")
    }
)

ai_results = {}     # Dictionary to store the output of the AI

@name_space.route("/<int:id>")
class Home(Resource):
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={ 'id': 'Specify the user id according to firebase id' })
    def get(self, id):
        # Get the output of the AI
        try:
            return {
                "status" : "Results retrieved",
                "result" : ai_results[id]
            }
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")
    
    @api.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' }, 
			 params={ 'id': 'Specify the Id associated with the person' })
    @api.expect(model)
    def post(self, id):
        try:
            # TODO: Run AI here with input from request.json["image"]
            ai_results[id] = request.json["image"]      # TODO: Replace with AI output
            return {
                "status" : "Image uploaded",
                "result" : ai_results[id]
            }
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

if __name__ == '__main__':
    app.run(debug=True)