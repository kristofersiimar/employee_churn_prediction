import streamlit as st
import pandas as pd
import numpy as np
import pickle
from PIL import Image


app_mode = st.sidebar.selectbox('Select Page', ['Home', 'Predict Churn'])

if app_mode == 'Home':
    logo = Image.open('blinkist_logo.jpg')
    st.image(logo, width = 50)
    st.title('Employee Churn Prediction Tool')
    st.markdown('Hi there 🙋‍!')
    st.markdown("""We are here to support you and our lovely colleagues! Please use the Predict Churn tool 
                (from sidebar) to identify 
                people who are happy and those who feel not too happy working at the company 😇!""")
    home_image = Image.open('home_pic.jpg')
    st.image(home_image, caption = 'Teamwork helps to put Big ideas into small packages!')


elif app_mode == 'Predict Churn':

    st.subheader('Fill in employee details to get prediction 🕵️‍')
    prop = {'Low': 1, 'Medium': 2, 'High': 3}
    satisfaction_level = st.number_input("satisfaction level (range 0 to 1)", min_value=0.0,  max_value=1.0)
    average_montly_hours = st.number_input("average montly hours", min_value=0, max_value=300)
    promotion_last_5year = st.number_input("promotion last 5 years", min_value=0, max_value=300)
    salary = st.radio("salary", tuple(prop.keys()))

    salary_low, salary_medium, salary_high = 0, 0, 0
    if salary == 'High':
        salary_high = 1
    elif salary == 'Low':
        salary_low = 1
    else:
        salary_medium = 1


    employee_data = {
        'satisfaction_level': satisfaction_level,
        'average_montly_hours ': average_montly_hours ,
        'promotion_last_5year': promotion_last_5year,
        'salary': [salary_low, salary_medium, salary_high],
        }

    features = [satisfaction_level, average_montly_hours, promotion_last_5year, employee_data['salary'][0],
                employee_data['salary'][1], employee_data['salary'][2]]

    results = np.array(features).reshape(1, -1)

    if st.button("Predict"):

        picklefile = open("emp-model.pkl", "rb")
        model = pickle.load(picklefile)

        prediction = model.predict(results)
        if prediction[0] == 0:
            st.success('Employee will not churn 🥳')
        elif prediction[0] == 1:
            st.error('Employee will churn 😢')

    df = pd.read_csv('emp_data.csv')
    display_df = st.checkbox(label = 'Want to see underlying data?')
    if display_df:
        st.write(df[['satisfaction_level', 'average_montly_hours', 'promotion_last_5years',
                     'salary', 'left']].head(5))
