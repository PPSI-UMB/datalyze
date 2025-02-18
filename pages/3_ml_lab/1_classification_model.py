import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split

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
st.title('Classification Model')
st.write('''
         Welcome to the Classification Model Builder! Leverage powerful machine learning algorithms to classify your data with precision. 
         Configure your dataset, select features, and build a robust classification model seamlessly.
         ''')

if 'dataset' not in st.session_state: # Ensure that the dataset has been uploaded
    st.warning('No dataset found. Please upload a dataset on the Home page first.')
elif st.session_state['problem_type'] == 'Regression' or st.session_state['problem_type'] == 'None': # Ensure that the problem type is Classification
    st.warning('This page is for **Classification** only. Please select a **Classification** problem type on the Home page.')
else: # Main Code Start From Here
    st.subheader('Data Preparation')
    st.write('''
             Prepare your dataset for classification by selecting the relevant features and target variable. 
             Fine-tune your data selection to ensure optimal model performance before training begins.
             ''')
    
    # Data Preparation
    # 1. Select Dataset
    dataset_choice = st.selectbox('**Select Dataset**', ['Current Dataset', 'Raw Dataset'])
    if dataset_choice == 'Current Dataset':
        selected_df = st.session_state['dataset_final'].copy()
    else:
        selected_df = st.session_state['dataset'].copy()
    col1, col2 = st.columns([3, 1])
    with col1:
        st.dataframe(selected_df, use_container_width=True)
        st.write('Dataset Shape:', selected_df.shape)
    with col2:
        st.write(pd.DataFrame(selected_df.dtypes, columns=['Data Type']), use_container_width=True)
        
    col1, col2 = st.columns(2)
    with col1:
        # 2. Select Features
        features = st.multiselect('**Select Dependent features (X variables)**', selected_df.columns, selected_df.columns)
        target = st.selectbox('**Select target (Y variable)**', selected_df.columns)
    with col2:
        # 3. Data Splitting
        train_size = st.slider('**Train Size**', min_value=0.1, max_value=0.9, step=0.05, value=0.8)
        test_size = st.slider('**Test Size**', min_value=0.1, max_value=0.9, value=1-train_size, disabled=True)
        random_state = st.number_input('**Random State**', min_value=0, max_value=100, value=42)
    
    # Apply Changes Button
    st.write('')
    if st.button('Apply Changes', use_container_width=True):
        processed_df = selected_df.copy()
        X = processed_df[features]
        y = processed_df[target]
        if X.select_dtypes(include=['object', 'datetime']).shape[1] > 0 or y.dtype in ['object', 'datetime']:
            st.error('Selected features contain non-numeric data types. Please select only numeric features.')
        elif X.isnull().sum().sum() > 0 or y.isnull().sum() > 0:
            st.error('Selected features contain missing values. Please handle missing values first.')
        else:
            X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_size, random_state=random_state)
            st.success('Data has been split successfully!')
            st.write('Training Set Shape:', X_train.shape, y_train.shape)
            st.write('Test Set Shape:', X_test.shape, y_test.shape)
    st.write('')

    # Model Selection
    st.subheader('Model Selection')
    st.write('''
            Select the best classification model for your data.
            Choose between manual model selection, where you can specify the algorithm and configure hyperparameters yourself, 
            or leverage automated hyperparameter tuning for optimal performance.
            ''')
    tab1, tab2 = st.tabs(['Manual', 'Hyperparameter Tuning'])
     
    with tab1:
         st.warning('This section is under development. Please check back later.')

    with tab2:
        st.warning('This section is under development. Please check back later.')