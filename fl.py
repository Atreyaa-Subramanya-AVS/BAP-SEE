from flask import Flask, render_template, flash, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

def get_db_connection():
    conn = sqlite3.connect('property.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS properties (
                   id INTEGER PRIMARY KEY,
                   description TEXT NOT NULL,
                   dimensions TEXT NOT NULL,
                   facing TEXT NOT NULL,
                   property_type TEXT NOT NULL,
                   rent INTEGER NOT NULL,
                   address TEXT NOT NULL,
                   parking TEXT,
                   bhk INTEGER,
                   overlooking TEXT,
                   floors INTEGER,
                   furnishing TEXT,
                   amenities TEXT,
                   flooring TEXT,
                   climate_control TEXT,
                   balcony TEXT,
                   ups TEXT,
                   purchased TEXT DEFAULT 'No',
                   name TEXT DEFAULT NULL,
                   mail TEXT DEFAULT NULL,
                   phno TEXT DEFAULT NULL,
                   img1_path TEXT,
                   img2_path TEXT,
                   img3_path TEXT,
                   img4_path TEXT,
                   img5_path TEXT,
                   img6_path TEXT
    )''')
    conn.commit()
    conn.close()

create_table()

# @app.route('/')
# def home():
#     return render_template('home.html')

@app.route('/')
def home():
    return render_template('auth.html')

@app.route('/client')
def client():
    return render_template('client.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/add_property', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        description = request.form.get('description', '')
        dimensions = request.form.get('dimensions', '')
        facing = request.form.get('facing', '')
        property_type = request.form.get('property_type', '')
        rent = int(request.form.get('rent', 0))
        address = request.form.get('address', '')
        parking = request.form.get('parking', '')
        bhk = int(request.form.get('bhk', 0))
        overlooking = request.form.get('overlooking', '')
        floors = int(request.form.get('floors', 0))
        furnishing = request.form.get('furnishing', '')
        amenities = request.form.get('amenities', '')
        flooring = request.form.get('flooring', '')
        climate_control = request.form.get('climate_control', '')
        balcony = request.form.get('balcony', '')
        ups = request.form.get('ups', '')

        img1 = request.files.get('img1')
        img2 = request.files.get('img2')
        img3 = request.files.get('img3')
        img4 = request.files.get('img4')
        img5 = request.files.get('img5')
        img6 = request.files.get('img6')
        img1_path = ''
        img2_path = ''
        img3_path = ''
        img4_path = ''
        img5_path = ''
        img6_path = ''

        if img1:
            img1_path = os.path.join('static', img1.filename)
            img1.save(img1_path)
        if img2:
            img2_path = os.path.join('static', img2.filename)
            img2.save(img2_path)
        if img3:
            img3_path = os.path.join('static', img3.filename)
            img3.save(img3_path)
        if img4:
            img4_path = os.path.join('static', img4.filename)
            img4.save(img4_path)
        if img5:
            img5_path = os.path.join('static', img5.filename)
            img5.save(img5_path)
        if img6:
            img6_path = os.path.join('static', img6.filename)
            img6.save(img6_path)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO properties (description, dimensions, facing, property_type, rent, address, parking, bhk, overlooking, floors,
                                furnishing, amenities, flooring, climate_control, balcony, ups, img1_path, img2_path, img3_path, img4_path, img5_path, img6_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (description, dimensions, facing, property_type, rent, address, parking, bhk, overlooking, floors, furnishing, amenities, flooring, climate_control, balcony, ups, img1_path, img2_path, img3_path, img4_path, img5_path, img6_path))
        conn.commit()
        conn.close()
        return redirect(url_for('view_property'))
    return render_template('add_property.html')

@app.route('/edit_property/<int:property_id>', methods=['GET', 'POST'])
def edit_property(property_id):
    if request.method == 'POST':
        description = request.form.get('description', '')
        dimensions = request.form.get('dimensions', '')
        facing = request.form.get('facing', '')
        property_type = request.form.get('property_type', '')
        rent = int(request.form.get('rent', 0))
        address = request.form.get('address', '')
        parking = request.form.get('parking', '')
        bhk = int(request.form.get('bhk', 0))
        overlooking = request.form.get('overlooking', '')
        floors = int(request.form.get('floors', 0))
        furnishing = request.form.get('furnishing', '')
        amenities = request.form.get('amenities', '')
        flooring = request.form.get('flooring', '')
        climate_control = request.form.get('climate_control', '')
        balcony = request.form.get('balcony', '')
        ups = request.form.get('ups', '')
        purchased = request.form.get('purchased', 'No')

        current_img_paths = [request.form.get(f'current_img{i}_path', '') for i in range(1, 7)]

        img_paths = []
        for i in range(1, 7):
            img = request.files.get(f'img{i}')
            if img:
                img_path = os.path.join('static', img.filename)
                img.save(img_path)
                img_paths.append(img_path)
            else:
                img_paths.append(current_img_paths[i-1])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE properties
            SET description=?, dimensions=?, facing=?, type=?, rent=?, address=?, parking=?, bhk=?, overlooking=?, floors=?,
                furnishing=?, amenities=?, flooring=?, climate_control=?, balcony=?, ups=?, purchased=?, 
                img1_path=?, img2_path=?, img3_path=?, img4_path=?, img5_path=?, img6_path=?
            WHERE id=?
        ''', (description, dimensions, facing, property_type, rent, address, parking, bhk, overlooking, floors, furnishing, amenities, flooring, climate_control, balcony, ups, purchased, *img_paths, property_id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('view_property'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM properties WHERE id = ?', (property_id,))
    property = cursor.fetchone()
    conn.close()
    
    if property:
        return render_template('edit_property.html', property=property)
    else:
        flash("Property not found for the given ID.")
        return redirect(url_for('view_property'))

@app.route('/view_property')
def view_property():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM properties')
    properties = cursor.fetchall()
    conn.close()
    return render_template('view_property.html', properties=properties)

@app.route('/client/view_property_client')
def view_property_client():
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM properties')
    properties=cursor.fetchall()
    conn.close()
    return render_template('view_property_client.html',properties=properties)

@app.route('/property/<int:property_id>')
def property(property_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM properties WHERE id = ?', (property_id,))
    property = cursor.fetchone()
    conn.close()
    if property:
        return render_template('property.html', property=property)
    else:
        flash("Property not found for the given ID.")
        return redirect(url_for('view_property'))

@app.route('/home/view_by_place', methods=['GET', 'POST'])
def view_by_place():
    if request.method == 'POST':
        property_address = request.form.get('property_address', '')
        conn = get_db_connection()
        cursor = conn.cursor()
        prop_address = '%' + property_address + '%'
        cursor.execute('SELECT * FROM properties WHERE address LIKE ?', (prop_address,))
        properties = cursor.fetchall()
        conn.close()
        return render_template('view_by_place.html', properties=properties)
    return render_template('view_by_place.html', properties=[])

@app.route('/delete_property/<int:property_id>', methods=['POST'])
def delete_property(property_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT img1_path, img2_path, img3_path, img4_path, img5_path, img6_path FROM properties WHERE id = ?', (property_id,))
    paths = cursor.fetchone()
    cursor.execute('DELETE FROM properties WHERE id = ?', (property_id,))
    conn.commit()
    conn.close()

    for path in paths:
        if path:
            os.remove(path)

    return redirect(url_for('view_property'))


@app.route('/thanks')
def thanks():
    name = request.args.get('name', '')
    return render_template('thanks.html')


 
if __name__ == '__main__':
    app.run(debug=True)
