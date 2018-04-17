from flask import Flask, request, Response
import jsonpickle
import numpy as np
import base64
from PIL import Image
from io import BytesIO

# Initialize the Flask application
app = Flask(__name__)

# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # # decode image

    img = base64.b64decode(nparr)
    file_like = BytesIO(img)
    img = Image.open(file_like)
    img.save("../images/retrieved_image.jpg")

    # do some fancy processing here....

    # build a response dict to send back to client
    response = {'message': 'image received'}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    print("Image Recieved")
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
app.run(host="107.180.71.58", port=5000)