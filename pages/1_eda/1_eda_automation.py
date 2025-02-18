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
st.title('EDA Automation')
st.write('This is the EDA Automation page.')

if 'dataset_final' not in st.session_state: # Ensure that the dataset has been uploaded
    st.warning('No dataset found. Please upload a dataset on the Home page first.')
else: # Main Code Start From Here
    st.warning('This page is under development. Please check back later.')