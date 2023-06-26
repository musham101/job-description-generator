import streamlit as st
import requests
import json, time
from globals import API_KEY

api_key = API_KEY

def convert_string_to_json(json_string):
    try:
        json_object = json.loads(json_string)
        return json_object
    except ValueError as e:
        print("Invalid JSON format:", e)
        return None

def make_request(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key,
    }
    json_data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'user',
                'content': f'{prompt}',
            },
        ],
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
    json_response = json.loads(response.text)
    answers = json_response["choices"][0]["message"]["content"]
    resp = convert_string_to_json(answers)
    if resp == None:
        return answers
    else:
        resp

st.title("Job Description Generator | ChatGPT")
st.subheader("Enter details")

job_title = st.text_input("Job Title")
req_exp = st.text_input("Req Experience")
skills = st.text_input("Skills")
gender = st.radio("Gender", ['male', 'female'])
company = st.text_input("Company Name")
office_location = st.text_input("Company Address")

prompt = f"create me a job description for a job with job title {job_title}, required experience {req_exp}, gender {gender}, skills required are {skills}, company {company} and office location {office_location}."

if st.button('Get Job Description'):
    start_time = time.time()
    api_response = make_request(prompt)
    api_response = {
        "job_description": api_response
    }
    end_time = time.time()
    elapsed_time = end_time - start_time
    st.write("Response Time: " + str(elapsed_time) + " Seconds")

    raw_response, formated_response = st.columns(2)

    raw_response.width = 500
    formated_response.width = 500

    with raw_response:
        st.subheader('ChatGPT Response:')
        st.write(api_response)

    with formated_response:
        st.subheader('Extracted Response:')
        st.write(api_response['job_description'])