import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to create the database table
def create_table():
    connection = sqlite3.connect('patients.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS patient (
                      id INTEGER PRIMARY KEY,
                      telephone TEXT NOT NULL,
                      name TEXT NOT NULL,
                      dob TEXT NOT NULL,
                      id_number TEXT NOT NULL,
                      address TEXT NOT NULL,
                      county TEXT NOT NULL,
                      sub_county TEXT NOT NULL,
                      email TEXT NOT NULL,
                      gender TEXT NOT NULL,
                      marital_status TEXT NOT NULL,
                      kin_name TEXT NOT NULL,
                      kin_dob TEXT NOT NULL,
                      kin_id_number TEXT NOT NULL,
                      kin_gender TEXT NOT NULL,
                      kin_relationship TEXT NOT NULL
                  )''')
    connection.commit()
    connection.close()

# Function to insert patient data into the database
def insert_patient_data(patient_data):
    connection = sqlite3.connect('patients.db')
    cursor = connection.cursor()

    query = '''INSERT INTO patient (telephone, name, dob, id_number, address, county, sub_county, email, gender, marital_status, kin_name, kin_dob, kin_id_number, kin_gender, kin_relationship)
               VALUES (:telephone, :name, :dob, :id_number, :address, :county, :sub_county, :email, :gender, :marital_status, :kin_name, :kin_dob, :kin_id_number, :kin_gender, :kin_relationship)'''

    cursor.execute(query, patient_data)
    connection.commit()

    # Get the automatically generated ID and add it to the patient_data dictionary
    patient_data['id'] = cursor.lastrowid

    connection.close()

# Function to send email to the patient
def send_patient_email(patient_data):
    sender_email = 'michealphenh10@gmail.com'
    sender_password = 'qgstmtvymmooyukd'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = patient_data['email']
    msg['Subject'] = 'Patient Registration'

    body = f'Hello {patient_data["name"]}, thank you for registering as a patient. Your patient reference number is {patient_data["id"]}.'
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, patient_data['email'], msg.as_string())
    server.quit()

def main():
    create_table()

    while True:
        print("\nPatient Registration Form")
        print("-------------------------")
        telephone = input("Telephone: ")
        name = input("Name: ")
        dob = input("Date of Birth (YYYY-MM-DD): ")
        id_number = input("ID Number: ")
        address = input("Address: ")
        county = input("County: ")
        sub_county = input("Sub County: ")
        email = input("Email: ")
        gender = input("Gender: ")
        marital_status = input("Marital Status: ")
        kin_name = input("Next of Kin Name: ")
        kin_dob = input("Next of Kin Date of Birth (YYYY-MM-DD): ")
        kin_id_number = input("Next of Kin ID Number: ")
        kin_gender = input("Next of Kin Gender: ")
        kin_relationship = input("Next of Kin Relationship: ")

        patient_data = {
            'telephone': telephone,
            'name': name,
            'dob': dob,
            'id_number': id_number,
            'address': address,
            'county': county,
            'sub_county': sub_county,
            'email': email,
            'gender': gender,
            'marital_status': marital_status,
            'kin_name': kin_name,
            'kin_dob': kin_dob,
            'kin_id_number': kin_id_number,
            'kin_gender': kin_gender,
            'kin_relationship': kin_relationship
        }

        insert_patient_data(patient_data)
        send_patient_email(patient_data)

        print("\nPatient data saved successfully!")
        print(f"A confirmation email has been sent to {email}.")

        continue_registration = input("\nDo you want to register another patient? (yes/no): ")
        if continue_registration.lower() != 'yes':
            break

if __name__ == '__main__':
    main()
