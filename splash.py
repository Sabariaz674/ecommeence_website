from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Route for the First Splash Page
@app.route('/')
def splash():
    return render_template('splash.html')  # Render the splash page

# Route for the Second Splash Page
@app.route('/splash2')
def splash2():
    return render_template('splash2.html')  # Render the splash2 page

# Route for the Home Page
@app.route('/home')
def home():
    return render_template('home.html')  # Render the home page after splash2


# Route for the Aesthetic Outfits Page (NEW!)
@app.route('/category')
def category():
    return render_template('category.html')  # Render the products page

@app.route('/traditional')
def traditional():
    return render_template('traditional.html') 

@app.route('/addtocart')
def addtocart():
    return render_template('addtocart.html')  # Render the products page

if __name__ == '__main__':
    app.run(debug=True)
