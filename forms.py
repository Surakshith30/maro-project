from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, email_validator


class BillingForm(FlaskForm):

    bfname = StringField('First Name',
                             validators=[DataRequired(),Length(min=2,max=20)])
    blname = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    billing_address = StringField('Billing Address',
                                  validators=[DataRequired(), Length(min=2,max=50)])
    bstate = StringField('State',
                        validators=[DataRequired(), Length(min=2, max=20)])
    bcity = StringField('City', validators=[DataRequired(), Length(min=2, max=20)])
    bpincode = IntegerField('Pincode', validators=[DataRequired()])


class ShippingForm(FlaskForm):
    sfname = StringField('First Name',
                             validators=[DataRequired(),Length(min=2,max=20)])
    slname = StringField('Last Name',
                            validators=[DataRequired(), Length(min=2, max=20)])
    shipping_address = StringField('Billing Address',
                                  validators=[DataRequired(), Length(min=2,max=50)])
    sstate = StringField('State',
                        validators=[DataRequired(), Length(min=2, max=20)])
    scity = StringField('City', validators=[DataRequired(), Length(min=2, max=20)])
    spincode = IntegerField('Pincode', validators=[DataRequired()])


class PaymentForm(FlaskForm):
    card_no = StringField('Card Number',
                             validators=[DataRequired(),Length(min=2,max=20)])
    pname = StringField('Name on card',
                            validators=[DataRequired(), Length(min=2, max=20)])
    CVV = StringField('Billing Address',
                                  validators=[DataRequired(), Length(min=2,max=50)])
    valid_through = StringField('State',
                        validators=[DataRequired(), Length(min=2, max=20)])
    scity = StringField('City', validators=[DataRequired(), Length(min=2, max=20)])
    spincode = IntegerField('Pincode', validators=[DataRequired()])