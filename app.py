from flask import Flask
from bird import *

app = Flask(__name__)

@app.route("/")
def get_scooters():
    bird = get_bird()
    return bird

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)