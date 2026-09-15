import sqlite3



from datetime import datetime,time,timedelta

from streamlit import cursor

DB_NAME="hospital.db"

def create_doctors_table():
    connection=sqlite3.connect(DB_NAME)  #to connect to database
    cursor=connection.cursor()           #Think of the cursor as a messenger that sends SQL commands to the database.
    cursor.execute("""
          CREATE TABLE IF NOT EXISTS doctors(
             doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             specialization TEXT NOT NULL,
             experience INTEGER,
             consultation_fee REAL)""")
    connection.commit()  # Save the table creation
    connection.close()  # Close database connection
    print("Doctors table created successfully!")

def insert_doctors():
    connection=sqlite3.connect(DB_NAME)
    cursor=connection.cursor()
    doctors=[
        ("Dr.RAjesh","Cardiology",12,800),
        ("Dr.Priya","Dermatology",8,600),
        ("Dr.Anil","Orthopedics",15,700)
    ]
    cursor.executemany("""
    INSERT INTO doctors
        (name,specialization,experience,consultation_fee)
        VALUES (?,?,?,?)
        
    """,doctors)

    connection.commit()
    connection.close()  # to close connection to database
    print("Doctors added successfully")

def create_patients_table():
    connection=sqlite3.connect(DB_NAME)
    cursor=connection.cursor()
    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS patients
    (patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
     name TEXT NOT NULL,
     age INTEGER,
     phone TEXT
   
        )
        
   """ )
    connection.commit()
    connection.close()
    print("Patients table created successfully!")

def insert_patients():
    connection=sqlite3.connect(DB_NAME)
    cursor=connection.cursor()
    patients = [
        ("Ravi", 35, "9876543210"),
        ("Priya", 28, "9876543211"),
        ("Anil", 45, "9876543212")
    ]
    cursor.executemany(
        """
        INSERT INTO patients(
        name,age,phone)
            VALUES(?,?,?)
        """,patients
    )
    connection.commit()
    connection.close()
    print("Patients added successfully")

def create_appointments_table():
    connection=sqlite3.connect(DB_NAME)
    cursor=connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments
        (appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
         patient_id INTEGER NOT NULL,
         doctor_id INTEGER NOT NULL,
         appointment_date TEXT NOT NULL,
         appointment_time TEXT NOT NULL,
         status TEXT DEFAULT 'Booked'
    )
       """)
    connection.commit()
    connection.close()
    print("Appointments table created successfully!")

def book_appointment(patient_id,doctor_id,appointment_date,appointment_time):

     try:
         appointment_date_obj=datetime.strptime(
             appointment_date,"%d-%m-%Y"
         )
     except ValueError:
         return "Invalid date.Please use DD-MM-YYYY format."
     # Date cannot be in the past
     if appointment_date_obj.date()<datetime.today().date():
         return "Appointment date cannot be in the past."
     appointment_date_db = appointment_date_obj.strftime("%Y-%m-%d")
     try:
         appointment_time_obj=datetime.strptime(
             appointment_time,"%H:%M"
         )
     except ValueError:
         return "Invalid time.Please use HH:MM format."
     # Create allowed slots
     allowed_times=[]
     current_time=time(9,0)
     end_time=time(17,30)
     while current_time<=end_time:
         allowed_times.append(current_time)
         current_datetime=datetime.combine(datetime.today(),current_time)
         current_datetime = current_datetime.replace(
             second=0,
             microsecond=0
         )

         current_datetime = current_datetime + timedelta(minutes=30)

         current_time = current_datetime.time()
