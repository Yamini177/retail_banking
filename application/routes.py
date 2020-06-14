from application import app, db
from flask import render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(20))
    password = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=datetime.now)

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssn_id = db.Column(db.Integer)
    cname = db.Column(db.String(20))
    age = db.Column(db.Integer)
    address = db.Column(db.Integer)
    state = db.Column(db.String(20))
    city = db.Column(db.String(20))

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form['email']
        uname = request.form['uname']
        password = request.form['pass']
        cnfrm_password = request.form['cpass']

        query = Employees.query.filter_by(uname = uname).first()

        if query != None:
            if uname == str(query.uname):
                flash('Username already taken')
                return redirect( url_for('registration') )
        
        if password != cnfrm_password:
            flash('Password do not match')
            return redirect( url_for('registration') )

        user = Employees(uname = uname, password = password)
        db.session.add(user)
        db.session.commit()
        flash('Registration was successfull', category='info')
        return redirect( url_for('login') )
    return render_template('emp_registration.html')

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect( url_for('home') )

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        emp = Employees.query.filter_by(uname=username).first()
        if emp == None:
            flash('Invalid Credentials. Check User Name and Password', category='error')
            return redirect( url_for('login') )
        elif username == emp.uname and password == emp.password:
            session['username'] = username
            return redirect( url_for('home') )
        else:
            flash('Invalid Credentials. Check User Name and Password', category="error")

    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        flash('You are logged out. Please login again to continue')
        return redirect( url_for('login') )

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been successfully logged out.')
    return redirect( url_for('login') )

@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
    if 'username' in session:
        if request.method == 'POST':
            ssn_id = request.form['ssn_id']
            cname = request.form['cname']
            age = request.form['age']
            address = request.form['address']
            state = request.form['state']
            city = request.form['city']

            customer = Customers(ssn_id=ssn_id, cname=cname, age=age, address=address, state=state, city=city)
            db.session.add(customer)
            db.session.commit()
            flash('Customer added successfully')
            return redirect( url_for('create_customer') )
    else:
        flash('You are logged out. Please login again to continue')
        return redirect( url_for('login') )

    return render_template('create_customer.html')

@app.route('/search_customer', methods=['GET', 'POST'])
def search_customer():
    if 'username' in session:
        if request.method == 'POST':
            ssn_id = request.form['ssn_id']
            customer = Customers.query.filter_by(ssn_id = ssn_id).first()
            if customer == None:
                flash('No customer with that ssn_id exists')
                return redirect( url_for('search_customer') )
            else:
                flash('Following details found')
                return render_template('customer_found.html', customer = customer)
    
    else:
        return redirect( url_for('login') )
    
    return render_template('search_customer.html')

@app.route('/customer_found')
def customer_found():
    if 'username' in session:
        return render_template('customer_found.html')
    else:
        return redirect( url_for('login') )

@app.route('/delete_customer', methods=['GET', 'POST'])
def delete_customer():
    if 'username' in session:
        if request.method == 'POST':
            ssn_id = request.form['ssn_id']
            customer_id = request.form['customer_id']
            customer_name = request.form['customer_name']
            age = request.form['age']
            address = request.form['address']

            customer = Customers.query.filter_by(ssn_id = ssn_id).first()
            if customer == None or str(customer.id) != customer_id or str(customer.ssn_id) != ssn_id or str(customer.cname) != customer_name or str(customer.age) != age or str(customer.address) != address:
                flash('No customer with that that details found. Please enter correct details')
                return redirect( url_for('delete_customer') )
            else:
                db.session.delete(customer)
                db.session.commit()
                flash('Successfully deleted customer')
                return redirect( url_for('delete_customer') )
    
    return render_template('delete_customer.html')

# TODO Complete view function
@app.route('/update_customer')
def update_customer():
    return render_template('update_customer.html')

# TODO Complete
@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/delete_all', methods=['GET', 'POST'])
def delete_all():
    if request.method == 'POST':
        db.session.query(Employees).delete()
        db.session.commit()
        db.session.query(Customers).delete()
        db.session.commit()
        flash('Deleted all customers record')
        return render_template('delete_all.html')
    return render_template('delete_all.html')
