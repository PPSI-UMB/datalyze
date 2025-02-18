import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import RobustScaler

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
st.title('Data Normalization')
st.write('''
        Data normalization is a process of scaling numerical data to a standard range to ensure that the data is consistent and comparable.
        This process is crucial to prevent features with large values from dominating the model and to improve the model's performance.
        ''')

if 'dataset_final' not in st.session_state: # Ensure that the dataset has been uploaded
    st.warning('No dataset found. Please upload a dataset on the Home page first.')
elif st.session_state['dataset_final'].isnull().sum().sum() > 0: # Ensure that the dataset does not contain missing values
    st.warning('The dataset contains missing values. Please handle missing values on the Data Cleaning page first.')
else: # Main Code Start From Here
    df = st.session_state['dataset_final'].copy()
    
    # Display Current Dataset Function
    def display_current_dataset(df):
        st.markdown('---')
        st.subheader('Current Dataset')
        col1, col2 = st.columns([3, 1])
        with col1:
            st.dataframe(df, use_container_width=True)
            st.write('Shape:', df.shape)
        with col2:
            st.write(pd.DataFrame(df.dtypes, columns=['Data Type']), use_container_width=True)
    
    st.subheader('Select Normalization Method')
    normalization_method = st.selectbox('**Select normalization method**', ['Min-Max Normalization', 'Z-Score Standardization', 'Robust Scaling'], label_visibility='collapsed')
    if st.button('Normalize Data'):
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        df_numeric = df[numeric_cols].copy()
        if normalization_method == 'Min-Max Normalization':
            scaler = MinMaxScaler()
            df_numeric[numeric_cols] = scaler.fit_transform(df_numeric[numeric_cols])
        elif normalization_method == 'Z-Score Standardization':
            scaler = StandardScaler()
            df_numeric[numeric_cols] = scaler.fit_transform(df_numeric[numeric_cols])
        elif normalization_method == 'Robust Scaling':
            scaler = RobustScaler()
            df_numeric[numeric_cols] = scaler.fit_transform(df_numeric[numeric_cols])
        df.update(df_numeric)
        st.session_state['dataset_final'] = df
        st.rerun()
            
    display_current_dataset(df)