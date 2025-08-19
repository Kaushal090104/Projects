import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from streamlit_option_menu import option_menu
import data_analysis_functions as function
import home_page
import base64
import data_preprocessing_function as preprocessing_function
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

 

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#uncomment the above lines of code when we want to remove made with streamlit logo and also the top right three-dots icon

home_page.set_bg_from_local("assets/bg6.jpg")  # <-- Update this to match your image path

# Create a Streamlit sidebar

# Set custom CSS
custom_css = home_page.custom_css


# Create the introduction section
st.title("Welcome to Automated Exploratory Data Analysis")



selected = option_menu(
    menu_title=None,
    options=['Home', 'Data Exploration', 'Data Preprocessing', 'AI Analysis'],  # Added 'AI Analysis'
    icons=['house-heart', 'bar-chart-fill', 'hammer', 'robot'],  # Added an icon for AI Analysis
    orientation='horizontal'
)

if selected == 'Home':
    home_page.show_home_page()


# Create a button in the sidebar to upload CSV
uploaded_file = st.sidebar.file_uploader("Upload Your CSV File Here", type=["csv","xls"])
use_example_data = st.sidebar.checkbox("Use Example Titanic Dataset", value=False)



if uploaded_file:
    df = function.load_data(uploaded_file)


    # get a copy of original df from the session state or create a new one. this is for preprocessing purposes
    if 'new_df' not in st.session_state:
        st.session_state.new_df = df.copy()

    

# Create a checkbox in the sidebar to choose between the example dataset and uploaded dataset

elif use_example_data:
    # Load the example dataset
    df = function.load_data(file="example_dataset/titanic.csv")

    # Set st.session_state.new_df to the example dataset for data preprocessing
    if 'new_df' not in st.session_state:
        st.session_state.new_df = df
   


# TODO: Some issue related to session_state. When we upload a new dataset, it does not reflect changes in the data preprocessing tab as we are using session state.
# and the data is defined only once. need to solve this issue.
# Temporary solution is to reload the page and upload a new dataset


# Display the dataset preview or any other content here
if uploaded_file is None and selected!='Home' and not use_example_data:
    # st.subheader("Welcome to DataExplora!")
    st.markdown("#### Use the sidebar to upload a CSV file or use the provided example dataset and explore your data.")
    
