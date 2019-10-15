from flask import Flask, request
import takescreenshot

app = Flask(__name__)

@app.route("/", methods=["POST"])
def generate_image():
    takescreenshot.initialize(request.json["imageNames"])
    return "Finished taking screenshot..."

# main driver function 
if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run(port=5000, threaded=True, host=('0.0.0.0')) 