import streamlit as st

# Page Style
st.markdown('''
    <style>
        .block-container {
            max-width: 80%;
            padding-top: 4.5rem;
        }
    </style>
    ''', unsafe_allow_html=True)

# Page Header 
st.title('Regression Model')
st.write('This is the Regression Model page.')

if 'dataset' not in st.session_state: # Ensure that the dataset has been uploaded
    st.warning('No dataset found. Please upload a dataset on the Home page first.')
elif st.session_state['problem_type'] == 'Classification' or st.session_state['problem_type'] == 'None': # Ensure that the problem type is Regression
    st.warning('This page is for **Regression** only. Please select a **Regression** problem type on the Home page.')
else: # Main Code Start From Here
    st.warning('This page is under development. Please check back later.')