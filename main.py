from flask import Flask, render_template      
import os
app = Flask(__name__)

@app.route("/")
def sample():
    return render_template("sample.html")

@app.route("/sampleEcommTest.html")
def sampleEcommTest():
    return render_template("sampleEcommTest.html")    
     
if __name__ == "__main__":
    app.run(threaded=True,debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
 