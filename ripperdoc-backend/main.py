from flask import Flask, request
from flask_restx import Resource, Api, fields
from neural_network import NeuralNetwork

import file_operations as io
import methods

ai_results = {}     # Dictionary to store the output of the AI
ai: NeuralNetwork = None    # The AI model

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

@name_space.route("/<string:id>")
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
            image = None
            try:
                image = methods.read_image_from_bytes(request.json["image"])
            except Exception as e:
                name_space.abort(400, e.__doc__, status = "Error in reading image file", statusCode = "400")

            ai_results[id] = ai.predict(image)
            return {
                "status" : "Image uploaded",
                "result" : ai_results[id]
            }
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500")
        except Exception as e:
            name_space.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

def train_ai():
    nn: NeuralNetwork = NeuralNetwork()
    nn.train(batch_size=1)
    nn.save('test')


if __name__ == '__main__':

    # Load AI
    print('Loading AI...')
    ai = NeuralNetwork(model=io.load_model('ai/test.h'))
    print('AI loaded successfully')

    # Start flask server
    app.run(debug=True)
    # train_ai()