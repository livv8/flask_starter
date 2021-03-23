from flask_wtf import FlaskForm
from wtforms import StringField, FileField, TextAreaField,SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed



class addPropertyform(FlaskForm):
    title= StringField('Property Name', validators=[DataRequired(), Length(max=30)] )
    numofbedrooms= StringField('2', validators=[DataRequired(), Length(max=3)] )
    numofbath=StringField('3' , validators=[DataRequired(), Length(max=3)] )
    location= StringField ( '32 River road' , validators=[DataRequired(), Length(max=200)] )
    price= StringField ( '150,000' , validators=[DataRequired(), Length(max=20)] )
    housetype=SelectField( 'type', choices=[('H','House'), ('A', 'Apartment')] )
    descript=TextAreaField('Description', validators=[DataRequired(), Length(max=30)] )
    
class FormPhoto(FlaskForm):
     photo= FileField('image', validators= [FileRequired(), FileAllowed(['jpg', 'png', 'Image Only']) ])
     