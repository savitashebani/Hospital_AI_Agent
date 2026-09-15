import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import ToolMessage, content
from langchain.agents import create_agent
from tools import find_doctor_tool, book_appointment_tool, cancel_appointment_tool, get_appointments_tool, \
    find_patient_tool, get_patient_appointments_tool, find_patient_by_name_tool, \
    get_patient_appointment_history_tool,reschedule_appointment_tool,find_doctor_by_name_tool
from langgraph.checkpoint.memory import InMemorySaver
load_dotenv()

llm=ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
tools=[find_doctor_tool,book_appointment_tool,cancel_appointment_tool,get_appointments_tool,find_patient_tool,get_patient_appointments_tool,find_patient_by_name_tool,get_patient_appointment_history_tool,reschedule_appointment_tool,find_doctor_by_name_tool] #Here is the list of tools available to the AI.
"""llm_with_tools=llm.bind_tools(tools) #Give these tools to the LLM so it knows they are available.
messages=[
    (
        "human",
        "Find me a doctor who specializes in Cardiology."
    )
    ]
# Step 1: Ask the LLM
response=llm_with_tools.invoke(messages)
print("LLM TOOL CALL:")
print(response.tool_calls)

# Step 2: Execute the tool
tool_call=response.tool_calls[0]  #gets the first tool request from the LLM.
result=find_doctor_tool.invoke(
    tool_call["args"]
)
print("\n TOOL RESULT:")
print(result)

# Step 3: Give the tool result back to the LLM
messages.append(response)
messages.append(
    ToolMessage(
          content=str(result),
          tool_call_id=tool_call["id"]
     )
)
# Step 4: Ask the LLM for the final answer
final_response=llm_with_tools.invoke(messages)
print("\n FINAL ANSWER:")
print(final_response.content)

"""
"""USER
 ↓
1️⃣ ASK AI
 ↓
2️⃣ AI CHOOSES TOOL
 ↓
3️⃣ PYTHON RUNS TOOL
 ↓
4️⃣ RESULT GOES BACK TO AI
 ↓
FINAL ANSWER"""
checkpointer=InMemorySaver()
# 3. Create the agent
agent=create_agent(
    model=llm,
    tools=tools,
    system_prompt=(
        "You are a helpful hospital assistant. "
    "Use the available tools to find doctors, find patients, "
    "book appointments, cancel appointments, and view appointments. "
    
    "IMPORTANT PATIENT APPOINTMENT RULE: "
    "When the user asks for a specific patient's appointments, "
    "first identify the patient and then use the "
    "get_patient_appointments_tool to retrieve that patient's appointments. "
       
       
    "When the user asks for a patient's appointment history,"
    "first identify the patient and then use the"
    "get_patient_appointment_history_tool to retrieve the complete history. "
        
    "IMPORTANT BOOKING RULES: "
    "Never change a date or time requested by the user. "
    "Never automatically choose another appointment time. "
    "If a requested time is invalid, tell the user and ask for confirmation "
    "before using a different time. "
    "Only book a different time after the user explicitly confirms that time."
     
     "IMPORTANT APPOINTMENT STATUS RULE:"
     "When showing appointment history, do not describe a past appointment"
     "as a current appointment just because its database status is 'Booked'"

     "A 'Booked' appointment with a date before today is a past appointment."
     "A 'Booked' appointment with today or a future date is an upcoming appointment."

     "When summarizing appointment history, clearly distinguish between"
     "past booked appointments, upcoming booked appointments, and cancelled appointments."
        
     "IMPORTANT RESCHEDULE RULE:"
     " When the user wants to reschedule an appointment,"
     "first identify the appointment ID."
     "Only reschedule an appointment that is currently booked."
     "Never reschedule a cancelled or past appointment."
     "The new date and time must be provided by the user."
      "Never automatically choose a different date or time."
        
     "When the user provides a doctor's name, use"
     "find_doctor_by_name_tool to identify the doctor"
    "instead of asking for the specialization unless necessary."
        
    "IMPORTANT APPOINTMENT QUERY RULE:"
    "When the user asks for 'all appointments',"
    "'appointment history', 'complete appointments'"
    "or similar wording, use"
    "get_patient_appointment_history_tool."

    "When the user asks specifically for 'upcoming appointments',"
    "use get_patient_appointments_tool."

    "Do not use get_patient_appointments_tool when the user asks"
    "for all appointments."
        
    "IMPORTANT PATIENT IDENTIFICATION RULE:"

    "If multiple patients have the same name, never choose one"
    "automatically."

    "Ask the user for the patient's phone number or Patient ID"
    "before performing any appointment operation."
    ),
    checkpointer=checkpointer
)
config={
    "configurable":{
        "thread_id":"hospital_conversation_1"
    }
}
# 4. Ask the agent
response=agent.invoke({
     "messages":[
            {
                "role":"user",
                "content":"Find doctors specializing in Dermatology."
            }
        ]
    },
    config
)
"""response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Yes, book it at 11:30."
            }
        ]
    },
    config
)"""

# 5. Print the final AI response
print(response["messages"][-1].content)
