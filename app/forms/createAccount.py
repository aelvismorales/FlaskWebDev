from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class createAccount(FlaskForm):
    name=StringField('Name:',validators=[DataRequired("The name is neccesary.")])
    password=PasswordField('Password:',validators=[DataRequired("Insert a password.")])
    email=EmailField("Email:",validators=[DataRequired("Please insert a valid email.")])
    submit=SubmitField('Submit')