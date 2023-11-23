from flask import Flask, request, jsonify
from PIL import Image
from time import localtime, strftime
from Prediction import predict
app = Flask(__name__)

@app.route("/api/get-building", methods=["POST"])
def process_image():
    file = request.files['image']
    bearing, lat, long = float(request.form['bearing']), float(request.form['lat']), float(request.form['long'])

    # img = Image.open(file.stream)
    file.save("received-img.jpg")

    buildings = predict(lat, long, bearing, "received-img.jpg")
    return jsonify({'msg': 'success', 'buildings': buildings})

@app.route("/api/ping", methods=["GET"])
def ping():
    return jsonify({'msg': 'success', 'date': strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())})

if __name__ == "__main__":
    app.run(debug=True)