import streamlit as st
import pandas as pd

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
st.title('Feature Engineering')
st.write('''
    Welcome to the Feature Engineering page. On this page, you can enhance your dataset by adding new features, removing unnecessary ones, renaming existing features, and performing one-hot encoding on categorical features. 
    Utilize these tools to refine your dataset and improve the performance of your machine learning models.
    ''')

if 'dataset_final' not in st.session_state: # Ensure that the dataset has been uploaded
    st.warning('No dataset found. Please upload a dataset on the Home page first.')
elif st.session_state['dataset_final'].isnull().sum().sum() > 0: # Ensure that the dataset does not contain missing values
    st.warning('The dataset contains missing values. Please handle missing values on the Data Cleaning page first.')
else: # Main Code Start From Here
    df = st.session_state['dataset_final'].copy()
    tab1, tab2, tab3, tab4 = st.tabs(['Add Feature', 'Remove Feature', 'Rename Feature', 'One-Hot Encoding'])
    
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
                
    # Add Feature
    with tab1:
        st.subheader('Add Feature')
        st.write('''
                 This section allows you to add new features to the dataset by performing mathematical operations on existing features.
                 Select the type of operation to proceed.
                 ''')
        
        operation_type = st.selectbox('**Select operation type**', ['None', 'Basic Mathematical Operation', 'Polynomial'])
        if operation_type == 'Basic Mathematical Operation':
            new_feature_name = st.text_input('**Enter the name for the new feature**')
            features = st.multiselect('**Select two numerical features**', df.columns)
            if len(features) == 2:
                if not (pd.api.types.is_numeric_dtype(df[features[0]]) and pd.api.types.is_numeric_dtype(df[features[1]]) and not pd.api.types.is_bool_dtype(df[features[0]]) and not pd.api.types.is_bool_dtype(df[features[1]])):
                    st.error('Selected features must be numeric (integer or float).')
                else:
                    operation = st.selectbox('Select operation', ['Addition', 'Subtraction', 'Multiplication', 'Division'])
                    if st.button('Add Feature'):
                        if not new_feature_name:
                            st.error('Please enter a name for the new feature.')
                        else:
                            new_feature = None
                            if operation == 'Addition':
                                new_feature = df[features[0]] + df[features[1]]
                            elif operation == 'Subtraction':
                                new_feature = df[features[0]] - df[features[1]]
                            elif operation == 'Multiplication':
                                new_feature = df[features[0]] * df[features[1]]
                            elif operation == 'Division':
                                new_feature = df[features[0]] / df[features[1]]
                            df[new_feature_name] = new_feature
                            st.success(f"New feature '{new_feature_name}' added to the dataset")
                            st.session_state['dataset_final'] = df
                            st.rerun()
            elif len(features) > 2:
                st.error('Please select only two features.')
            else:
                st.warning('Please select two numerical features (integer or float) to add a new feature')
        elif operation_type == 'Polynomial':
            new_feature_name = st.text_input('**Enter the name for the new feature**')
            feature = st.selectbox('**Select a numerical feature**', df.columns)
            if feature:
                if not (pd.api.types.is_numeric_dtype(df[feature]) and not pd.api.types.is_bool_dtype(df[feature])):
                    st.error('Selected feature must be numeric (integer or float).')
                else:
                    degree = st.number_input('**Select polynomial degree**', min_value=2, step=1)
                    if st.button('Add Feature'):
                        if not new_feature_name:
                            st.error('Please enter a name for the new feature.')
                        else:
                            new_feature = df[feature] ** degree
                            df[new_feature_name] = new_feature
                            st.success(f"New feature '{new_feature_name}' added to the dataset")
                            st.session_state['dataset_final'] = df
                            st.rerun()
        else:
            st.warning('Please select an operation type to add a new feature')
            
        display_current_dataset(df)
            
    # Remove Feature
    with tab2:
        st.subheader('Remove Feature')
        st.write('''
                 This section allows you to remove features that are not needed from the dataset.
                 Select features to remove and click the 'Remove Feature' button to remove the selected features.
                 ''')
        
        features_to_remove = st.multiselect('**Select features to remove**', df.columns)
        if st.button('Remove Feature'):
            if not features_to_remove:
                st.warning('Please select features to remove')
            else:
                df.drop(columns=features_to_remove, inplace=True)
                st.success('Selected features removed from the dataset')
                st.session_state['dataset_final'] = df
                st.rerun()
                
        display_current_dataset(df)
            
    # Rename Feature
    with tab3:
        st.subheader('Rename Feature')
        st.write('''
                 This section allows you to rename features in the dataset.
                 Select a feature and enter a new name to rename the selected feature.
                 ''')
        
        feature_to_rename = st.selectbox('**Select feature to rename**', df.columns)
        new_feature_name = st.text_input('**Enter the new name for the feature**')
        if st.button('Rename Feature'):
            if not feature_to_rename:
                st.warning('Please select a feature to rename')
            elif not new_feature_name:
                st.warning('Please enter a new name for the feature')
            else:
                df.rename(columns={feature_to_rename: new_feature_name}, inplace=True)
                st.success(f"Feature '{feature_to_rename}' renamed to '{new_feature_name}'")
                st.session_state['dataset_final'] = df
                st.rerun()
                
        display_current_dataset(df)
    
    # One-Hot Encoding
    with tab4:
        st.subheader('One-Hot Encoding')
        st.write('''
                 This section allows you to convert categorical features to numerical features using one-hot encoding.
                 Select categorical features to encode and click the 'One-Hot Encode' button to convert the features.
                 ''')
        
        categorical_features = df.select_dtypes(include=['number', 'object']).loc[:, df.nunique() <= 10].loc[:, df.nunique() > 2]
        categorical_features = categorical_features.loc[:, ~categorical_features.apply(pd.api.types.is_bool_dtype)].columns
        if len(categorical_features) == 0:
            st.warning('No categorical features available for one-hot encoding. Ensure there are features with unique values between 3 and 10.')
        else:
            features_to_encode = st.multiselect('**Select categorical features to encode**', categorical_features)
            if st.button('One-Hot Encode'):
                if not features_to_encode:
                    st.warning('Please select categorical features to encode')
                else:
                    df = pd.get_dummies(df, columns=features_to_encode, drop_first=True)
                    st.session_state['dataset_final'] = df
                    st.rerun()
                    
        display_current_dataset(df)