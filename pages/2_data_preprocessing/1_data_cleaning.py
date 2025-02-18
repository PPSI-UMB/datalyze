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
st.title('Data Cleaning')
st.write('''
        Data cleaning is a process of preparing and correcting data by removing or correcting errors, inconsistencies, and inaccuracies.
        This process is crucial to ensure that the dataset is accurate, complete, and ready for analysis.
        ''')

if 'dataset_final' not in st.session_state: # Ensure that the dataset has been uploaded
    st.warning('No dataset found. Please upload a dataset on the Home page first.')
else: # Main Code Start From Here
    df = st.session_state['dataset_final'].copy()
    tab1, tab2, tab3 = st.tabs(['Change Data Type', 'Remove Duplicate Data', 'Missing Value Handler'])
    
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
    
    # Change Data Type
    with tab1:
        st.subheader('Change Data Type')
        st.write('''
                 This section allows you to change the data type of selected features to ensure that the data is in the correct format.
                 Select features and the new data type to change the data type of the selected features.
                 ''')
        
        features_to_change = st.multiselect('**Select features to change data type**', df.columns)
        if features_to_change:
            new_dtype = st.selectbox('**Select new data type**', options=['int64', 'float64', 'object', 'boolean'])
            if st.button('Change Data Type'):
                success = True
                for column in features_to_change:
                    try:
                        if new_dtype == 'boolean':
                            unique_values = df[column].dropna().unique()
                            if len(unique_values) != 2:
                                raise ValueError(f'Feature \'{column}\' does not have exactly 2 unique values.')
                        if new_dtype == 'boolean':
                            unique_values = df[column].dropna().unique()
                            mapping = {unique_values[0]: False, unique_values[1]: True}
                            df[column] = df[column].map(mapping)
                        else:
                            df[column] = df[column].astype(new_dtype)
                    except Exception as e:
                        if 'could not convert string to float' in str(e):
                            st.error(f'Data type cannot be changed for feature \'{column}\'. It contains non-numeric characters.')
                        else:
                            st.error(f'Data type cannot be changed for feature \'{column}\'. Error: {e}')
                        success = False
                if success:
                    st.session_state['dataset_final'] = df
                    st.rerun()
        else:
            st.warning('Please select features to change data type')
            
        display_current_dataset(df)
    
    # Remove Duplicate Data
    with tab2:
        st.subheader('Remove Duplicate Data')
        st.write('''
                 This section helps you identify and remove duplicate records from the dataset, which can cause inaccuracies in analysis.
                 The duplicate data will be displayed below, and you can choose to delete them.
                 ''')
        
        duplicates = df[df.duplicated()]
        num_duplicates = duplicates.shape[0]
        percent_duplicates = (num_duplicates / df.shape[0]) * 100
        st.write(f'**Number of duplicate data: {num_duplicates}/{df.shape[0]} ({percent_duplicates:.2f}%)**')
        st.dataframe(duplicates, use_container_width=True)
        if not duplicates.empty:
            if st.button('Delete Duplicate Data'):
                df = df.drop_duplicates()
                df.reset_index(drop=True, inplace=True)
                st.session_state['dataset_final'] = df
                st.rerun()
        else:
            st.success('No duplicate data found')
            
        display_current_dataset(df)
    
    # Missing Value Handler
    with tab3:
        st.subheader('Missing Value Handler')
        st.write('''
                This section helps you identify and provides options to handle missing values in the dataset by either deleting them or filling them with appropriate values such as the mean or the most frequent value.
                The missing data will be displayed below, and you can choose the solution method to handle them.
                ''')
        
        null_data = df[df.isnull().any(axis=1)]
        num_null = null_data.shape[0]
        percent_null = (num_null / df.shape[0]) * 100
        missing_data = df.isnull().sum()
        total_missing = missing_data.sum()
        percent_missing = (total_missing / df.size) * 100
        st.write(f'**Number of missing value: {total_missing}/{df.shape[0]} ({percent_missing:.2f}%)**')
        st.dataframe(null_data, use_container_width=True)
        if not null_data.empty:
            solution_method = st.selectbox('**Select Solution Method**', ['Delete', 'Fill with Mean Value (integer & float data type)', 'Fill with Most Frequent Value'])
            if solution_method == 'Fill with Most Frequent Value':
                data_type_option = st.radio('**Select Data Type to Apply**', ['Integer & Float', 'Boolean', 'All of above'])
            if st.button('Start Action'):
                if solution_method == 'Delete':
                    df = df.dropna()
                elif solution_method == 'Fill with Mean Value (integer & float data type)':
                    df = df.apply(lambda x: x.fillna(x.mean()) if x.dtype in ['int64', 'float64'] else x, axis=0)
                elif solution_method == 'Fill with Most Frequent Value':
                    if data_type_option == 'Integer & Float':
                        df = df.apply(lambda x: x.fillna(x.mode()[0]) if x.dtype in ['int64', 'float64'] else x, axis=0)
                    elif data_type_option == 'Boolean':
                        df = df.apply(lambda x: x.fillna(x.mode()[0]) if x.dtype == 'bool' else x, axis=0)
                    elif data_type_option == 'All of above':
                        df = df.apply(lambda x: x.fillna(x.mode()[0]) if x.dtype in ['int64', 'float64', 'bool'] else x, axis=0)
                df.reset_index(drop=True, inplace=True)
                st.session_state['dataset_final'] = df
                st.rerun()
        else:
            st.success('No missing value found')
            
        display_current_dataset(df)
