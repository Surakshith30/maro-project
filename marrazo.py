from flask import Flask, render_template, request, url_for, redirect, flash
from flask import *  
from flask import session
from flask_sqlalchemy import SQLAlchemy
from forms import BillingForm, ShippingForm , PaymentForm
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
# import update
import sqlite3
from datetime import datetime

import os
import psycopg2

app = Flask(__name__)
app.secret_key = "wkfw"  
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///site.db"
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Billing(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    bfname = db.Column(db.String(20),  nullable=False)
    blname = db.Column(db.String(20),  nullable=False)
    billing_address = db.Column(db.String(50),  nullable=False)
    bstate = db.Column(db.String(20), nullable=False)
    bcity = db.Column(db.String(20), nullable=False)
    bpincode = db.Column(db.Integer, nullable=False)
    #carts = db.relationship('Cart', backref='shopper_cart',lazy = True)
    def __repr__(self):
        return f"Billing('{self.bfname}','{self.blname}')"

class Shipping(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    sfname = db.Column(db.String(20),  nullable=False)
    slname = db.Column(db.String(20),  nullable=False)
    shipping_address = db.Column(db.String(50),  nullable=False)
    fstate = db.Column(db.String(20), nullable=False)
    fcity = db.Column(db.String(20), nullable=False)
    fpincode = db.Column(db.Integer, nullable=False)
    #carts = db.relationship('Cart', backref='shopper_cart',lazy = True)
    def __repr__(self):
        return f"Billing('{self.sfname}','{self.slname}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name=db.Column(db.String(30),nullable = False)
    product_cost = db.Column(db.Integer, nullable = False)
    product_quantity=db.Column(db.Integer, nullable = False)
    #carts = db.relationship('Cart', backref='product_cart', lazy=True)
    def __repr__(self):
        return f"Product('{self.id}','{self.product_name}','{self.product_cost}','{self.product_quantity}')"

#class Cart(db.Model):
 #   id = db.Column(db.Integer, primary_key = True)
  #  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   # product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable = False)
    #def __repr__(self):
     #   return f"Cart('{self.id}','{self.user_id}','{self.product_id}')"


add_to_cart = {1:3, #product_id : product_quantity
        2:5}
cart_details={'total_amt':0,
              'products':0}
temp_list = []

@app.route("/checkout", methods=['GET','POST'])
def checkout(add_to_cart=add_to_cart):
    form = BillingForm()
    for key in add_to_cart.keys():
        result =db.session.query(Product).filter(Product.id==key)
        for r in result:
            temp = {'id': r.id, 'product_name': r.product_name, 'product_cost': r.product_cost,
                    'product_quantity': r.product_quantity, }
            temp_list.append(temp)
    cart_details['products']=temp_list

    print(cart_details['products'])
    if form.validate_on_submit():
        bill = Billing(bfname = form.bfname.data, blname = form.blname.data, billing_address = form.billing_address.data,
                       bstate=form.bstate.data, bcity = form.bcity.data, bpincode = form.bpincode.data )
        db.session.add(bill)
        db.session.commit()
        flash('success', 'success')
        print("done")
        return redirect(url_for('checkout'))
    print(form.errors)
    return render_template("checkout 3.html", form=form, cart_details= cart_details)


#@app.route("/checkout-shipping", methods=['GET','POST'])
#def shipping():
 #   form = ShippingForm()
  #  print(form.errors)
   # if form.validate_on_submit():
    #    flash('success', 'success')
     #   print("done")
      #  return redirect(url_for('payment'))
    #print(form.errors)
    #return render_template("checkout2.html", form=form)


#@app.route("/checkout-payment", methods=['GET','POST'])
#def payment():
 #   form = PaymentForm()
  #  print(form.errors)
   # if form.validate_on_submit():
    #    flash('success', 'success')
     #   print("done")
      #  return redirect(url_for('checkout'))
    #print(form.errors)
    #return render_template("checkout3.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# def get_db_connection():
#     with sqlite3.connect('dbms.db') as conn:
#         cur = conn.cursor()
#     return conn
    
    
# @app.before_request
# def before_request_func():
#     print("before_request executing!")
    

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# @app.route('/home.html', methods=['POST'])
# def index():
#     if 'email' in session:
#         return redirect(url_for('logout'))
#     return redirect(url_for('login'))

@app.route("/sign-in")
def signin():
    return render_template("sign-in.html")

# @app.route("/login", methods=['POST'])
# def get_email():
#     return isp_query
@app.route("/login", methods=['GET','POST'])
def login():
    print("=======================================================================================")
    with sqlite3.connect('dbms.db') as conn:
        cur = conn.cursor()
        email_id= request.form["email_id"]
    #     em_id=email_id
        session['email_id']=email_id.lower()
        pwd = request.form["pwd"]
#         conn = get_db_connection()
        cur_in=conn.cursor()
        cur_pwd=conn.cursor()
#         cur = conn.cursor()
        cur_name=conn.cursor()
        cur_date=conn.cursor()
        cur_details=conn.cursor()
        cur_email=conn.cursor()
        cur_get_all=conn.cursor()
        current_email=conn.cursor()
        email_id=email_id.lower()
    #         global  params
        params = [email_id]
        pswd=[pwd]
        em_id=str(session['email_id'])

        # cursor return affected rows
        cur.execute('select count(email_id) from signup where email_id=?', params)# prevent SqlInject
#         print(count)
        cur_pwd.execute('select password from signup where email_id=?',params)
        cur_name.execute('select name from signup where email_id=?',params)
        cur_details.execute('select id from signup where email_id=?',params)
        cur_email.execute('select email_id from signup where email_id=?',params)
        cur_date.execute("SELECT datetime('now','localtime') as timestamps;")
#         date_time=cur_date.fetchone()
        date_time=cur_date.fetchone()
        datetime_object = datetime.strptime(date_time[0], '%Y-%m-%d %H:%M:%S')
        date_time=datetime_object.strftime("%Y-%m-%d, %H:%M:%S")
        get_id=cur_details.fetchone()
        get_email=cur_email.fetchone()
        name_get=cur_name.fetchone()
        print(get_id)
        count_pwd=cur_pwd.fetchone()
        count=cur.fetchone()
#         print(count[0])
        if count[0] < 0:
            # count 0 email 
    #         redirect(url_for('addperson'))
            return redirect(url_for('signin'))
        elif count[0] < 0 or count_pwd[0]!=pwd:
            conn.commit()
            cur.close()
            #conn.close()
            return redirect(url_for('signin'))
        else:
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            current_email.execute('select count(email_id) from signin where email_id=?',params)
            count_email_id=current_email.fetchone()
            if count_email_id[0]<1:
                cur_get_all.execute('insert into signin (id,email_id,last_visited,logout_time)'
                           'values(?,?,?,?)',(get_id[0],em_id,date_time,date_time))
                conn.commit()
#                 cur_get_all.close()
                #conn.close()
            else:
                cur_get_all.execute("update signin set last_visited='{0}' where email_id='{1}'".format(date_time,em_id))
                conn.commit()
#                 cur_get_all.close()
                #conn.close()
    #         logout_entry()
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    #         cur_in.execute('insert into signin (id,email_id,last_visited,logout_time)'
    #                    'values(%s,%s,%s,%s)',(get_id,get_email,date_time,date_time))
#             flash('Welcome'+" "+name_get[0].capitalize())
            flash(name_get[0],'category1')
            flash('Welcome'+" "+session['email_id'],'category2')
        return render_template('home.html',response=session['email_id']) # redirect(url_for('home'))
    
# @app.after_request

def logout_entry():
#     if 'email_id' not in session:
#         return redirect(url_for('login'))
#         email_id =request.args.get("email_id")
#     global em_id
#     print(type(session['email_id']))
#     print('sdknkdnsds')
#     em_id=session.get('email_id')
#     print(email_id)
    with sqlite3.connect('dbms.db') as conn:
        cur = conn.cursor()
#         cur=conn.cursor()
        cur_date=conn.cursor()
        cur_details=conn.cursor()
        cur_email=conn.cursor()
        print(session['email_id'])
        em_id=str(session['email_id'])
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")    
    #     cur_details.execute('select id from signup where email_id={s}',em_id)
    #     cur_email.execute('select email_id from signup where email_id=%s',em_id)
    #     cur_date.execute("SELECT (current_timestamp AT TIME ZONE 'UTC'+'05:30') as timestamps;")
    #     date_time=cur_date.fetchone()
    #     get_id=cur_details.fetchone()
    #     get_email=cur_email.fetchone()
    #     cur.execute('update signin set logout_time=%s where email_id=%s',[date_time,em_id])
        cur_details.execute("select id from signup where email_id='{0}'".format(em_id))
        cur_email.execute("select email_id from signup where email_id='{0}'".format(em_id))
        cur_date.execute("SELECT datetime('now','localtime') as timestamps")
        date_time=cur_date.fetchone()
        get_id=cur_details.fetchone()
        get_email=cur_email.fetchone()
        datetime_object = datetime.strptime(date_time[0], '%Y-%m-%d %H:%M:%S')
        date_time=datetime_object.strftime("%Y-%m-%d, %H:%M:%S")
        cur.execute("update signin set logout_time='{0}'where email_id='{1}'".format(date_time,em_id))
        conn.commit()
        #conn.close()

#     return response

#@app.route('/logout',methods=['GET','POST'])
#def logout():
#     conn = get_db_connection()
#     cur=conn.cursor()
#     cur_date=conn.cursor()
#     cur_details=conn.cursor()
#     cur_email=conn.cursor()
#     if 'email_id' not in session:
#         return redirect(url_for('login'))
#         email_id =request.args.get("email_id")
#     global em_id
#     print(type(session['email_id']))
    
#     em_id=session.get('email_id')
#     print(em_id)
#     cur_details.execute('select id from signup where email_id=%s',em_id)
#     cur_email.execute('select email_id from signup where email_id=%s',em_id)
#     cur_date.execute("SELECT (current_timestamp AT TIME ZONE 'UTC'+'05:30') as timestamps;")
#     date_time=cur_date.fetchone()
#     get_id=cur_details.fetchone()
#     get_email=cur_email.fetchone()
#     cur.execute('update signin set logout_time=%s where email_id=%s',[date_time,q])
    print("*****************************************************************************")
    logout_entry()
    session.pop('email_id',None)
    return redirect(url_for('home'))

   
# @app.route('/home.html', methods=['POST'])
# def index():
#     login=False
#     if 'email' in session:
#         login=True
#         return render_template('home.html',login=login)

# @app.route("/addToCart")
# def addToCart():
#     if 'email_id' not in session:
#         return redirect(url_for('signin'))
#     else:
#         productId = int(request.args.get('productId'))
# #         with sqlite3.connect('dbms.db') as conn:
# #             cur = conn.cursor()
#             cur.execute("SELECT id FROM signin WHERE email_id = ?", (session['email_id'], ))
#             userId = cur.fetchone()[0]
#             try:
#                 cur.execute("INSERT INTO customer_cart (id,email_id,product_id) VALUES (?, ?)", (userId,email_id,productId))
#                 conn.commit()
#                 msg = "Added successfully"
#             except:
#                 conn.rollback()
#                 msg = "Error occured"
#         #conn.close()
#         return redirect(url_for('home'))
    
# @app.route("/shopping-cart")
# def cart():
#      email = "pratiksha@gmail.com"
#      cur = conn.cursor()
#      params=[email]
#      cur.execute("SELECT email_id FROM signin WHERE email_id = %s",params)
#      email_Id = cur.fetchone()[0]
#      cur.execute("SELECT product_id,product_type,category,sub_category,product_name,price,label,rating,image,description = %s",email_Id)
#      products = cur.fetchall()
#      totalPrice = 0
#      for row in products:
#          totalPrice += row[2]
#      return render_template("shopping-cart.html")


@app.route("/create_account/", methods=['GET','POST'])
def create_account():
    with sqlite3.connect('dbms.db') as conn:
        cur = conn.cursor()
        email_id = request.form["email_id"]
        Name = request.form["Name"]
        Phone = request.form["Phone"]
        pwd = request.form["pwd"]
        cpwd = request.form["cpwd"]
#         conn = get_db_connection()
#         cur = conn.cursor()
        cur_date=conn.cursor()
        count_row=conn.cursor()
        params = [email_id]
        # cursor return affected rows
        count_row.execute('select count(*) from signup')
        cur.execute('select count(email_id) from signup where email_id=?', params)  # prevent SqlInject
    #     print(count)
        cur_date.execute("SELECT datetime('now','localtime') as timestamps;")
        ids=count_row.fetchone()
        ids=ids[0]+1
        print(ids)
        date_time=cur_date.fetchone()
        datetime_object = datetime.strptime(date_time[0], '%Y-%m-%d %H:%M:%S')
        date_time=datetime_object.strftime("%Y-%m-%d, %H:%M:%S")
        count=cur.fetchone()
    #     print(count[0])
        if count[0] > 0:
            # count 0 email
            return redirect(url_for('signin'))
        else:
    #         cur.execute('select email_id from signin ')
            cur.execute('INSERT INTO signup (Id,email_id, name,phone_number,password,confirm_password,created_at,modified_at)'
                        'VALUES (?,?,?,?,?,?,?,?)',
                        (ids,email_id, Name,Phone,pwd,cpwd,date_time,date_time))
            conn.commit()
            cur.close()
            #conn.close()
    return redirect(url_for('signin'))

# @app.route("/home.html")
# def home():
#     return render_template("home.html")
@app.route("/header.html")
def header():
    return render_template("header.html") 
    
@app.route("/shirts.html")
def shirts():
    return render_template("shirts.html") 
    
@app.route("/mens_shirt1-0001.html")
def mens_shirt1():
    # conn = get_db_connection()
    # cur_name=conn.cursor()
    # params=[session['email_id'].lower()]
    # cur_name.execute('select name from signup where email_id=(%s)',params)
    # name_get=cur_name.fetchone()
    # flash(session['email_id'],'category1')
    # flash(('Welcome'+" "+ name_get[0]),'category2')
    return render_template("mens_shirt1-0001.html")      
   
@app.route("/mens_shirt2-0002.html")
def mens_shirt2():
    return render_template("mens_shirt2-0002.html")

@app.route("/mens_shirt3-0003.html")
def mens_shirt3():
    return render_template("mens_shirt3-0003.html")    

@app.route("/mens_shirt4-0004.html")
def mens_shirt4():
    return render_template("mens_shirt4-0004.html")    

@app.route("/mens_shirt5-0005.html")
def mens_shirt5():
    return render_template("mens_shirt5-0005.html")  

@app.route("/mens_shirt6-0006.html")
def mens_shirt6():
    return render_template("mens_shirt6-0006.html")

@app.route("/mens_shirt7-0007.html")
def mens_shirt7():
    return render_template("mens_shirt7-0007.html") 
    
@app.route("/mens_shirt8-0008.html")
def mens_shirt8():
    return render_template("mens_shirt8-0008.html") 

@app.route("/mens_shirt9-0009.html")
def mens_shirt9():
    return render_template("mens_shirt9-0009.html") 


@app.route("/mens_shirt10-0010.html")
def mens_shirt10():
    return render_template("mens_shirt10-0010.html")       
  
@app.route("/mens_shirt11-0011.html")
def mens_shirt11():
    return render_template("mens_shirt11-0011.html")
    
@app.route("/mens_shirt12-0012.html")
def mens_shirt12():
    return render_template("mens_shirt12-0012.html")
    
@app.route("/mens_shirt13-0013.html")
def mens_shirt13():
    return render_template("mens_shirt13-0013.html")

@app.route("/mens_shirt14-0014.html")
def mens_shirt14():
    return render_template("mens_shirt14-0014.html")  

@app.route("/mens_shirt15-0015.html")
def mens_shirt15():
    return render_template("mens_shirt15-0015.html")
    
@app.route("/mens_shirt16-0016.html")
def mens_shirt16():
    return render_template("mens_shirt16-0016.html")
     
@app.route("/shopping-cart.html")
def cart():
    return render_template("shopping-cart.html")
  
# @app.route("/checkout.html")
# def checkout():
#     return render_template("checkout.html")

@app.route("/Mens_shose.html")
def Mshose():
    return render_template("Mens_shose.html") 
    
    
@app.route("/woman_handbags.html")
def whandbags():
    return render_template("woman_handbags.html") 
 
@app.route("/toys.html")
def toys():
    return render_template("toys.html") 

@app.route("/toy1.html")
def toy1():
    return render_template("toy1.html")

@app.route("/mens_Shoes-0017.html")
def shose1():
    return render_template("mens_Shoes-0017.html")

@app.route("/mens_Shoes-0018.html")
def shose2():
    return render_template("mens_Shoes-0018.html")
    
@app.route("/mens_Shoes-0019.html")
def shose3():
    return render_template("mens_Shoes-0019.html")

@app.route("/mens_Shoes-0020.html")
def shose4():
    return render_template("mens_Shoes-0020.html")

@app.route("/mens_Shoes-0021.html")
def shose5():
    return render_template("mens_Shoes-0021.html")

@app.route("/mens_Shoes-0022.html")
def shose6():
    return render_template("mens_Shoes-0022.html")

@app.route("/mens_Shoes-0023.html")
def shose7():
    return render_template("mens_Shoes-0023.html")
    
@app.route("/mens_Shoes-0024.html")
def shose8():
    return render_template("mens_Shoes-0024.html")    
    
@app.route("/mens_Shoes-0025.html")
def shose9():
    return render_template("mens_Shoes-0025.html")
    
@app.route("/mens_Shoes-0026.html")
def shose10():
    return render_template("mens_Shoes-0026.html")
    
@app.route("/mens_Shoes-0027.html")
def shose11():
    return render_template("mens_Shoes-0027.html")
 
@app.route("/mens_Shoes-0028.html")
def shose12():
    return render_template("mens_Shoes-0028.html")
    
@app.route("/mens_Shoes-0029.html")
def shose13():
    return render_template("mens_Shoes-0029.html")
    
@app.route("/mens_Shoes-0030.html")
def shose14():
    return render_template("mens_Shoes-0030.html")
    
@app.route("/mens_Shoes-0031.html")
def shose15():
    return render_template("mens_Shoes-0031.html")

@app.route("/mens_Shoes-0032.html")
def shose16():
    return render_template("mens_Shoes-0032.html")
    
@app.route("/toys.html")
def toy():
    return render_template("toys.html")
    
@app.route("/toys1-0129.html")
def toys1():
    return render_template("toys1-0129.html")
    
@app.route("/toys2-0130.html")
def toys2():
    return render_template("toys2-0130.html")
  
@app.route("/toys3-0131.html")
def toys3():
    return render_template("toys3-0131.html")
    
@app.route("/toys4-0132.html")
def toys4():
    return render_template("toys4-0132.html")
   
@app.route("/toys5-0133.html")
def toys5():
    return render_template("toys5-0133.html")
    
@app.route("/toys6-0134.html")
def toys6():
    return render_template("toys6-0134.html")
@app.route("/toys7-0135.html")

def toys7():
    return render_template("toys7-0135.html")
    
@app.route("/toys8-0136.html")
def toys8():
    return render_template("toys8-0136.html")
    
@app.route("/toys9-0137.html")
def toys9():
    return render_template("toys9-0137.html")
    
@app.route("/toys10-0138.html")
def toys10():
    return render_template("toys10-0138.html")
    
@app.route("/toys11-0139.html")
def toys11():
    return render_template("toys11-0139.html")
       
@app.route("/toys12-0140.html")
def toys12():
    return render_template("toys12-0140.html")
    
@app.route("/toys13-0141.html")
def toys13():
    return render_template("toys13-0141.html")
    
@app.route("/toys14-0142.html")
def toys14():
    return render_template("toys14-0142.html")   
       
@app.route("/toys15-0143.html")
def toys15():
    return render_template("toys15-0143.html")  
       
@app.route("/toys16-0144.html")
def toys16():
    return render_template("toys16-0144.html")
    
@app.route("/woman_handbags.html")
def whandbag():
    return render_template("woman_handbags.html") 

@app.route("/handbag1-0081.html")
def handbag1():
    return render_template("handbag1-0081.html") 

@app.route("/handbag2-0082.html")
def handbag2():
    return render_template("handbag2-0082.html")

@app.route("/handbag3-0083.html")
def handbag3():
    return render_template("handbag3-0083.html")

@app.route("/handbag4-0084.html")
def handbag4():
    return render_template("handbag4-0084.html")

@app.route("/handbag5-0085.html")
def handbag5():
    return render_template("handbag5-0085.html") 

@app.route("/handbag6-0086.html")
def handbag6():
    return render_template("handbag6-0086.html") 

@app.route("/handbag7-0087.html")
def handbag7():
    return render_template("handbag7-0087.html")

@app.route("/handbag8-0088.html")
def handbag8():
    return render_template("handbag8-0088.html")         

@app.route("/handbag9-0089.html")
def handbag9():
    return render_template("handbag9-0089.html") 

@app.route("/handbag10-0090.html")
def handbag10():
    return render_template("handbag10-0090.html")     

@app.route("/handbag11-0091.html")
def handbag11():
    return render_template("handbag11-0091.html")      

@app.route("/handbag12-0092.html")
def handbag12():
    return render_template("handbag12-0092.html")  

@app.route("/handbag13-0093.html")
def handbag13():
    return render_template("handbag13-0093.html")  

@app.route("/handbag14-0094.html")
def handbag14():
    return render_template("handbag14-0094.html")   

@app.route("/handbag15-0095.html")
def handbag15():
    return render_template("handbag15-0095.html")

@app.route("/handbag16-0096.html")
def handbag16():
    return render_template("handbag16-0096.html")

@app.route("/mens_jacket.html")
def mjacket():
    return render_template("mens_jacket.html")

@app.route("/mens_jacket1-0033.html")
def mjacket1():
    return render_template("mens_jacket1-0033.html")

@app.route("/mens_jacket2-0034.html")
def mjacket2():
    return render_template("mens_jacket2-0034.html")

# @app.route("/mens_jacket3-0035.html")
# def mjacket3():
    # return render_template("mens_jacket3-0035.html")

# @app.route("/mens_jacket4-0036.html")
# def mjacket4():
    # return render_template("mens_jacket4-0036.html") 

# @app.route("/mens_jacket5-0037.html")
# def mjacket5():
    # return render_template("mens_jacket5-0037.html") 

# @app.route("/mens_jacket6-0038.html")
# def mjacket6():
    # return render_template("mens_jacket6-0038.html") 

# @app.route("/mens_jacket7-0039.html")
# def mjacket7():
    # return render_template("mens_jacket7-0039.html") 

# @app.route("/mens_jacket8-0040.html")
# def mjacket8():
    # return render_template("mens_jacket8-0040.html") 

# @app.route("/mens_jacket9-0041.html")
# def mjacket9():
    # return render_template("mens_jacket9-0041.html") 

# @app.route("/mens_jacket10-0042.html")
# def mjacket10():
    # return render_template("mens_jacket10-0042.html") 

# @app.route("/mens_jacket11-0043.html")
# def mjacket11():
    # return render_template("mens_jacket11-0043.html") 

# @app.route("/mens_jacket12-0044.html")
# def mjacket12():
    # return render_template("mens_jacket12-0044.html") 

# @app.route("/mens_jacket13-0045.html")
# def mjacket13():
    # return render_template("mens_jacket13-0045.html") 

# @app.route("/mens_jacket14-0046.html")
# def mjacket4():
    # return render_template("mens_jacket14-0046.html") 

# @app.route("/mens_jacket15-0047.html")
# def mjacket15():
    # return render_template("mens_jacket15-0047.html") 

# @app.route("/mens_jacket16-0048.html")
# def mjacket16():
    # return render_template("mens_jacket16-0048.html") 

@app.route("/womens_top.html")
def wtop():
    return render_template("womens_top.html")  

@app.route("/top1-0065.html")
def wtop1():
    return render_template("top1-0065.html")

@app.route("/top2-0066.html")
def wtop2():
    return render_template("top2-0066.html")

@app.route("/top3-0067.html")
def wtop3():
    return render_template("top3-0067.html")
   
@app.route("/top4-0068.html")
def wtop4():
    return render_template("top4-0068.html")
     
@app.route("/top5-0069.html")
def wtop5():
    return render_template("top5-0069.html")

@app.route("/top6-0070.html")
def wtop6():
    return render_template("top6-0070.html")    

@app.route("/top7-0071.html")
def wtop7():
    return render_template("top7-0071.html")

@app.route("/top8-0072.html")
def wtop8():
    return render_template("top8-0072.html")

@app.route("/top9-0073.html")
def wtop9():
    return render_template("top9-0073.html")     

@app.route("/top10-0074.html")
def wtop10():
    return render_template("top10-0074.html") 

@app.route("/top11-0075.html")
def wtop11():
    return render_template("top11-0075.html") 

@app.route("/top12-0076.html")
def wtop12():
    return render_template("top12-0076.html")

@app.route("/top13-0077.html")
def wtop13():
    return render_template("top13-0077.html")

@app.route("/top14-0078.html")
def wtop14():
    return render_template("top14-0078.html")

@app.route("/top15-0079.html")
def wtop15():
    return render_template("top15-0079.html")

@app.route("/top16-0080.html")
def wtop16():
    return render_template("top16-0080.html")

@app.route("/bags.html")
def bags():
    return render_template("bags.html")  
   
@app.route("/bags1-0171.html")
def bags1():
    return render_template("bags1-0171.html")  
       
@app.route("/bags2-0172.html")
def bags2():
    return render_template("bags2-0172.html")   
@app.route("/bags3-0173.html")
def bags3():
    return render_template("bags3-0173.html") 
    
@app.route("/bags4-0174.html")
def bags4():
    return render_template("bags4-0174.html")   
@app.route("/bags5-0175.html")
def bags5():
    return render_template("bags5-0175.html")     
 
@app.route("/bags6-0176.html")
def bags6():
    return render_template("bags6-0176.html")
@app.route("/bags7-0177.html")
def bags7():
    return render_template("bags7-0177.html")
@app.route("/bags8-0178.html")
def bags8():
    return render_template("bags8-0178.html")  
@app.route("/bags9-0179.html")
def bags9():
    return render_template("bags9-0179.html")  
@app.route("/bags10-0180.html")
def bags10():
    return render_template("bags10-0180.html")  
@app.route("/bags11-0181.html")
def bags11():
    return render_template("bags11-0181.html")  
@app.route("/bags12-0182.html")
def bags12():
    return render_template("bags12-0182.html")   
@app.route("/bags13-0183.html")
def bags13():
    return render_template("bags13-0183.html")
@app.route("/bags14-0184.html")
def bags14():
    return render_template("bags14-0184.html")
@app.route("/bags15-0185.html")
def bags15():
    return render_template("bags15-0185.html")
@app.route("/bags16-0186.html")
def bags16():
    return render_template("bags16-0186.html")  

@app.route("/womens_shoes.html")
def wshoes():
    return render_template("womens_shoes.html")  

@app.route("/w-shoes-0113.html")
def wshoes1():
    return render_template("w-shoes-0113.html")

@app.route("/w-shoes-0114.html")
def wshoes2():
    return render_template("w-shoes-0114.html")

@app.route("/w-shoes-0115.html")
def wshoes3():
    return render_template("w-shoes-0115.html")

@app.route("/w-shoes-0116.html")
def wshoes4():
    return render_template("w-shoes-0116.html")

@app.route("/w-shoes-0117.html")
def wshoes5():
    return render_template("w-shoes-0117.html")

@app.route("/w-shoes-0118.html")
def wshoes6():
    return render_template("w-shoes-0118.html")

@app.route("/w-shoes-0119.html")
def wshoes7():
    return render_template("w-shoes-0119.html")                           

@app.route("/w-shoes-0120.html")
def wshoes8():
    return render_template("w-shoes-0120.html")

@app.route("/w-shoes-0121.html")
def wshoes9():
    return render_template("w-shoes-0121.html")

@app.route("/w-shoes-0122.html")
def wshoes10():
    return render_template("w-shoes-0122.html")

@app.route("/w-shoes-0123.html")
def wshoes11():
    return render_template("w-shoes-0123.html")

@app.route("/w-shoes-0124.html")
def wshoes12():
    return render_template("w-shoes-0124.html")

@app.route("/w-shoes-0125.html")
def wshoes13():
    return render_template("w-shoes-0125.html")

@app.route("/w-shoes-0126.html")
def wshoes14():
    return render_template("w-shoes-0126.html")

@app.route("/w-shoes-0127.html")
def wshoes15():
    return render_template("w-shoes-0127.html")

@app.route("/w-shoes-0128.html")
def wshoes16():
    return render_template("w-shoes-0128.html") 

@app.route("/jeans.html")
def jeans():
    return render_template("jeans.html")
@app.route("/jeans1-0145.html")
def jeans1():
    return render_template("jeans1-0145.html") 
@app.route("/jeans2-0146.html")
def jeans2():
    return render_template("jeans2-0146.html")  
@app.route("/jeans3-0147.html")
def jeans3():
    return render_template("jeans3-0147.html")  
@app.route("/jeans4-0148.html")
def jeans4():
    return render_template("jeans4-0148.html")  
@app.route("/jeans5-0149.html")
def jeans5():
    return render_template("jeans5-0149.html")  
@app.route("/jeans6-0150.html")
def jeans6():
    return render_template("jeans6-0150.html")    
@app.route("/jeans7-0151.html")
def jeans7():
    return render_template("jeans7-0151.html") 
@app.route("/jeans8-0152.html")
def jeans8():
    return render_template("jeans8-0152.html") 
@app.route("/jeans9-0153.html")
def jeans9():
    return render_template("jeans9-0153.html") 
@app.route("/jeans10-0154.html")
def jeans10():
    return render_template("jeans10-0154.html") 
@app.route("/jeans11-0155.html")
def jeans11():
    return render_template("jeans11-0155.html") 
@app.route("/jeans12-0156.html")
def jeans12():
    return render_template("jeans12-0156.html") 
@app.route("/jeans13-0157.html")
def jeans13():
    return render_template("jeans13-0157.html") 
@app.route("/jeans14-0158.html")
def jeans14():
    return render_template("jeans14-0158.html")   
@app.route("/jeans15-0159.html")
def jeans15():
    return render_template("jeans15-0159.html") 
@app.route("/jeans16-0160.html")
def jeans16():
    return render_template("jeans16-0160.html")
@app.route("/bshirts.html")
def bshirts():
    return render_template("bshirts.html")
@app.route("/bshirts1-0161.html")
def bshirts1():
    return render_template("bshirts1-0161.html")
@app.route("/bshirts2-0162.html")
def bshirts2():
    return render_template("bshirts2-0162.html")  
@app.route("/bshirts3-0163.html")
def bshirts3():
    return render_template("bshirts3-0163.html") 
@app.route("/bshirts4-0164.html")
def bshirts4():
    return render_template("bshirts4-0164.html") 
@app.route("/bshirts5-0165.html")
def bshirts5():
    return render_template("bshirts5-0165.html")   
@app.route("/bshirts6-0166.html")
def bshirts6():
    return render_template("bshirts6-0166.html")   
@app.route("/bshirts7-0167.html")
def bshirts7():
    return render_template("bshirts7-0167.html")
@app.route("/bshirts8-0168.html")
def bshirts8():
    return render_template("bshirts8-0168.html")
@app.route("/bshirts9-0169.html")
def bshirts9():
    return render_template("bshirts9-0169.html")  
@app.route("/bshirts10-0170.html")
def bshirts10():
    return render_template("bshirts10-0170.html")  
@app.route("/bshirts11-0171.html")
def bshirts11():
    return render_template("bshirts11-0171.html")  
@app.route("/bshirts12-0172.html")
def bshirts12():
    return render_template("bshirts12-0172.html")  
@app.route("/bshirts13-0173.html")
def bshirts13():
    return render_template("bshirts13-0173.html")     
@app.route("/bshirts14-0174.html")
def bshirts14():
    return render_template("bshirts14-0174.html")
@app.route("/bshirts15-0175.html")
def bshirts15():
    return render_template("bshirts15-0175.html")
@app.route("/bshirts16-0176.html")
def bshirts16():
    return render_template("bshirts16-0176.html")
@app.route("/womens_jewellery.html")
def wjewellery():
    return render_template("womens_jewellery.html") 

@app.route("/jewellery1-0097.html")
def wjewellery1():
    return render_template("jewellery1-0097.html") 

@app.route("/jewellery2-0098.html")
def wjewellery2():
    return render_template("jewellery2-0098.html")

@app.route("/jewellery3-0099.html")
def wjewellery3():
    return render_template("jewellery3-0099.html")
 
@app.route("/jewellery4-0100.html")
def wjewellery4():
    return render_template("jewellery4-0100.html")

@app.route("/jewellery5-0101.html")
def wjewellery5():
    return render_template("jewellery5-0101.html")

@app.route("/jewellery6-0102.html")
def wjewellery6():
    return render_template("jewellery6-0102.html")     
     
@app.route("/jewellery7-0103.html")
def wjewellery7():
    return render_template("jewellery7-0103.html")      

@app.route("/jewellery8-0104.html")
def wjewellery8():
    return render_template("jewellery8-0104.html") 

@app.route("/jewellery9-0105.html")
def wjewellery9():
    return render_template("jewellery9-0105.html") 

@app.route("/jewellery10-0106.html")
def wjewellery10():
    return render_template("jewellery10-0106.html")     

@app.route("/jewellery11-0107.html")
def wjewellery11():
    return render_template("jewellery11-0107.html") 

@app.route("/jewellery12-0108.html")
def wjewellery12():
    return render_template("jewellery12-0108.html") 

@app.route("/jewellery13-0109.html")
def wjewellery13():
    return render_template("jewellery13-0109.html")

@app.route("/jewellery14-0110.html")
def wjewellery14():
    return render_template("jewellery14-0110.html")

@app.route("/jewellery15-0111.html")
def wjewellery15():
    return render_template("jewellery15-0111.html")

@app.route("/jewellery16-0112.html")
def wjewellery16():
    return render_template("jewellery16-0112.html")  
@app.route("/appleLap.html")
def apple():
    return render_template("appleLap.html")  
@app.route("/Apple1-0257.html")
def apple1():
    return render_template("Apple1-0257.html")  
   
@app.route("/apple2-0258.html")
def apple2():
    return render_template("apple2-0258.html")
@app.route("/apple3-0259.html")
def apple3():
    return render_template("apple3-0259.html")   
@app.route("/apple4-0260.html")
def apple4():
    return render_template("apple4-0260.html")  
@app.route("/apple5-0261.html")
def apple5():
    return render_template("apple5-0261.html")
@app.route("/apple6-0262.html")
def apple6():
    return render_template("apple6-0262.html")
@app.route("/apple7-0263.html")
def apple7():
    return render_template("apple7-0263.html")
@app.route("/apple8-0264.html")
def apple8():
    return render_template("apple8-0264.html")
@app.route("/apple9-0265.html")
def apple9():
    return render_template("apple9-0265.html")
@app.route("/apple10-0266.html")
def apple10():
    return render_template("apple10-0266.html")
@app.route("/apple11-0267.html")
def apple11():
    return render_template("apple11-0267.html")
@app.route("/apple12-0268.html")
def apple12():
    return render_template("apple12-0268.html")
@app.route("/apple13-0269.html")
def apple13():
    return render_template("apple13-0269.html") 
@app.route("/apple14-0270.html")
def apple14():
    return render_template("apple14-0270.html")   
@app.route("/apple15-0271.html")
def apple15():
    return render_template("apple15-0271.html")   
@app.route("/apple16-0272.html")
def apple16():
    return render_template("apple16-0272.html")    
@app.route("/Memory(RAM).html")
def dmemory():
    return render_template("Memory(RAM).html")

@app.route("/D_Memory1-0289.html")
def dmemory1():
    return render_template("D_Memory1-0289.html")

@app.route("/D_Memory2-0290.html")
def dmemory2():
    return render_template("D_Memory2-0290.html")

@app.route("/D_Memory3-0291.html")
def dmemory3():
    return render_template("D_Memory3-0291.html")

@app.route("/D_Memory4-0292.html")
def dmemory4():
    return render_template("D_Memory4-0292.html")

@app.route("/D_Memory5-0293.html")
def dmemory5():
    return render_template("D_Memory5-0293.html")

@app.route("/D_Memory6-0294.html")
def dmemory6():
    return render_template("D_Memory6-0294.html")

@app.route("/D_Memory7-0295.html")
def dmemory7():
    return render_template("D_Memory7-0295.html")

@app.route("/D_Memory8-0296.html")
def dmemory8():
    return render_template("D_Memory8-0296.html")            
@app.route("/Motherboards.html")
def dmotherboard():
    return render_template("Motherboards.html") 

@app.route("/D_Motherboard1-0297.html")
def dmotherboard1():
    return render_template("D_Motherboard1-0297.html") 

@app.route("/D_Motherboard2-0298.html")
def dmotherboard2():
    return render_template("D_Motherboard2-0298.html")

@app.route("/D_Motherboard3-0299.html")
def dmotherboard3():
    return render_template("D_Motherboard3-0299.html")

@app.route("/D_Motherboard4-0300.html")
def dmotherboard4():
    return render_template("D_Motherboard4-0300.html")

@app.route("/D_Motherboard5-0301.html")
def dmotherboard5():
    return render_template("D_Motherboard5-0301.html")

@app.route("/D_Motherboard6-0302.html")
def dmotherboard6():
    return render_template("D_Motherboard6-0302.html")

@app.route("/D_Motherboard7-0303.html")
def dmotherboard7():
    return render_template("D_Motherboard7-0303.html")

@app.route("/D_Motherboard8-0304.html")
def dmotherboard8():
    return render_template("D_Motherboard8-0304.html")

@app.route("/D_Motherboard9-0305.html")
def dmotherboard9():
    return render_template("D_Motherboard9-0305.html")


if __name__ == "__main__":
    app.run(debug=True)
 