else:
    
    if selected=='Data Exploration':

        tab1, tab2 = st.tabs(['📊 Dataset Overview :clipboard', "🔎 Data Exploration and Visualization"])
        num_columns, cat_columns = function.categorical_numerical(df)
        
        
        with tab1: # DATASET OVERVIEW TAB
            st.subheader("1. Dataset Preview")
            st.markdown("This section provides an overview of your dataset. You can select the number of rows to display and view the dataset's structure.")
            function.display_dataset_overview(df,cat_columns,num_columns)


            st.subheader("3. Missing Values")
            function.display_missing_values(df)
            
            st.subheader("4. Data Statistics and Visualization")
            function.display_statistics_visualization(df,cat_columns,num_columns)

            st.subheader("5. Data Types")
            function.display_data_types(df)

            st.subheader("Search for a specific column or datatype")
            function.search_column(df)

        with tab2: 

            function.display_individual_feature_distribution(df,num_columns)

            st.subheader("Scatter Plot")
            function.display_scatter_plot_of_two_numeric_features(df,num_columns)


            if len(cat_columns)!=0:
                st.subheader("Categorical Variable Analysis")
                function.categorical_variable_analysis(df,cat_columns)
            else:
                st.info("The dataset does not have any categorical columns")


            st.subheader("Feature Exploration of Numerical Variables")
            if len(num_columns)!=0:
                function.feature_exploration_numerical_variables(df,num_columns)

            else:
                st.warning("The dataset does not contain any numerical variables")

            # Create a bar graph to get relationship between categorical variable and numerical variable
            st.subheader("Categorical and Numerical Variable Analysis")
            if len(num_columns)!=0 and len(cat_columns)!=0:
                function.categorical_numerical_variable_analysis(df,cat_columns,num_columns)
                
            else:
                st.warning("The dataset does not have any numerical variables. Hence Cannot Perform Categorical and Numerical Variable Analysis")
        
    # DATA PREPROCESSING  
    if selected=='Data Preprocessing':
        # st.header("🛠️ Data Preprocessing")
        revert = st.button("Revert to Original Dataset",key="revert_button")

        if revert:
            st.session_state.new_df = df.copy()

        # REMOVING UNWANTED COLUMNS
        st.subheader("Remove Unwanted Columns")
        columns_to_remove = st.multiselect(label='Select Columns to Remove',options=st.session_state.new_df.columns)

        if st.button("Remove Selected Columns"):
            if columns_to_remove:
                st.session_state.new_df = preprocessing_function.remove_selected_columns(st.session_state.new_df,columns_to_remove)
                st.success("Selected Columns Removed Sucessfully")
                
        st.dataframe(st.session_state.new_df)
       

       # Handle missing values in the dataset
        st.subheader("Handle Missing Data")
        missing_count = st.session_state.new_df.isnull().sum()

        if missing_count.any():

            selected_missing_option = st.selectbox(
                "Select how to handle missing data:",
                ["Remove Rows in Selected Columns", "Fill Missing Data in Selected Columns (Numerical Only)"]
            )

            if selected_missing_option == "Remove Rows in Selected Columns":
                columns_to_remove_missing = st.multiselect("Select columns to remove rows with missing data", options=st.session_state.new_df.columns)
                if st.button("Remove Rows with Missing Data"):
                    st.session_state.new_df = preprocessing_function.remove_rows_with_missing_data(st.session_state.new_df, columns_to_remove_missing)
                    st.success("Rows with missing data removed successfully.")

            elif selected_missing_option == "Fill Missing Data in Selected Columns (Numerical Only)":
                numerical_columns_to_fill = st.multiselect("Select numerical columns to fill missing data", options=st.session_state.new_df.select_dtypes(include=['number']).columns)
                fill_method = st.selectbox("Select fill method:", ["mean", "median", "mode"])
                if st.button("Fill Missing Data"):
                    if numerical_columns_to_fill:
                        st.session_state.new_df = preprocessing_function.fill_missing_data(st.session_state.new_df, numerical_columns_to_fill, fill_method)
                        st.success(f"Missing data in numerical columns filled with {fill_method} successfully.")

                    else:
                        st.warning("Please select a column to fill in the missing data")

            function.display_missing_values(st.session_state.new_df)

        else:
            st.info("The dataset does not contain any missing values")

        encoding_tooltip = '''**One-Hot encoding** converts categories into binary values (0 or 1). It's like creating checkboxes for each category. This makes it possible for computers to work with categorical data.
        **Label encoding** assigns unique numbers to categories. It's like giving each category a name (e.g., Red, Green, Blue becomes 1, 2, 3). This helps computers understand and work with categories.
        '''   
        st.subheader("Encode Categorical Data")

        new_df_categorical_columns = st.session_state.new_df.select_dtypes(include=['object']).columns

        if not new_df_categorical_columns.empty:
            select_categorical_columns = st.multiselect("Select Columns to perform encoding",new_df_categorical_columns)

            #choose the encoding method
            encoding_method = st.selectbox("Select Encoding Method:",['One Hot Encoding','Label Encoding'],help=encoding_tooltip)
    

            if st.button("Apply Encoding"):
                if encoding_method=="One Hot Encoding":
                    st.session_state.new_df = preprocessing_function.one_hot_encode(st.session_state.new_df,select_categorical_columns)
                    st.success("One-Hot Encoding Applied Sucessfully")

                if encoding_method=="Label Encoding":
                    st.session_state.new_df = preprocessing_function.label_encode(st.session_state.new_df,select_categorical_columns)
                    st.success("Label Encoding Applied Sucessfully")


            st.dataframe(st.session_state.new_df)
        else:
            st.info("The dataset does not contain any categorical columns")

        feature_scaling_tooltip='''**Standardization** scales your data to have a mean of 0 and a standard deviation of 1. It helps in comparing variables with different units. Think of it like making all values fit on the same measurement scale.
        **Min-Max scaling** transforms your data to fall between 0 and 1. It's like squeezing data into a specific range. This makes it easier to compare data points that vary widely.'''


        st.subheader("Feature Scaling")
        new_df_numerical_columns = st.session_state.new_df.select_dtypes(include=['number']).columns
        selected_columns = st.multiselect("Select Numerical Columns to Scale", new_df_numerical_columns)

        scaling_method = st.selectbox("Select Scaling Method:", ['Standardization', 'Min-Max Scaling'],help=feature_scaling_tooltip)

        if st.button("Apply Scaling"):
            if selected_columns:
                if scaling_method == "Standardization":
                    st.session_state.new_df = preprocessing_function.standard_scale(st.session_state.new_df, selected_columns)
                    st.success("Standardization Applied Successfully.")
                elif scaling_method == "Min-Max Scaling":
                    st.session_state.new_df = preprocessing_function.min_max_scale(st.session_state.new_df, selected_columns)
                    st.success("Min-Max Scaling Applied Successfully.")
            else:
                st.warning("Please select numerical columns to scale.")

        st.dataframe(st.session_state.new_df)

        st.subheader("Identify and Handle Outliers")

        
        # Select numeric column for handling outliers
        


        selected_numeric_column = st.selectbox("Select Numeric Column for Outlier Handling:", new_df_numerical_columns)
        st.write(selected_numeric_column)

        
        # Display outliers in a box plot
        fig, ax = plt.subplots()
        ax = sns.boxplot(data=st.session_state.new_df, x=selected_numeric_column)
        st.pyplot(fig)


        outliers = preprocessing_function.detect_outliers_zscore(st.session_state.new_df, selected_numeric_column)
        if outliers:
            st.warning("Detected Outliers:")
            st.write(outliers)
        else:
            st.info("No outliers detected using IQR.")


        # Choose handling method
        outlier_handling_method = st.selectbox("Select Outlier Handling Method:", ["Remove Outliers", "Transform Outliers"])

        # Perform outlier handling based on the method chosen
        if st.button("Apply Outlier Handling"):
            if outlier_handling_method == "Remove Outliers":
               
                st.session_state.new_df = preprocessing_function.remove_outliers(st.session_state.new_df, selected_numeric_column,outliers)
                st.success("Outliers removed successfully.")

            elif outlier_handling_method == "Transform Outliers":
                # Provide options for transforming outliers (e.g., capping, log transformation)
                # Update st.session_state.new_df after transforming outliers
                st.session_state.new_df = preprocessing_function.transform_outliers(st.session_state.new_df, selected_numeric_column,outliers)
                st.success("Outliers transformed successfully.")

        # Show the updated dataset
        st.dataframe(st.session_state.new_df)
        
        if st.session_state.new_df is not None:
            # Convert the DataFrame to CSV
            csv = st.session_state.new_df.to_csv(index=False)
            # Encode as base64
            b64 = base64.b64encode(csv.encode()).decode()
            # Create a download link
            href = f'data:file/csv;base64,{b64}'
            # Display a download button
            st.markdown(f'<a href="{href}" download="preprocessed_data.csv"><button>Download Preprocessed Data</button></a>', unsafe_allow_html=True)
        else:
            st.warning("No preprocessed data available to download.")
    
    if selected == 'AI Analysis':
        st.header("AI-Driven Data Analysis")
        st.markdown("### Unleash the power of AI to extract insights from your dataset!")

        if df is None:
            st.warning("Please upload a dataset or select the example dataset to proceed with AI Analysis.")
        else:
            ai_tab1, ai_tab2, ai_tab3 = st.tabs(["🎯 Feature Importance", "🔗 Clustering Analysis", "📈 Target Prediction"])

            with ai_tab1:
                st.subheader("Feature Importance")
                st.markdown("Using Random Forest to identify the most important features in your dataset.")
                target_column = st.selectbox("Select the target column:", df.columns)

                if target_column:
                    from sklearn.ensemble import RandomForestClassifier
                    from sklearn.model_selection import train_test_split

                    y = df[target_column]
                    X = df.drop(columns=[target_column])
                    X = X.select_dtypes(include=['number']).fillna(0)

                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
                    rf = RandomForestClassifier(random_state=42)
                    rf.fit(X_train, y_train)

                    feature_importances = rf.feature_importances_
                    importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': feature_importances})
                    importance_df = importance_df.sort_values(by='Importance', ascending=False)

                    st.dataframe(importance_df)
                    st.bar_chart(importance_df.set_index('Feature'))

            with ai_tab2:
                st.subheader("Clustering Analysis")
                st.markdown("Using K-Means clustering to group data into meaningful clusters.")
                from sklearn.cluster import KMeans
                from sklearn.decomposition import PCA

                num_clusters = st.slider("Select the number of clusters:", 2, 10, 3)
                cluster_data = X.select_dtypes(include=['number'])
                kmeans = KMeans(n_clusters=num_clusters, random_state=42)
                cluster_labels = kmeans.fit_predict(cluster_data)

                df['Cluster'] = cluster_labels

                pca = PCA(n_components=2)
                pca_data = pca.fit_transform(cluster_data)

                cluster_df = pd.DataFrame(pca_data, columns=['PCA1', 'PCA2'])
                cluster_df['Cluster'] = cluster_labels
                import plotly.express as px
                fig = px.scatter(cluster_df, x='PCA1', y='PCA2', color=cluster_df['Cluster'].astype(str))
                st.plotly_chart(fig)

            with ai_tab3:
                st.subheader("Target Prediction")
                st.markdown("Train a Logistic Regression model to predict the target variable.")
                from sklearn.linear_model import LogisticRegression
                from sklearn.metrics import classification_report

                lr = LogisticRegression(max_iter=1000)
                lr.fit(X_train, y_train)
                y_pred = lr.predict(X_test)

                st.markdown("#### Classification Report")
                report = classification_report(y_test, y_pred, output_dict=True)
                st.dataframe(pd.DataFrame(report).transpose())