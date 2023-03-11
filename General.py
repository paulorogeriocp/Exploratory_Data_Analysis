import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Exploratory Data Analysis on Streamlit")

# Load the data using a file imported by the user
uploaded_file = st.file_uploader("Choose a CSV file:")

#Show raw data - dataframe
if uploaded_file:
    #Load dataframe
    df = pd.read_csv(uploaded_file)

    
    #First step - see raw data#
    # Show an amount of rows and columns
    st.header("Show raw data:")
    n_rows, ncols=df.shape
    st.write("Your data has ", n_rows, " rows and ", ncols, " columns")
    amount_rows_show = st.slider("How many rows would you like to see?", 0, df.shape[0], 5)
    columns_df = st.multiselect('Select which columns would you like to see:', options=df.columns, default=list(df.columns[0:5]))
    st.write("Raw data:")
    st.dataframe(df.head(amount_rows_show)[columns_df])

    #Descriptive statistics
    st.write("Descriptive statistics: central tendency, dispersion and shape of a dataset’s distribution, excluding NaN values:")
    st.dataframe(df.describe())


    #Second step - data preparation#

    #Drop unnecessary columns
    columns_to_process = st.multiselect('Select which columns would you like to keep. The others will be deleted', options=df.columns)
    new_df=df[columns_to_process].copy()
    st.dataframe(new_df)

    #To do
    #Remove NaN and missing values


    #Third step - plot the data#

    #Plot a histogram of the first column
    if columns_to_process: #In case there is at least a column selected
        #val_count  = new_df[columns_to_process[0]].value_counts()
        #fig = plt.figure(figsize=(10,5))
        #sns.barplot(x=val_count.index, y=val_count.values, alpha=0.8)
        #st.pyplot(fig)
        df1 = new_df[columns_to_process[0]].value_counts().rename_axis('unique_values').reset_index(name='counts')
        st.bar_chart(df1)
    
    
