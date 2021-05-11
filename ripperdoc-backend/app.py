from flask import Flask, request
from flask_restx import Resource, Api, fields

import constants
import methods
import numpy as np
import requests
import tensorflow as tf

ai_results = {}     # Dictionary to store the output of the AI

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
        description = "Image bits in Base64 format",
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
            # Decode image into tensor
            image_bytes = request.json['image']
            image = tf.image.decode_image(image_bytes, dtype=tf.string, channels=3)

            # Format input
            input_arr = tf.keras.preprocessing.image.img_to_array(image)
            input_arr = np.array([input_arr])
            input_arr /= 255        # Apply normalization

            # Make prediction
            url = 'localhost:8501/models/ripperdoc_xception:predict'
            payload = '{"instances" : ' + input_arr + '}'
            result = requests.post(url, payload)
            pred:str = constants.labels[int(result.argmax().__str__())]

            # Return as response
            ai_results[id] = pred
            return {
                "status" : "Image uploaded",
                "result" : ai_results[id]
            }
        except KeyError as e:
            name_space.abort(500, e.__doc__, status = "Could not retrieve information", statusCode = "500") 
        except Exception as e:
            print(e)
            name_space.abort(400, e.__doc__, status = "Could not retrieve information", statusCode = "400")

if __name__ == '__main__':
    # Start flask server or train AI
    app.run(host='0.0.0.0')