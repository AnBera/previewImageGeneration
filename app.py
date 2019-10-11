from flask import Flask
import takescreenshot

app = Flask(__name__)

@app.route("/")
def hello():
    takescreenshot.initialize()
    return "Finished taking screenshot..."

# main driver function 
if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run(port=5001, threaded=True, host=('0.0.0.0')) 