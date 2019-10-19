from flask import Flask, request
import takescreenshot
import concurrent.futures
import os

executer = concurrent.futures.ThreadPoolExecutor(max_workers=min(32, os.cpu_count() + 4))

app = Flask(__name__)

@app.route("/", methods=["POST"])
def generate_image():
    executer.submit(takescreenshot.initialize, request.json["imageNames"])
    return "taking screenshot job submitted..."

@app.route("/batch", methods=["POST"])
def generate_batch_image():
    executer.submit(takescreenshot.initialize_batch)
    return "taking screenshot job submitted..."

# main driver function 
if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run(port=5000, threaded=True, host=('0.0.0.0')) 