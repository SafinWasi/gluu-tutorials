import json
from flask import Flask, render_template, redirect, request
from client import Client
from extras import print_json

app = Flask(__name__)

@app.route("/")
def root():
    client_id = client_.config["client_id"]
    if client_.id_token or client_.access_token:
        return  json.dumps(client_.get_userinfo())
    else:
        return render_template("home.html", 
                                client_id=client_id)
@app.route("/login")
def login():
    new_url = client_.metadata["authorization_endpoint"] + "?response_type=code" \
        + "&client_id=" + client_.config["client_id"] + "&callback_uri=" \
        + client_.config["redirect_uri"] + "&scope=" + client_.config["scope"] \
        + "&state=abcdefghij"
    print(new_url)
    return redirect(new_url)

@app.route("/callback")
def callback():
    code_ = request.args.get("code")
    if code_:
        a = client_.get_token(code_)
        client_.id_token = a['id_token']
        client_.access_token = a['access_token']
        return redirect("/")
    

if __name__ == "__main__":
    print("Initializing")
    with open("settings.json", "r") as f:
        config_ = json.loads(f.read())
    client_ = Client(config_)
    app.run(host="0.0.0.0", debug=True)
