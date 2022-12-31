from flask import Blueprint,request,render_template,session,redirect,url_for,flash
from ..models.user import User 
from ..forms.createAccount import createAccount
from ..forms.login import login
from flask_login import login_required
from app import db

auth=Blueprint('auth',__name__)

@auth.route('/create',methods=['GET','POST'])
def create():
    form=createAccount()
    if form.validate_on_submit() and request.method=='POST':
        session['username']=form.name.data
        new_user=User(username=form.name.data,email=form.email.data)
        new_user.password=form.password.data
        db.session.add(new_user)
        return redirect(url_for('auth.create'))
    return render_template('create.html',form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    form=login()
    if form.validate_on_submit() and request.method=='POST':
        user=User.query.filter_by(name=form.name.data).first()
        if user is None:
            session['know']=False
            return redirect(url_for('auth.create'))
        else:
            session['know']=True
        session['name']=form.name.data
        form.name.data=''
        return redirect(url_for('auth.login'))
    return render_template('login.html',form=form,name=session.get('name'),know=session.get('know',False))

@auth.route('/secret')
@login_required
def secret():
    return "<h1>SOLO PERSONAS AUTORIZADAS</h1>"