# Check slot
    # print("Requested time:", appointment_time_obj.time())
     #print("Allowed times:", allowed_times)
     if appointment_time_obj.time() not in allowed_times:

             return "Invalid appointment slot.Appointments are available every 30 minutes between 9:00 and 17:30."
     connection=sqlite3.connect(DB_NAME)
     cursor=connection.cursor()
     cursor.execute("""
             SELECT appointment_id
             FROM appointments
             WHERE doctor_id=?
             AND appointment_date=?
             AND appointment_time=?
             AND status='Booked'
             """,(doctor_id,appointment_date_db,appointment_time)
         
     )
     existing_appointment=cursor.fetchone()

     if existing_appointment:

         connection.close()

         return "Doctor is already Booked at this time."
     cursor.execute("""
         INSERT INTO appointments
         (patient_id, doctor_id, appointment_date, appointment_time)
         VALUES (?, ?, ?, ?)
     """, (
         patient_id,
         doctor_id,
         appointment_date,
         appointment_time
     ))

     appointment_id = cursor.lastrowid

     connection.commit()
     connection.close()

     return f"Appointment is BOOKED successfully! Appointment ID: {appointment_id}"


def find_patient(name,phone):
    connection=sqlite3.connect(DB_NAME)
    cursor=connection.cursor()
    cursor.execute("""
    SELECT patient_id,name,age,phone
    FROM patients
    WHERE name=? AND phone=?
    """,(name,phone))
    patient=cursor.fetchone()

    connection.close()


    if patient:
        print("Patient found!")
        print("Patient ID:", patient[0])
        print("Name:", patient[1])
        print("Age:", patient[2])
    else:
        print("Patient not found.")
    return patient

def find_patient_by_name(name):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT patient_id, name, age, phone
        FROM patients
        WHERE name = ?
    """, (name,))

    patients = cursor.fetchall()

    connection.close()

    return patients

def find_doctor(specialization):
    connection=sqlite3.connect(DB_NAME)
    cursor=connection.cursor()
    cursor.execute("""
    SELECT doctor_id,name,specialization,experience,consultation_fee
    FROM doctors
        WHERE specialization=?
    """,(specialization,))
    doctor=cursor.fetchone()
    connection.close()
    if doctor:
        print("Doctor found!")
        print("Doctor ID:", doctor[0])
        print("Name:", doctor[1])
        print("Specialization:", doctor[2])
        print("Experience:", doctor[3], "years")
        print("Consultation Fee: ₹", doctor[4])
    else:
        print("Doctor not found.")
    return doctor


def book_appointment_from_user():
    name = input("Enter patient name:").strip()
    if not name:
        print("patient name cannot be empty")
        return
    phone = input("Enter patient phone number:").strip()
    if not phone.isdigit():
       print("phone number must contain only digits")
       return
    if len(phone)!=10:
        print("phone number must be 10 digits")
        return

    patient = find_patient(name, phone)

    if patient is None:
        print("Patient not found.Please register first.")
        return
    patient_id = patient[0]

    specialization = input("enter doctor specialization:").strip()
    doctor = find_doctor(specialization)

    if doctor is None:
        print("Doctor not found.")
        return
    doctor_id = doctor[0]

    appointment_date = input("Enter the date(DD-MM-YYYY):").strip()
    try:
        appointment_date_obj =datetime.strptime(appointment_date,"%d%m%y")
    except ValueError:
        print("Invalid Date format.")
        return
    today=datetime.today()
    if appointment_date_obj.date() < today.date():
        print("Appointment date cannot be in the past.")
        return
    appointment_time = input(
        "Enter appointment time (HH:MM): "
    ).strip()

    try:
        appointment_time_obj=datetime.strptime(
            appointment_time,
            "%H:%M"
        )
    except ValueError:
        print("Invalid time format.")
        return
    oappointment_time = input(
    "Enter appointment time (HH:MM): "
).strip()

    try:
        appointment_time_obj = datetime.strptime(
        appointment_time,
        "%H:%M"
     )
    except ValueError:
     print("Invalid time format.")
     return

    allowed_times = []

    current_time = datetime.combine(
    datetime.today(),
    time(9, 0)
    )

    end_time = datetime.combine(
      datetime.today(),
      time(17, 30)
    )

    while current_time <= end_time:
      allowed_times.append(current_time.time())
      current_time += timedelta(minutes=30)

    if appointment_time_obj.time() not in allowed_times:
      print("Invalid appointment slot.")
      print("Appointments are available every 30 minutes.")
      return


    book_appointment(patient_id, doctor_id, appointment_date, appointment_time)
def get_connection():
    return sqlite3.connect(DB_NAME)
def get_patients():
    connection=sqlite3.connect(DB_NAME)
    cursor=connection.cursor()
    cursor.execute("""
    SELECT * FROM patients
    """)
    patients=cursor.fetchall()
    connection.close()
    for patient in patients:
        print(patient)
    return patients

def get_doctors():
        connection = sqlite3.connect(DB_NAME)

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM doctors")

        doctors = cursor.fetchall()
        for doctor in doctors:
            print(doctor)

        connection.close()

        return doctors

def get_appointments():
    connection=sqlite3.connect(DB_NAME)
    cursor=connection.cursor()
    cursor.execute("""
    SELECT
    appointments.appointment_id,
    patients.name,
    doctors.name,
    appointments.appointment_date,
    appointments.appointment_time,
    appointments.status,
    doctors.consultation_fee
    FROM appointments
        JOIN patients
        ON appointments.patient_id=patients.patient_id
        JOIN doctors
        ON appointments.doctor_id=doctors.doctor_id
    """)
    appointments=cursor.fetchall()
   # print(appointments)
    connection.close()
    return appointments

def get_patient_appointments(patient_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    today=datetime.today().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT
            appointments.appointment_id,
            patients.name,
            doctors.name,
            appointments.appointment_date,
            appointments.appointment_time,
            appointments.status,
            doctors.consultation_fee
        FROM appointments
        JOIN patients
            ON appointments.patient_id = patients.patient_id
        JOIN doctors
            ON appointments.doctor_id = doctors.doctor_id
        WHERE appointments.patient_id = ?
        AND appointments.status='Booked'
        AND appointments.appointment_date>=?  
        ORDER BY appointments.appointment_date,
                 appointments.appointment_time
    """, (patient_id,today))

    appointments = cursor.fetchall()

    connection.close()

    return appointments

