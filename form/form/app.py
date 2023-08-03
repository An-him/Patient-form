from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
db = SQLAlchemy(app)

class Patient(db.Model):

with app.app_context():
    db.create_all()

# Configuration for the email service
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'intricatesyllable@gmail.com'
app.config['MAIL_PASSWORD'] = 'Uganda2000'
mail = Mail(app)

# Define the Patient model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telephone = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    id_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    county = db.Column(db.String(100), nullable=False)
    sub_county = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    marital_status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Patient('{self.name}', '{self.telephone}')"

# Define the form route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        patient_data = {
            'telephone': request.form['telephone'],
            'name': request.form['name'],
            'dob': request.form['dob'],
            'id_number': request.form['id_number'],
            'address': request.form['address'],
            'county': request.form['county'],
            'sub_county': request.form['sub_county'],
            'email': request.form['email'],
            'gender': request.form['gender'],
            'marital_status': request.form['marital_status']
        }

        # Create a new patient object
        new_patient = Patient(**patient_data)

        # Save the patient object to the database
        db.session.add(new_patient)
        db.session.commit()

        # Send email to the patient
        send_patient_email(new_patient)

        # Redirect to a thank you page or any other desired page
        return redirect('/thank-you')

    return render_template('index.html')

# Function to send email to the patient
def send_patient_email(patient):
    msg = Message('Patient Registration', sender='your_email@example.com', recipients=[patient.email])
    msg.body = f'Hello {patient.name}, thank you for registering as a patient. Your patient reference number is {patient.id}.'
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
