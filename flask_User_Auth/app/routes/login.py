from flask import Blueprint,request,render_template,session,redirect,url_for,flash
from ..models.user import User 
from ..forms.createAccount import createAccount
from app import db

auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    form=createAccount()
    if form.validate_on_submit() and request.method=='POST':
        session['username']=form.name.data
        new_user=User(username=form.name.data,email=form.email.data)
        new_user.password=form.password.data
        db.session.add(new_user)
        return redirect(url_for('auth.login'))
    return render_template('login.html',form=form)