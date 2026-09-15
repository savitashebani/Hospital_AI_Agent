import streamlit as st
import pandas as pd
from agent import agent as hospital_agent
import sqlite3
from database import book_appointment,get_appointments,cancel_appointment,get_booked_appointments
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥"
)
st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)
DB_NAME="hospital.db"
def get_connection():
    return sqlite3.connect(DB_NAME)
def get_patients():
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("""
      SELECT patient_id,name 
      FROM patients
      """)
    patients=cursor.fetchall()
    connection.close()
    return patients
def get_all_patients():
    connection=get_connection()
    cursor=connection.cursor()
    cursor.execute("""
    SELECT patient_id,name,age,phone
    FROM patients""")
    patients=cursor.fetchall()
    connection.close()
    return patients
def get_doctors():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT doctor_id, name, specialization,experience,consultation_fee
        FROM doctors
    """)

    doctors = cursor.fetchall()

    connection.close()

    return doctors



st.markdown(
    '<div class="main-title">🏥 Hospital Management System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Smart and Simple Hospital Management</div>',
    unsafe_allow_html=True
)

st.write("Welcome to our Hospital Management System") #st.write() is used to display content on the page.

st.header("Patient Information")  #st.header() creates a section heading on your webpage.

st.sidebar.header("🏥 Hospital Menu")
menu=st.sidebar.selectbox(
"Choose an option",
    [ "🏠 Home",
        "👤 Patients",
        "👨‍⚕️ Doctors",
        "📅 Appointments",
        "🤖 AI Assistant"

    ]
)
st.sidebar.markdown("---")
st.sidebar.caption("Hospital Management System")
if menu == "🏠 Home":
    st.header("Welcome to the Hospital")
    st.write("Manage patients, doctors, and appointments from here.")

elif menu == "👤 Patients":
    st.header("👤 Patient Management")
    with st.form("Patients form"):
       patient_name = st.text_input("Patient Name")
       phone = st.text_input("Phone Number")
       age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        step=1
      )
       submitted=st.form_submit_button("Register Patient")
       if submitted:
         if not patient_name:
             st.error("Patient Name cannot be empty")
         elif not phone.isdigit():
             st.error("Phone number must contain only digits")
         elif len(phone)!=10:
             st.error("Phone number must contain 10 digits")
         else:
             connection=get_connection()
             cursor=connection.cursor()
             cursor.execute("""
             SELECT patient_id FROM patients WHERE phone=?""",(phone,))
             existing_patient=cursor.fetchone()
             if existing_patient:
                 st.error("Patient with this phone number already exists.")
             else:
                cursor.execute("""
                 INSERT INTO patients(name,age,phone)
                 VALUES(?,?,?)
                """,(patient_name,age,phone))
                connection.commit()


                st.success("Patient Registered successfully!")
                connection.close()
    st.subheader("Registered Patients")
    patients=get_all_patients()
    df=pd.DataFrame(
        patients,
        columns=["Patient ID","Name","Age","Phone"]
    )
    st.dataframe(df,width="stretch") #tells Streamlit to make the table stretch across the available page width..
elif menu == "👨‍⚕️ Doctors":
    st.header("👨‍⚕️ Doctor Management")
    doctors=get_doctors()

    specializations=[
        "All",
        "Cardiology",
        "Dermatology",
        "Orthopedics"
    ]
    selected_specializations=st.selectbox("select specialization",specializations)
   # st.write("Available Doctors.")
   # st.dataframe(doctors) #st.dataframe() gives you an interactive table. The user can scroll through it and work with larger datasets more easily.
    df=pd.DataFrame(
        doctors,
        columns=[
            "Doctor ID",
            "Doctor Name",
            "Specialization",
            "Experience",
            "Consultation Fee"
        ]
    )
    if selected_specializations!="All":
        df=df[df["Specialization"]==selected_specializations]
    st.dataframe(df)
elif menu == "📅 Appointments":
    st.header("📅 Appointment Management")
    patients=get_patients()
    doctors=get_doctors()
   # st.write(doctors)
    patient_names=[patient[1] for patient in patients]
    selected_patient=st.selectbox("Select Patient",patient_names)
    selected_patient_id=next(  # to fetch patient_id of selected patient
        patient[0]
        for patient in patients
        if patient[1]==selected_patient
    )
    specializations=[
        "Cardiology",
        "Dermatology",
        "Orthopedics"
    ]
    selected_specialization=st.selectbox("Select Specialization",specializations)

    filtered_doctors=[    #list comprehension take only doctor name if selected specialization matches
        doctor[1]
        for doctor in doctors
        if doctor[2]==selected_specialization
    ]
    selected_doctor=st.selectbox("Select Doctor",filtered_doctors)
    selected_doctor_id=next(
        doctor[0]
        for doctor in doctors
        if doctor[1]==selected_doctor
    )
    appointment_date=st.date_input("Select Appointment Date")
    time_slots = [
        "09:00",
        "09:30",
        "10:00",
        "10:30",
        "11:00",
        "11:30",
        "12:00",
        "12:30",
        "13:00",
        "13:30",
        "14:00",
        "14:30",
        "15:00",
        "15:30",
        "16:00",
        "16:30",
        "17:00",
        "17:30"
    ]

    appointment_time = st.selectbox(
        "Select Appointment Time",
        time_slots
    )
    st.write("Here you can book and manage appointments.")
    book_button=st.button("📅 Book Appointment")
    if book_button:
        book_appointment(
            selected_patient_id,selected_doctor_id,str(appointment_date),appointment_time
        )
        st.success("Appointment booked successfully!🎉")
    st.subheader("📋 Booked Appointments")
    appointments=get_appointments()

    df=pd.DataFrame(
        appointments,
        columns=[
            "Appointment ID",
            "Patient Name",
            "Doctor Name",
            "Date",
            "Time",
            "Status",
            "Consultation Fee"
        ]
    )
    st.dataframe(df,width="stretch")
    st.subheader("Cancel Appointment")
    booked_appointments=get_booked_appointments()
    if booked_appointments:
         appointment_options={
            f"ID:{appointment[0]}|{appointment[1]}|{appointment[2]}|{appointment[3]}":appointment[0]
                for appointment in booked_appointments
           }
         selected_appointment=st.selectbox("select appointment to cancel",list(appointment_options.keys()))
         selected_appointment_id=appointment_options[selected_appointment]


         if st.button("Cancel Appointment"):
           message=cancel_appointment(selected_appointment_id)
           st.success(message)
    else:
      st.info("There are no booked appointment to cancel.")

elif menu == "🤖 AI Assistant":
    st.header("🤖 Hospital AI Assistant")
    # Create chat history
    if "messages" not in st.session_state:
        st.session_state.messages=[]
    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    # Get new user message
    user_input=st.chat_input("Ask me anything about appointments...")
    if user_input:
        # Display user's message
        with st.chat_message("user"):
            st.write(user_input)

        # Save user's message
        st.session_state.messages.append({"role":"user","content":user_input})

        # Send message to Agent
        response=hospital_agent.invoke(
            {
                "messages":[
                    {
                        "role":"user",
                        "content":user_input
                    }
                ]
            },
            config={
                "configurable":{
                    "thread_id":"hospital_user"
                }
            }
        )
        final_message=response["messages"][-1].content
        # Display AI response
        with st.chat_message("assistant"):

          st.write(final_message)

          # Save AI response
        st.session_state.messages.append({
              "role":"assistant",
              "content":final_message
        })