def get_patient_appointment_history(patient_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            appointments.appointment_id,
            patients.name,
            doctors.name,
            appointments.appointment_date,
            appointments.appointment_time,
            appointments.status,
            doctors.consultation_fee
        FROM appointments
        JOIN patients
            ON appointments.patient_id = patients.patient_id
        JOIN doctors
            ON appointments.doctor_id = doctors.doctor_id
        WHERE appointments.patient_id = ?
        ORDER BY appointments.appointment_date DESC,
                 appointments.appointment_time DESC
    """, (patient_id,))

    appointments = cursor.fetchall()
    connection.close()

    return appointments

def convert_old_appointment_dates():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT appointment_id, appointment_date
        FROM appointments
    """)

    appointments = cursor.fetchall()

    for appointment_id, old_date in appointments:
        try:
            date_obj = datetime.strptime(old_date, "%d-%m-%Y")
            new_date = date_obj.strftime("%Y-%m-%d")

            cursor.execute("""
                UPDATE appointments
                SET appointment_date = ?
                WHERE appointment_id = ?
            """, (new_date, appointment_id))

        except ValueError:
            # Date is already in YYYY-MM-DD format
            pass

    connection.commit()
    connection.close()

    print("Appointment dates converted successfully!")

def cancel_appointment(appointment_id):
    connection=sqlite3.connect(DB_NAME)
    cursor=connection.cursor()
    cursor.execute("""
    SELECT appointment_id
    FROM appointments
        WHERE appointment_id=?
        AND status="Booked"
    """,(appointment_id,))
    appointment=cursor.fetchone()

    if appointment is None:
        connection.close()
        return "Appointment not found or cancelled!"

    cursor.execute("""
    UPDATE appointments
    SET status="Cancelled" WHERE appointment_id=?
    """,(appointment_id,))
    connection.commit()
    connection.close()
    return "Appointment Cancelled Successfully!"

