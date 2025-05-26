from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import sqlite3
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'your_secret_key' 


# Categories data
categories = [
    {'name': 'Aesthetic', 'url': '/aesthetic', 'image': 'static/images/Asthetic.jpg','code': 'A0134', 'price': 'Rs3000'},
    {'name': 'Traditional', 'url': '/traditional', 'image': 'static/images/traditional.jpg','code': 'A0234', 'price': 'Rs3500'},
    {'name': 'Party Wear', 'url': '/partywear', 'image': 'static/images/partwear.jpg','code': 'A0534', 'price': 'Rs5000'},
    {'name': 'Classy', 'url': '/classy', 'image': 'static/images/classyoutfit.jpg','code': 'A0634', 'price': 'Rs4000'}
]

# Products data (to be shown in each category page)
products_data = {
   'Aesthetic': [
    {'name': 'Pink Satin Blouse', 'image': 'static/images/a1.jpg', 'price': 'Rs4500', 'Code': 'A0123', 'short_description': 'A beautiful satin blouse for elegant evenings.'},
    {'name': 'Brown Chiffon Top', 'image': 'static/images/a2.jpg', 'price': 'Rs7700', 'Code': 'A0124', 'short_description': 'A lightweight Chiffon top perfect for casual wear.'},
    {'name': 'White Silk Top', 'image': 'static/images/a5.jpg', 'price': 'Rs5500', 'Code': 'A0125', 'short_description': 'A white silk top, a must-have for your wardrobe.'},
    {'name': 'Off White Silk Top', 'image': 'static/images/a8.jpg', 'price': 'Rs4000', 'Code': 'A0126', 'short_description': 'A sleek and elegant peach top, ideal for day to evening wear.'},
    {'name': 'Blue Grey Lida Top', 'image': 'static/images/a9.jpg', 'price': 'Rs3000', 'Code': 'A0127', 'short_description': 'A blue grey lida top perfect for elegand evening.'},
    {'name': 'Grey Silk Blouse', 'image': 'static/images/a10.jpeg', 'price': 'Rs6000', 'Code': 'A0128', 'short_description': 'A grey silk blouse, adding a touch of luxury to any outfit.'},
    {'name': 'Hot Pink Extra-Long Sleeve ', 'image': 'static/images/a3.jpg', 'price': 'Rs4500', 'Code': 'A0129', 'short_description': 'A long sleeve elegant  with beautiful design, perfect for occasions.'},
    {'name': 'Pink Silk Top', 'image': 'static/images/a20.jpg', 'price': 'Rs3700', 'Code': 'A0130', 'short_description': 'A stylish pink silk top, a perfect blend of comfort and class.'},
    {'name': 'Beige Silk Top', 'image': 'static/images/a12.jpeg', 'price': 'Rs6700', 'Code': 'A0131', 'short_description': 'A beige silk top with beautiful design pergect for occasions.'},
    {'name': 'Dark Green silk Top', 'image': 'static/images/a14.jpeg', 'price': 'Rs3000', 'Code': 'A0132', 'short_description': ' A delicate green silk top that adds charm to any casual outing.'},
    {'name': 'Maroon Blouse', 'image': 'static/images/a11.jpeg', 'price': 'Rs7500', 'Code': 'A0133', 'short_description':' A sophisticated maroon blouse perfect for formal gatherings.'},
    {'name': 'Ivory Silk Top', 'image': 'static/images/a15.jpg', 'price': 'Rs3100', 'Code': 'A0134', 'short_description': 'An ivory silk top with beautiful design.An ivory silk top for effortless elegance'},
    {'name': 'Blue Blouses', 'image': 'static/images/a16.jpg', 'price': 'Rs3899', 'Code': 'A0135', 'short_description': 'Chiffon Tops with an Elegant High Collar offering a smooth and luxurious feel.'},
    {'name': 'Soft Pink Blouse', 'image': 'static/images/a17.jpg', 'price': 'Rs3799', 'Code': 'A0136', 'short_description': 'A soft pink blouse that adds elegance to any outfit.'},
    {'name': 'Dark Grey Elegant Blouse', 'image': 'static/images/a18.jpg', 'price': 'Rs3500', 'Code': 'A0137', 'short_description': 'A dark grey top with full selves blouse for elegent evening'},
    {'name': 'Black Grey Silk Top', 'image': 'static/images/a13.jpg', 'price': 'Rs5799', 'Code': 'A0138', 'short_description': 'A classic black silk top, a must-have wardrobe essential.'},
    {'name': 'Purel Chiffon Blouse', 'image': 'static/images/a21.jpg', 'price': 'Rs6700', 'Code': 'A0139', 'short_description': 'A stunning purpel chiffon blouse for a bold and chic look.'},
    {'name': 'Orange Top', 'image': 'static/images/a22.jpg', 'price': 'Rs6100', 'Code': 'A0140', 'short_description': 'A delicate orange top perfect for evening elegance.'},
    {'name': 'Satin Long Shirt', 'image': 'static/images/a23.jpg', 'price': 'Rs3000', 'Code': 'A0141', 'short_description': 'A luxurious satin logn shirt for sophisticated gatherings.'},
    {'name': 'White Floral Top', 'image': 'static/images/a24.jpg', 'price': 'Rs4099', 'Code': 'A0142', 'short_description': 'A floral print white top, perfect for the spring season'}
],

   'Traditional': [
       {'name': 'Black Traditional Dress with Embellishments', 'image': 'static/images/t3.jpg', 'price': 'Rs10000', 'Code': 'A0143', 'short_description': 'A stunning black dress with vibrant embroidery.'},
        {'name': 'Traditional Red And Blue Dress', 'image': 'static/images/t4.jpg', 'price': 'Rs5000', 'Code': 'A0144', 'short_description': 'A beautiful maroon dress adorned with intricate traditional embroidery.'},
        {'name': 'Red Traditional Cape Beautiful Top', 'image': 'static/images/t11.jpg', 'price': 'Rs6000', 'Code': 'A0145', 'short_description': 'A luxurious red traditional cape with embroidery'},
        {'name': 'White Traditional Dress hite Embroidered Dress', 'image': 'static/images/t7.jpg', 'price': 'Rs6900', 'Code': 'A0146', 'short_description': 'A classic white dress with colorful embroidery and traditional adornments.'},
        {'name': 'Flower Embroidered Beautiful Dress ', 'image': 'static/images/t9.jpg', 'price': 'Rs8099', 'Code': 'A0147', 'short_description': 'A beige dress with floral embroidery, featuring beautiful patterns and design.'},
        {'name': 'Purple Traditional Dress', 'image': 'static/images/t6.jpg', 'price': 'Rs9000', 'Code': 'A0148', 'short_description': 'A purple dress with rich embroidery details and a flowing skirt.'},
        {'name': 'Black Embroidered Cloak', 'image': 'static/images/t12.jpg', 'price': 'Rs4500', 'Code': 'A0149', 'short_description': 'A stylish black cloak with colorful embroidery, offering elegance and comfort.'},
        {'name': 'Beige Traditional Dress', 'image': 'static/images/t13.jpg', 'price': 'Rs7099', 'Code': 'A0150', 'short_description': 'A sophisticated beige dress with traditional embroidery and tassel accents.'},
        {'name': 'Yellow Traditional Dress', 'image': 'static/images/t14.jpg', 'price': 'Rs5500', 'Code': 'A0151', 'short_description': 'A beautiful yellow dress with intricate embroidery on the borders.'},
        {'name': 'Green Traditional Dress', 'image': 'static/images/t15.jpg', 'price': 'Rs7500', 'Code': 'A0152', 'short_description': 'A stunning green dress with elegant traditional patterns and a luxurious feel.'},
        {'name': 'Yellow Traditional Dress with Embellishments', 'image': 'static/images/t25.jpg', 'price': 'Rs4500', 'Code': 'A0245', 'short_description': 'A golden yellow dress, featuring beautiful beadwork.'},
        {'name': 'Red Traditional Dress with Green Veil', 'image': 'static/images/t16.jpg', 'price': 'Rs5500', 'Code': 'A0246', 'short_description': 'A vibrant red traditional dress with intricate embroidery, paired with a veil.'},
        {'name': 'Black and White Traditional Dress', 'image': 'static/images/t22.jpg', 'price': 'Rs6000', 'Code': 'A0347', 'short_description': 'A sleek black and white dress with a mix of elegant patterns and stitching for a chic.'},
        {'name': 'Vibrant Red Traditional Dress For Grand Evening', 'image': 'static/images/t20.jpg', 'price': 'Rs40000', 'Code': 'A0348', 'short_description': ' A red traditional dress with beautiful patterns and a flattering silhouette.'},
        {'name': 'Sky Blue and hite Embroidered Dress', 'image': 'static/images/t21.jpg', 'price': 'Rs7000', 'Code': 'A0678', 'short_description': 'his dress combines sky blue and white with stunning embroidery.'},
        {'name': 'Elegant Red Beautiful Flowing Dress', 'image': 'static/images/t17.jpg', 'price': 'Rs7500', 'Code': 'A0648', 'short_description': 'A stunning flowing red dress that offers an elegant look.'},
        {'name': 'Traditional Blue Dress with White Embroidery', 'image': 'static/images/t23.jpg', 'price': 'Rs6500', 'Code': 'A0749', 'short_description': ' A beautiful blue traditional dress with delicate white embroidery.'},
        {'name': 'Green and Red Traditional Dress', 'image': 'static/images/t18.jpg', 'price': 'Rs8500', 'Code': 'A0950', 'short_description': ' A luxurious green and red dress with beautiful embellishments.'},
        {'name': 'Red Traditional Long Frock Dress', 'image': 'static/images/t19.jpg', 'price': 'Rs3500', 'Code': 'A0751', 'short_description': 'A luxurious black and red dress with beautiful embellishments.'},
        {'name': 'Green Traditional Dress With Simple Dupata', 'image': 'static/images/t24.jpg', 'price': 'Rs3500', 'Code': 'A0252', 'short_description': 'A stunning green dress with elegant traditional patterns and a luxurious feel.'},
    ],
    'Party Wear': [
        {'name': 'Navy Blue Sequin Gown', 'image': 'static/images/p1.jpg', 'price': 'Rs10000', 'Code': 'A0343', 'short_description': 'An elegant navy gown with sequin and satin mix, ideal for formal evenings.'},
        {'name': 'Blush Pink Embroidered Suit', 'image': 'static/images/p2.jpg', 'price': 'Rs5000', 'Code': 'A0444', 'short_description': 'A delicate pink outfit with silver threadwork and sheer sleeves graceful '},
        {'name': 'Red Velvet Evening Gown', 'image': 'static/images/p3.jpg', 'price': 'Rs6000', 'Code': 'A0645', 'short_description': 'A plush red gown with glitter detailing and puffed sleeves, perfect for evening wear.'},
        {'name': 'Powder Blue Pleated Dress', 'image': 'static/images/p4.jpg', 'price': 'Rs6900', 'Code': 'A0446', 'short_description': 'A soft chiffon gown with pleats and sheer sleeves, styled with a glittering belt.'},
        {'name': 'Mustard Yellow Sharara Suit', 'image': 'static/images/p5.jpg', 'price': 'Rs8099', 'Code': 'A0147', 'short_description': 'A vibrant sharara suit with embroidered kameez and wide pleated pants.'},
        {'name': 'Dusty Mauve Slit Kurta', 'image': 'static/images/p6.jpg', 'price': 'Rs9000', 'Code': 'A0138', 'short_description': 'A modern slit kurta with minimal embellishments and a sleek silhouette.'},
        {'name': 'Sea Green Palazzo Set', 'image': 'static/images/p7.jpg', 'price': 'Rs4500', 'Code': 'A0249', 'short_description': 'A breezy palazzo suit with floral borders and flared sleeves in soft green.'},
        {'name': 'Peach Gold Anarkali Suit', 'image': 'static/images/p8.jpg', 'price': 'Rs7099', 'Code': 'A0190', 'short_description': 'A peach Anarkali adorned with gold embroidery and a matching dupatta.'},
        {'name': 'Deep Plum Embroidered Suit', 'image': 'static/images/p9.jpg', 'price': 'Rs5500', 'Code': 'A0181', 'short_description': 'A rich purple suit with geometric and floral threadwork on flowy sharara pants.'},
        {'name': 'Mint Green Floral Anarkali', 'image': 'static/images/p10.jpg', 'price': 'Rs7500', 'Code': 'A0112', 'short_description': 'A pastel green floral embroidered Anarkali with a graceful long jacket style.'},
        {'name': 'Indigo Textured Ball Gown', 'image': 'static/images/p11.jpg', 'price': 'Rs45000', 'Code': 'A0245', 'short_description': 'A structured indigo gown with elegant texture and feathered floral accents, ideal for formal events.'},
        {'name': 'Plum Draped Chiffon Gown', 'image': 'static/images/p12.jpg', 'price': 'Rs5500', 'Code': 'A0146', 'short_description': 'A luxurious plum gown with layered chiffon and knot waist detail, exuding grace and elegance.'},
        {'name': 'Icy Blue Crystal Gown', 'image': 'static/images/p13.jpg', 'price': 'Rs6000', 'Code': 'A0747', 'short_description': 'An ethereal icy blue gown with a sparkling embellished bodice and flutter sleeves Looks Elegant.'},
        {'name': 'Mauve Hijab Formal Gown', 'image': 'static/images/p14.jpg', 'price': 'Rs40000', 'Code': 'A0318', 'short_description': ' A modest and flowing mauve gown with floral waist details and a glossy finish, perfect for hijabi fashion.'},
        {'name': 'Lavender Palazzo Jacket Set', 'image': 'static/images/p15.jpg', 'price': 'Rs7000', 'Code': 'A0618', 'short_description': 'A trendy lavender palazzo set with embroidered jacket and sheer elegance Looks Amazing.'},
        {'name': 'Boho Printed Cape Suit', 'image': 'static/images/p16.jpg', 'price': 'Rs7500', 'Code': 'A0698', 'short_description': 'A modern boho-style outfit featuring a white base and colorful floral printed cape.'},
        {'name': 'Pastel Green Shirt Collar', 'image': 'static/images/p17.jpg', 'price': 'Rs6500', 'Code': 'A5109', 'short_description': ' A unique pastel green gown styled with a shirt collar and subtle embroidery.'},
        {'name': 'Black Flared Sharara Set', 'image': 'static/images/p18.jpg', 'price': 'Rs8500', 'Code': 'A4190', 'short_description': 'A bold black sharara set with a heavily embroidered top and classic ethnic flair.'},
        {'name': 'Mint Green Ruffle Suit', 'image': 'static/images/p19.jpg', 'price': 'Rs3500', 'Code': 'A3141', 'short_description': 'A dreamy mint green ruffle suit with flared sleeves and detailed floral embroidery.'},
        {'name': 'Slate Grey Ruffle Gown', 'image': 'static/images/p20.jpg', 'price': 'Rs3500', 'Code': 'A2112', 'short_description': 'A graceful high-low slate grey gown with layered ruffles and a soft drape.'},

    ],
    'Classy': [
        {'name': 'Chic Blazer & Black Set', 'image': 'static/images/c1.jpg', 'price': 'Rs10000', 'Code': 'A0393', 'short_description': 'A stylish cropped beige blazer paired with a black crop top and high-waisted trousers—perfect for modern minimalism.'},
        {'name': 'Coffee Brown Elegance', 'image': 'static/images/c2.jpg', 'price': 'Rs5000', 'Code': 'A0414', 'short_description': 'An off-shoulder cocoa brown blouse tucked into matching pleated trousers for an effortlessly refined coastal look.'},
        {'name': 'Satin Noir Power Set', 'image': 'static/images/c3.jpg', 'price': 'Rs6000', 'Code': 'A0665', 'short_description': 'Sleek all-black satin top and tailored pants for a commanding and elegant statement outfit.'},
        {'name': 'Floral Romance & Wine Pants', 'image': 'static/images/c4.jpg', 'price': 'Rs6900', 'Code': 'A0046', 'short_description': 'Delicate floral blouse matched with high-waisted maroon trousers, balancing femininity with class.'},
        {'name': 'Ivory & Caramel Duo', 'image': 'static/images/c5.jpg', 'price': 'Rs8099', 'Code': 'A0157', 'short_description': 'An off-shoulder ivory top styled with wide-leg caramel trousers for a polished, bold presence.'},
        {'name': 'Beige Layered Winter Look', 'image': 'static/images/c6.jpg', 'price': 'Rs9000', 'Code': 'A0168', 'short_description': 'A ribbed turtleneck, pleated skirt, and overcoat set in warm beige tones for a cozy yet sophisticated winter vibe.'},
        {'name': 'Mocha Jumpsuit Power Look', 'image': 'static/images/c7.jpg', 'price': 'Rs4500', 'Code': 'A0279', 'short_description': 'A sleeveless mocha jumpsuit with a draped neckline—elegant and empowering in one piece.'},
        {'name': 'Navy Silk & Golden Pants', 'image': 'static/images/c8.jpg', 'price': 'Rs7099', 'Code': 'A0180', 'short_description': 'A navy satin wrap top cinched with a cream belt, paired with flowing golden trousers—luxury in motion.'},
        {'name': 'Olive & Camel Combo', 'image': 'static/images/c9.jpg', 'price': 'Rs5500', 'Code': 'A0191', 'short_description': 'A rich green puff-sleeve blouse combined with tailored camel trousers—earthy tones, elevated style.'},
        {'name': 'Amber Monochrome Statement', 'image': 'static/images/c10.jpg', 'price': 'Rs7500', 'Code': 'A0012', 'short_description': 'A coordinated amber off-shoulder sweater and tailored pants set, paired with a matching bag and heels for a striking look.'},
        {'name': 'Beige Wrap Knit Top with Camel Trousers', 'image': 'static/images/c11.jpg', 'price': 'Rs45000', 'Code': 'A0745', 'short_description': 'Elegant and cozy, this wrap sweater paired with tailored high-waist camel pants creates a sophisticated  comfortable look.'},
        {'name': 'Burnt Orange Blazer with Navy Trousers', 'image': 'static/images/c12.jpg', 'price': 'Rs5500', 'Code': 'A0446', 'short_description': 'A bold and modern power outfit, the bright orange blazer contrasts beautifully with navy pants  professional style.'},
        {'name': 'Lavender Belted Elegant Jumpsuit', 'image': 'static/images/c13.jpg', 'price': 'Rs6000', 'Code': 'A0547', 'short_description': 'Soft and graceful, this pastel jumpsuit with a tied waist offers a polished yet relaxed fit perfect for brunches or daytime events.'},
        {'name': 'Dusty Pink Monochrome Suit Set', 'image': 'static/images/c14.jpg', 'price': 'Rs40000', 'Code': 'A0518', 'short_description': ' This belted pink jumpsuit paired with a matching cape-style coat gives a chic and commanding presence, perfect for formal.'},
        {'name': 'Ivory Blouse with Red Wide-Leg Pants', 'image': 'static/images/c15.jpg', 'price': 'Rs7000', 'Code': 'A0918', 'short_description': 'Classic and vibrant, this crisp ivory blouse combined with bold red pants makes a timeless and confident statement.'},
        {'name': 'Sheer Nude Bow Blouse with Navy Pants', 'image': 'static/images/c16.jpg', 'price': 'Rs7500', 'Code': 'A0798', 'short_description': 'Feminine and refined, this look combines a sheer blouse with sleeves and a bow tie neckline with structured navy trousers.'},
        {'name': 'White Embroidered Top with Flared Camel Pants', 'image': 'static/images/c17.jpg', 'price': 'Rs6500', 'Code': 'A0809', 'short_description': ' A fusion of boho and retro, the embroidered top with dramatic flared pants brings back glamour with a modern touch.'},
        {'name': 'Mint Green Blazer with Taupe Slacks', 'image': 'static/images/c18.jpg', 'price': 'Rs8500', 'Code': 'A0890', 'short_description': 'Soft pastel layers create a calm and stylish professional outfit, enhanced by a sleek white top and warm accessories.'},
        {'name': 'Red Blazer Suit with White Shirt', 'image': 'static/images/c19.jpg', 'price': 'Rs3500', 'Code': 'A0941', 'short_description': 'A sharp and commanding suit in striking red, balanced with a soft white blouse and nude heels for a clean, modern finish.'},
        {'name': 'Camel Blazer and Pants with Black Turtleneck', 'image': 'static/images/c20.jpg', 'price': 'Rs3500', 'Code': 'A0912', 'short_description': 'Minimalist and elegant, the tailored camel suit paired with a black turtleneck delivers effortless luxury and power.'},
    ]
}
"""@app.route('/')
def splash():
    return render_template('splash.html')
@app.route('/splash2')
def splash2():
    return render_template('splash2.html')"""

