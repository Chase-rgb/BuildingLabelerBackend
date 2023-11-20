from flask import Flask, request, jsonify
from PIL import Image
from time import localtime, strftime
app = Flask(__name__)

@app.route("/api/get-building", methods=["POST"])
def process_image():
    file = request.files['image']
    bearing, lat, long = request.form['bearing'], request.form['lat'], request.form['long']
    print("Bearing", bearing)
    print("Latitude", lat)
    print("Long", long)

    img = Image.open(file.stream)
    file.save("received-img.jpg")

    return jsonify({'msg': 'success', 'size': [img.width, img.height]})

@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({'msg': 'success', 'date': strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())})

if __name__ == "__main__":
    app.run(debug=True)