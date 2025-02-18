import streamlit as st
import pandas as pd

# Page Style
st.markdown("""
    <style>
        .block-container {
            max-width: 80%;
            padding-top: 4.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Page Header 
st.title('Welcome to Datalyze!')
st.write('''**Datalyze** is a powerful data analytics platform that helps you transform raw data into meaningful insights. 
         With interactive visualizations, accurate reports, and advanced analytics equipped with machine learning, you can make smarter decisions and optimize your strategies with ease.
         ''')
st.write('Unlock the full potential of your data—start exploring now! 📊✨')
st.write('-----')

# Main Code Start From Here
# Upload Dataset
st.subheader('Upload Dataset')
file = st.file_uploader('label', type=['csv', 'xlsx'], label_visibility='collapsed')
col1, col2 = st.columns([3, 1])
with col1:
    if file:
        df = pd.read_csv(file) if file.name.endswith('csv') else pd.read_excel(file)
        st.dataframe(df)
        st.write('Shape:', df.shape)
        st.session_state['dataset'] = df
        st.session_state['dataset_final'] = df
        # Delete Dataset Button
        if st.button('Delete Dataset'):
            del st.session_state['dataset']
            del st.session_state['dataset_final']
            st.rerun()
    elif 'dataset' in st.session_state:
        df = st.session_state['dataset']
        st.dataframe(df)
        st.write('Raw Dataset Shape:', df.shape)
        # Delete Dataset Button
        if st.button('Delete Dataset'):
            del st.session_state['dataset']
            del st.session_state['dataset_final']
            st.rerun()
with col2:
    if 'dataset' in st.session_state:
        df = st.session_state['dataset']
        dtypes_df = pd.DataFrame(df.dtypes, columns=['Data Type'])
        st.write(dtypes_df, use_container_width=True)

# Select Problem Type
st.subheader('Select Problem Type')

def update_problem_type():
    st.session_state['problem_type'] = st.session_state['problem_type_selectbox']

# Set default value for selectbox
if 'problem_type' not in st.session_state:
    st.session_state['problem_type'] = 'None'
problem_type = st.selectbox('label', ['None', 'Classification', 'Regression'], index=['None', 'Classification', 'Regression'].index(st.session_state['problem_type']), label_visibility='collapsed', key='problem_type_selectbox', on_change=update_problem_type)
if 'problem_type' in st.session_state:
    if st.session_state['problem_type'] == 'Classification':
        st.success('You have selected **Classification** problem')
    elif st.session_state['problem_type'] == 'Regression':
        st.success('You have selected **Regression** problem')
    else:
        st.warning('Please select a problem type to use **Machine Learning Lab** section')
        
# Display Current Dataset
st.markdown('---')
st.subheader('Current Dataset')
col1, col2 = st.columns([3, 1])
with col1:
    df_current = st.session_state['dataset_final']
    dtypes_df_current = pd.DataFrame(df_current.dtypes, columns=['Data Type'])
    st.dataframe(df_current, use_container_width=True)
    st.write('Shape:', df_current.shape)
with col2:
    st.write(dtypes_df_current, use_container_width=True)
