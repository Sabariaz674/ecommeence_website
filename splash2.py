from flask import Flask, render_template

app = Flask(__name__)

# Route for Splash Page
@app.route('/')
def splash2():
    return render_template('splash2.html')

# Route for the home page (after clicking "Let's Get Started")
@app.route('/home')
def home():
    return render_template('home.html')

# Define category route (if you need it)
@app.route('/category')
def category():
    return render_template('category.html')

if __name__ == '__main__':
    app.run(debug=True)
