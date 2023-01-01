from flask_wtf import FlaskForm
from wtforms import PasswordField,SubmitField,StringField
from wtforms.validators import DataRequired

class log(FlaskForm):
    password=PasswordField('Password:',validators=[DataRequired("Insert a password.")])
    name=StringField('Name:',validators=[DataRequired("The name is neccesary.")])
    submit=SubmitField('Submit')
