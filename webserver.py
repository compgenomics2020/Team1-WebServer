from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def home():
    return render_template("home.html")

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/analyze")
def analyze():
    return render_template("analyze.html")


if __name__=="__main__":
    app.run(debug=True)
