from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm  # Para crear formularios en Flask
from wtforms import (
    StringField,       # Campo de texto
    PasswordField,     # Campo de contraseña
    SubmitField,       # Botón de envío
    RadioField,        # Campo de opciones (botones de radio)
    SelectMultipleField,  # Campo de selección múltiple
    IntegerField       # Campo de número entero
)
from wtforms.validators import (
    DataRequired,  # Validador para campos obligatorios
    Length,        # Validador para longitud de texto
    NumberRange   
)
from wtforms import widgets


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField('Iniciar sesión')

class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField('Registrarse')

class PedidoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(min=2, max=100)])
    direccion = StringField("Dirección", validators=[DataRequired(), Length(min=5, max=200)])
    telefono = StringField("Teléfono", validators=[DataRequired(), Length(min=8, max=15)])

    tamaño_pizza = RadioField("Tamaño Pizza", choices=[
        ('Chica', 'Chica $40'),
        ('Mediana', 'Mediana $80'),
        ('Grande', 'Grande $120')
    ], validators=[DataRequired()])

    ingredientes = SelectMultipleField("Ingredientes", choices=[
        ('Jamon', 'Jamón $10'),
        ('Piña', 'Piña $10'),
        ('Champiñones', 'Champiñones $10')
    ], option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))

    numero_pizzas = IntegerField("Número de Pizzas", validators=[DataRequired(), NumberRange(min=1, max=100)])

    submit = SubmitField("Agregar")

class ProfesorForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    materia = StringField('Materia', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Guardar')