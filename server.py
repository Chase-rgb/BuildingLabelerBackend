from flask import Flask, request, jsonify
from PIL import Image
from time import localtime, strftime
app = Flask(__name__)

@app.route("/api/send-image", methods=["POST"])
def process_image():
    file = request.files['image']
    xCoord, yCoord = request.form['x-coord'], request.form['y-coord']
    img = Image.open(file.stream)
    file.save("received-img.jpg")

    return jsonify({'msg': 'success', 'size': [img.width, img.height]})

@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({'msg': 'success', 'date': strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())})

if __name__ == "__main__":
    app.run(debug=True)