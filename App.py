import streamlit as st

st.set_page_config(page_title='Datalyze', page_icon='images/logo.png')

# st.sidebar.image('images/logo.png', use_container_width=True)

# Sidebar menu:
# 0. Home Page
home = st.Page('pages/home.py', title='Home', icon='🏠', default=True)

# 1. EDA
eda_automation = st.Page('pages/1_eda/1_eda_automation.py', title='EDA Automation', icon='📊')
data_visualization = st.Page('pages/1_eda/2_data_visualization.py', title='Data Visualization', icon='📈')

# 2. Data Preprocessing
data_cleaning = st.Page('pages/2_data_preprocessing/1_data_cleaning.py', title='Data Cleaning', icon='🧹')
feature_engineering = st.Page('pages/2_data_preprocessing/2_feature_engineering.py', title='Feature Engineering', icon='⚙️')
data_normalization = st.Page('pages/2_data_preprocessing/3_data_normalization.py', title='Data Normalization', icon='⚖️')

# 3. Machine Learning Lab
classification_model = st.Page('pages/3_ml_lab/1_classification_model.py', title='Classification Model', icon='🎯')
regression_model = st.Page('pages/3_ml_lab/2_regression_model.py', title='Regression Model', icon='🔢')

pg = st.navigation(
    {
        '': [home],
        'Exploratory Data Analysis': [eda_automation, data_visualization],
        'Data Preprocessing': [data_cleaning, feature_engineering, data_normalization],
        'Machine Learning Lab': [classification_model, regression_model]
    }
)

pg.run()
