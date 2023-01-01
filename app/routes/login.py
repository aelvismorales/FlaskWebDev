from flask import Blueprint,request,render_template,session,redirect,url_for,flash
from ..models.user import User,Roles
from ..forms.createAccount import createAccount
from ..forms.login import log
from flask_login import login_required,logout_user,login_user
from app import db

auth=Blueprint('auth',__name__)

@auth.route('/index',methods=['GET','POST'])
def index():
    return render_template('index.html')


@auth.route('/create',methods=['GET','POST'])
def create():
    form=createAccount()
    if form.validate_on_submit() and request.method=='POST':
        rol=Roles.query.filter_by(name=form.rol.data).first()
        if rol is None:
            flash("Select a valid roles to the user.",category="info")
        else:
            session['username']=form.name.data
            new_user=User(username=form.name.data,email=form.email.data,role=rol)
            new_user.password=form.password.data
            db.session.add(new_user)
            flash("You can now loggin",'info')
            return redirect(url_for('auth.login'))
        return redirect(url_for('auth.create'))
    return render_template('create.html',form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    form=log()
    if form.validate_on_submit() and request.method=='POST':
        user=User.query.filter_by(username=form.name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            flash("You're login succesfull",'success')
            return redirect(request.args.get('next') or (url_for('auth.index')))
        flash("Invalid username or password ",'info')
    return render_template('login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out",'info')
    return redirect(url_for("auth.login"))

@auth.route("/roles",methods=['GET','POST'])
def roles():
    administrador=Roles(name="administrador")
    vendedor=Roles(name="vendedor")
    db.session.add(administrador)
    db.session.add(vendedor)
    return redirect(url_for('auth.index'))

@auth.route('/secret')
@login_required
def secret():
    return "<h1>SOLO PERSONAS AUTORIZADAS</h1>"