from flask import Blueprint,request,render_template,session,redirect,url_for,flash,current_app
from ..models.user import User,Roles
from ..forms.createAccount import createAccount
from ..forms.login import log
from flask_login import login_required,logout_user,login_user,current_user
from flask_mail import Message
from app import db,mail
auth=Blueprint('auth',__name__)

def send_email(to,subject,template,**kwargs):
    msg=Message(current_app.config['MAIL_SUBJECT_PREFIX']+subject,sender=current_app.config['MAIL_SENDER'],recipients=[to])
    msg.body=render_template(template+'.txt.',**kwargs)
    msg.html=render_template(template+'.html',**kwargs)
    mail.send(msg)



@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5]!='auth.':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token=current_user.generate_confirmation_token()
    send_email('./auth/email/confirm','Confirm Your Account',current_user,token=token)
    flash('A new confirmation email has been sent to you by email.','info')
    return redirect(url_for('auth.index'))
    
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('auth.index'))
    return render_template('unconfirmed.html')

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
            db.session.commit()
            token=new_user.generate_confimation_token()
            send_email(new_user.email,'Confirm Your Account','./auth/email/confirm',user=new_user,token=token)
            flash('A confirmation email has been sent to you by email.','info')

            return redirect(url_for('auth.index'))
        return redirect(url_for('auth.create'))
    return render_template('create.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('auth.index'))
    if current_user.confirm(token):
        flash('You have confirmed your acount. Thanks!','success')
    else:
        flash('The confirmation link is invalid or has expired','info')
    return redirect(url_for('auth.index'))


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