# Route for the home page (after clicking "Let's Get Started")
@app.route('/')
def home():
    # Pass categories to home.html
    return render_template('home.html', categories=categories)

@app.route('/aesthetic')
def aesthetic():
    aesthetic_products = products_data.get('Aesthetic', [])
    return render_template('aesthetic.html', products=aesthetic_products, category="Aesthetic")

@app.route('/traditional')
def traditional():
    traditional_products = products_data.get('Traditional', [])
    return render_template('Traditional.html', products=traditional_products, category="Traditional")

@app.route('/partywear')
def partywear():
    partywear_products = products_data.get('Party Wear', [])
    return render_template('partywear.html', products=partywear_products, category="Party Wear")

@app.route('/classy')
def classy():
    classy_products = products_data.get('Classy', [])
    return render_template('classyoutfit.html', products=classy_products, category="Classy")

"""@app.route('/<category>')
def category_page(category):
    category_products = products_data.get(category.capitalize(), [])
    return render_template('category.html', products=category_products, category=category.capitalize())"""

@app.route('/addtocart', methods=['POST'])
def addtocart():
    # Retrieve product details from the form
    product_name = request.form.get('product_name')
    product_code = request.form.get('product_code')
    product_image = request.form.get('product_image')
    product_price = request.form.get('product_price')
    product_description = request.form.get('product_description')
    quantity = int(request.form.get('quantity', 1))

    item = {
    'name': product_name,
    'Code': product_code,
    'image': product_image,
    'price': product_price,  # Ensure price is passed here
    'short_description': product_description,
    'quantity': quantity
}

    # Add the item to the cart in session
    if 'cart' not in session:
        session['cart'] = []

    found = False
    for cart_item in session['cart']:
        if cart_item['Code'] == item['Code']:
            cart_item['quantity'] += quantity
            found = True
            break

    if not found:
        session['cart'].append(item)

    # Recalculate total amount for the cart
    total_amount = sum(float(item['price'].replace('Rs', '').strip()) * item['quantity'] for item in session['cart'])

    # Store the total amount in the session
    session['total_amount'] = total_amount

    # Redirect to the correct category page
    category = request.form.get('category')  # Get the category from the form
    categories_list = ['aesthetic', 'traditional', 'partywear', 'classy']

    if category not in categories_list:
        category = 'aesthetic' 
        
        
         # Default category in case of invalid category

    return redirect(url_for(category))  # Redirect to the selected category page

