from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')  # Make sure this is the clothing site's homepage
if __name__ == '__main__':
    app.run(debug=True)