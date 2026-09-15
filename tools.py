from langchain_core.tools import tool
from database import find_doctor,find_doctor_by_name,book_appointment,cancel_appointment,get_appointments,find_patient,get_patient_appointments,find_patient_by_name,get_patient_appointment_history,reschedule_appointment

@tool
def find_doctor_tool(specialization:str):
    """
    Find a doctor by Specialization.

    """
    return find_doctor(specialization)

@tool
def book_appointment_tool(
        patient_id:int,
        doctor_id:int,
        appointment_date:str,
        appointment_time:str
):
    """
    Book an appointment.
    IMPORTANT:
    -use the exact appointment date requested by the user.
    -use the exact appointment time requested by the user.
    -NEVER change user's requested date or time.
    -Do not choose a different time automatically.
    -If the requested time is invalid,the booking function will reject it.
    appointment_date must be in DD-MM-YYYY format.
    appointment_time must be in HH:MM format.

    """
    result=book_appointment(
        patient_id,
        doctor_id,
        appointment_date,
        appointment_time
    )
    #print("Booking Tool Result:",result)
    return result
@tool
def cancel_appointment_tool(appointment_id:int):
    """

    Cancel a booked hospital appointment using its appointment ID.
    """
    result=cancel_appointment(appointment_id)
    return result
@tool
def get_appointments_tool():
    """
    Get all hospital appointments with patient,doctor,date,time,status, and fee.

    """
    appointments=get_appointments()
    if not appointments:
        return "There are no appointments."
    return str(appointments)

@tool
def get_patient_appointments_tool(patient_id:int):
    """
    Get all appointments for a patient using their patient ID
   
    """
    appointments=get_patient_appointments(patient_id)
    if not appointments:
         return f"There are no appointments with {patient_id}"
    return str(appointments)

@tool
def get_patient_appointment_history_tool(patient_id: int):
    """
    Get the complete appointment history for a patient,
    including past, cancelled, and booked appointments.
    """
    appointments = get_patient_appointment_history(patient_id)

    if not appointments:
        return f"There is no appointment history for patient {patient_id}."

    return str(appointments)
@tool
def find_patient_tool(name:str,phone:str):
    """
    Find a registered patient using their name and phone number

    """
    patient=find_patient(name,phone)
    if patient is None:
        return "Patient not found"
    return str(patient)

@tool
def find_patient_by_name_tool(name: str):
    """
    Find registered patients using their name.
    """
    patients = find_patient_by_name(name)

    if not patients:
        return "Patient not found."

    if len(patients) > 1:
        return (
            "Multiple patients found with this name. "
            "Please provide the patient's phone number."
        )

    return str(patients[0])

@tool
def reschedule_appointment_tool(appointment_id:int,new_date:str,new_time):
    """

    Reschedule an existing booked appointment to a new date and time.
    """
    result=reschedule_appointment(appointment_id,new_date,new_time)
    return result

@tool
def find_doctor_by_name_tool(name: str):
    """
    Find a doctor by name.
    """
    doctors = find_doctor_by_name(name)

    if not doctors:
        return "Doctor not found."

    if len(doctors) > 1:
        return "Multiple doctors found with this name. Please provide the specialization."

    return str(doctors[0])