@app.route('/final_cart')
def final_cart():
    # Retrieve the cart from the session
    cart = session.get('cart', [])
    total_amount = session.get('total_amount', 0)
    return render_template('final_cart.html', cart=cart, total_amount=total_amount)


@app.route('/remove_item/<product_code>', methods=['GET', 'POST'])
def remove_item(product_code):
    cart = session.get('cart', [])
    
    # Remove item with the given product code
    session['cart'] = [item for item in cart if item['Code'] != product_code]
    
    # Recalculate total amount for the updated cart
    total_amount = sum(float(item['price'].replace('Rs', '').strip()) * item['quantity'] for item in session['cart'])
    
    # Store the updated total amount in the session
    session['total_amount'] = total_amount
    
    # Return a response (redirecting back to the final cart page)
    return redirect(url_for('final_cart'))  # Redirect to final cart page after removing item

@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    product_code = request.form['product_code']
    new_quantity = int(request.form['quantity'])

    # Find the product in the cart and update its quantity
    for item in session['cart']:
        if item['Code'] == product_code:
            item['quantity'] = new_quantity
            break

    # Recalculate total amount for the cart
    total_amount = sum(float(item['price'].replace('Rs', '').strip()) * item['quantity'] for item in session['cart'])
    session['total_amount'] = total_amount

    return jsonify({'total_amount': total_amount})
 
