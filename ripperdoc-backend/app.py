from flask import Flask, request
from flask_restx import Resource, Api, fields

import constants
import numpy as np
import requests
import tensorflow as tf
import base64
import io
from PIL import Image

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
        description = "Image bits in Base64 format (jpg)",
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
            base64_bytes = image_bytes.encode('ascii')
            im_file = io.BytesIO(base64.b64decode(base64_bytes))
            image = Image.open(im_file)

            # Format input
            input_arr = tf.keras.preprocessing.image.img_to_array(image)
            input_arr = np.array([input_arr])
            input_arr = tf.image.resize(input_arr, [constants.image_width, constants.image_height])  # Resize image to fit neural network input
            input_arr = np.array(input_arr)     # Convert it back to numpy array
            input_arr /= 255        # Apply normalization

            # Make request to serving docker container
            serving_ip = request.remote_addr
            url = 'http://' + serving_ip + ':8501/v1/models/ripperdoc:predict'
            payload = {"instances" : input_arr.tolist()}
            response = requests.post(url = url, json = payload)
            
            # Process prediction
            r_json = response.json()        # JSON data of response
            pred_np = np.array(r_json['predictions'])       # Get prediction list and convert it to numpy array
            pred:str = constants.labels[int(pred_np.argmax().__str__())]        # Apply argmax and convert it to label

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