"""def get_patient_appointments(name, phone):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
       """""" SELECT
            appointments.appointment_id,
            doctors.name,
            doctors.specialization,
            appointments.appointment_date,
            appointments.appointment_time,
            appointments.status,
            doctors.consultation_fee
        FROM appointments
        JOIN patients
            ON appointments.patient_id = patients.patient_id
        JOIN doctors
            ON appointments.doctor_id = doctors.doctor_id
        WHERE patients.name = ?
        AND patients.phone = ?
    , (name, phone))

    appointments = cursor.fetchall()

    connection.close()

    return appointments

    name = input("Enter patient name to get your appointment details:").strip()



    phone= input("Enter phone number to get your appointment details:").strip()


    appointments = get_patient_appointments(name, phone)

    if appointments:
        for appointment in appointments:
          print("\nAppointment ID:", appointment[0])
          print("Doctor:", appointment[1])
          print("Specialization:", appointment[2])
          print("Date:", appointment[3])
          print("Time:", appointment[4])
          print("Status:", appointment[5])
          print("Consultation Fee: ₹", appointment[6])
    else:
     print("No appointments found.")"""
def delete_patient():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM patients")

    connection.commit()
    connection.close()

    print("All patient records deleted")
def delete_doctors():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM doctors")

    connection.commit()
    connection.close()
    print("All doctor records deleted")

def get_booked_appointments():
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute(
        """
        SELECT 
        appointments.appointment_id,
        patients.name,
        doctors.name,
        appointments.appointment_date,
        appointments.appointment_time,
        appointments.status,
        doctors.consultation_fee
        FROM appointments
        JOIN patients
        ON appointments.patient_id=patients.patient_id
        JOIN doctors
        ON appointments.doctor_id=doctors.doctor_id
        WHERE appointments.status='Booked'
    
    """)
    appointments=cursor.fetchall()
    print(appointments)
    connection.close()
    return appointments

def reschedule_appointment(appointment_id, new_date, new_time):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # Check whether appointment exists and is currently booked
    cursor.execute("""
        SELECT doctor_id,appointment_date
        FROM appointments
        WHERE appointment_id = ?
        AND status = 'Booked'
    """, (appointment_id,))

    appointment = cursor.fetchone()

    if not appointment:
        connection.close()
        return "Appointment not found or it is not currently booked."

    doctor_id = appointment[0]
    appointment_date=appointment[1]
    today=datetime.today().strftime("%Y-%m-%d")
    if appointment_date<today:
        connection.close()
        return"Past appointments cannot be rescheduled."
    # Check whether doctor is already booked at the new date/time
    cursor.execute("""
        SELECT appointment_id
        FROM appointments
        WHERE doctor_id = ?
        AND appointment_date = ?
        AND appointment_time = ?
        AND status = 'Booked'
        AND appointment_id != ?
    """, (doctor_id, new_date, new_time, appointment_id))

    existing = cursor.fetchone()

    if existing:
        connection.close()
        return "Doctor is already booked at the new date and time."

    # Update appointment
    cursor.execute("""
        UPDATE appointments
        SET appointment_date = ?,
            appointment_time = ?
        WHERE appointment_id = ?
    """, (new_date, new_time, appointment_id))

    connection.commit()
    connection.close()

    return "Appointment rescheduled successfully."

def find_doctor_by_name(name):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT doctor_id, name, specialization, experience, consultation_fee
        FROM doctors
        WHERE name = ?
    """, (name,))

    doctors = cursor.fetchall()

    connection.close()

    return doctors

if __name__=="__main__":

    create_doctors_table()
    #insert_doctors()
    create_patients_table()
    #insert_patients()
    get_patients()
    #delete_patient()
    get_doctors()
    #delete_doctors()
    create_appointments_table()
    get_booked_appointments()
    #book_appointment_from_user()
    #doctors=get_doctors()
    #book_appointment(1,1,"2026-08-15","10:00")
    #book_appointment_from_user()
   # find_patient("Ravi","9876543210")
   # find_doctor("Cardiology")
   # print("\n",doctors)
    #get_appointments()
    #cancel_appointment(8)
    # convert_old_appointment_dates()