@app.route('/product_order', methods=['GET', 'POST'])
def product_order():
    cart = session.get('cart', [])
    total = sum(float(item['price'].replace('Rs', '').strip()) * item['quantity'] for item in cart)
    grand_total = total + 250
    return render_template('product_order.html', cart=cart, total=total, grand_total=grand_total)
def add_order_date_column():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "orders.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if the column exists first to avoid errors
    cursor.execute("PRAGMA table_info(orders);")
    columns = [column[1] for column in cursor.fetchall()]

    if "order_date" not in columns:
        cursor.execute("""
            ALTER TABLE orders ADD COLUMN order_date TEXT;
        """)
        conn.commit()
        print("order_date column added successfully.")

    conn.close()

# Call this function when the app starts (only once for setup)
add_order_date_column()

# Final submit route
@app.route('/submit_order', methods=['POST'])
def submit_order():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address1 = request.form.get('address1')
    address2 = request.form.get('address2')
    address3 = request.form.get('address3')
    order_date = request.form.get('order_date')
    payment_method = request.form.get('payment_method')

    # Validate the order_date (Ensure it is in the correct format: YYYY-MM-DD)
    try:
        if order_date:
            datetime.strptime(order_date, '%Y-%m-%d')  # Check if the date format is valid
        else:
            order_date = datetime.now().strftime('%Y-%m-%d')  # Set the current date if not provided
    except ValueError:
        return "Invalid date format. Please use YYYY-MM-DD."

    cart = session.get('cart', [])
    total_amount = session.get('total_amount', 0)

    # Check required fields
    if not all([name, email, phone, address1]):
        return "Please fill all required fields."

    if not cart:
        return "Cart is empty."

    # Correct path to your SQLite database
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "orders.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert each cart item
    for item in cart:
        cursor.execute("""
            INSERT INTO orders (
                name, email, phone, address1, address2, address3, payment_method,
                product_name, product_code, product_price, quantity, total_price, order_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name, email, phone, address1, address2, address3, payment_method,
            item['name'], item['Code'], float(item['price'].replace('Rs', '').strip()),
            item['quantity'],
            float(item['price'].replace('Rs', '').strip()) * item['quantity'],
            order_date
        ))

    conn.commit()
    conn.close()

    # Clear cart after successful order
    session.pop('cart', None)
    session.pop('total_amount', None)

    return redirect(url_for('order_success'))

@app.route('/order_success')
def order_success():
    return render_template('order_success.html')
if __name__ == '__main__':
    app.run(debug=True)