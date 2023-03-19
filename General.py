import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Exploratory Data Analysis on Streamlit",
    layout="wide"
)

st.title("Exloratory Data Analysis on Streamlit")

# Load the data using a file imported by the user
uploaded_file = st.file_uploader("Choose a CSV file:")

#Show raw data - dataframe
if uploaded_file:
    #Load dataframe
    df = pd.read_csv(uploaded_file)

    
    ########## First step - see raw data ##########
    # Show an amount of rows and columns
    st.header("1) Show raw data:")
    n_rows, ncols=df.shape
    st.write("Your data has ", n_rows, " rows and ", ncols, " columns")
    amount_rows_show = st.slider("How many rows would you like to see?", 0, df.shape[0], 5)
    columns_df = st.multiselect('Select which columns would you like to see:', options=df.columns, default=list(df.columns[0:11]))
    st.write("Raw data:")
    st.dataframe(df.head(amount_rows_show)[columns_df])

    #Descriptive statistics
    st.write("Descriptive statistics: central tendency, dispersion and shape of a dataset’s distribution, excluding Not a Number (NaN) values:")
    st.dataframe(df.describe())


    ########## Second step - data preparation ##########

    #Drop unnecessary columns
    st.header("2) Data preparation:")
    columns_to_process = st.multiselect('Select which columns would you like to keep. The others will be deleted', options=df.columns)
    new_df=df[columns_to_process].copy()
    st.dataframe(new_df)
    

    ########## Third step - remove NaN and missing values ##########

    #Shows NaN and missing values by columns
    st.header("3) Remove NaN and missing values:")
    st.write("Amount of null and missing values by columns:", new_df.isna().sum())
    if sum(new_df.isna().sum())>0: # Shows checkbox only if there is at least one NaN and missing value
     remove_nan_miss = st.checkbox('Remove NaN and missing rows?')   
     if remove_nan_miss: # Checkbox for NaN and missing values
       new_df=new_df.dropna() # Drop rows
       new_df=new_df.reset_index(drop=True) # Reset index after drop the rows
       st.write("Amount of null and missing values by columns:", new_df.isna().sum())


    ########## Fourth step - plot the data ##########

    #Plot a histogram of the first column
    st.header("4) Plot the data:")
    if columns_to_process: #In case there is at least a column selected
        plot_type = st.radio("Display a bar chart, line chart or histogram?", ("Bar chart", "Line chart", "Histogram"))
        if plot_type=="Bar chart": # Plot a bar chart
           column_to_plot = st.selectbox('Select the column for the plot:', columns_to_process) 
           st.bar_chart(new_df[column_to_plot].value_counts())
        elif plot_type=="Line chart": # Plot a line chart
            x_to_plot = st.selectbox('Select the column for the x plot:', columns_to_process)
            y_to_plot = st.selectbox('Select the column for the y plot:', columns_to_process)
            st.line_chart(new_df, x=x_to_plot, y=y_to_plot)
        else:
            column_to_plot = st.selectbox('Select the column for the plot:', columns_to_process)
            fig, ax= plt.subplots(figsize=(9, 3))
            n_bins = st.slider('Select the number of bins:', 1, int(new_df[column_to_plot].mean()/3), int(new_df[column_to_plot].mean()/9))
            plot_kde = st.checkbox('Plot the Kernel Density Estimate (KDE)?')   
            sns.histplot(data=new_df, x=column_to_plot, binwidth=n_bins, alpha=0.6, kde = plot_kde)
            st.pyplot(fig)

            
    ########## Fifth step - show correlations ##########

    #Show correlations among the variables
    st.header("5) Pairwise correlations among the columns:")
    if columns_to_process:
        df_corr=df[columns_to_process].corr()
        fig2, ax2= plt.subplots(figsize=(6, 2))
        sns.heatmap(df_corr, ax=ax2, annot=True)
        st.pyplot(fig2)
               
    
    
