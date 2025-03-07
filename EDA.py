import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore', category= UserWarning, module= 'matplotlib')

# Set seaborn theme
sns.set_theme(style= 'darkgrid')

# Sidebar for Navigation:
st.sidebar.title('Navigation')
page = st.sidebar.radio(
    "Select Page:", ["Welcome", "Univariate Analysis", "Bivariate Analysis", "Multivariate Analysis"], key = 'navigation'
)

# Create the welcome page:
if page == 'Welcome':
    st.title("Wlcome to My EDA Visualiser")
    st.write(
          """
        This application is designed for dynamic data visualization and analysis using your uploaded dataset. It supports:

        - **Univariate Analysis:** Single-variable exploration.
        - **Bivariate Analysis:** Explore relationships between two variables.
        - **Multivariate Analysis:** Advanced insights involving multiple variables.

        ### Features include:
        - Interactive visualizations.
        - Seamless data upload and processing.
        - Advanced plots with custom options.

        Navigate through the sidebar options to begin your journey! 📊
        """
    )
if page != "welcome":
    st.sidebar.title("Upload Your File.")
    uploaded_file = st.sidebar.file_uploader("Upload Here: ", type='csv', key = 'uploader')

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.success("File is uploaded successfully.")
    else:
        st.sidebar.info("Please upload a CSV file to proceed.")
        st.stop()
    
    # define numeric and categorical columns:
    numeric_columns = data.select_dtypes(include= "number").columns.to_list()
    categorical_columns = data.select_dtypes(include= ["category", 'object']).columns.to_list()

    # Helper function to display plots:
    def display_plot(fig):
        st.pyplot(fig)

# Create the Univariate Analysis Page:
if page == 'Univariate Analysis':
    st.title("Univariate Analysis", anchor= False)
    st.header('Explore the Single Variable Trends.')
    st.write('Explore univariate plots with dynamic column selection.')

    # Create a 2 x 2 subplot with increase fig size:
    fig, ax = plt.subplots(2, 2, figsize= (25, 15))

    # Create the histogram:
    st.write('Histogram: ')
    hist_col = st.selectbox("Select a Cloumn for your Histogram.", numeric_columns, key = 'histogram', index=0)
    sns.histplot(data[hist_col], kde = True, ax = ax[0,0])
    ax[0,0].set_title(f"Histogram of {hist_col} Distribution.", fontsize = 30, weight = 'bold', color = 'black')
    ax[0,0].tick_params(axis = 'x', rotation = 90, size = 15)


    # Create the countplot:
    if categorical_columns:
        st.subheader("Count Plot: ")
        count_col = st.selectbox("Select a Column for Count Plot:", categorical_columns, key = "count", index = 0)
        sns.countplot(ax = ax[0,1], data=data, x = count_col)
        ax[0,1].set_title(f"Count Plot of {count_col}", fontsize = 30, color = 'black', weight = 'bold')
        ax[0,1].tick_params(axis = 'x', labelsize = 15, rotation = 90)

    # Create the pie chart:
    if categorical_columns:
        st.subheader('Pie Chart: ')
        pie_col = st.selectbox("Select a Column for Pie Chart:", categorical_columns, key = 'pie', index = 0)
        pie_data = data[pie_col].value_counts().sort_values(ascending=False).head(10)
        pie_data.plot.pie(ax = ax[1,0], textprops= {'fontsize': 30}, autopct= "%1.1f%%")
        ax[1,0].set_title(f"Pie Chart of top 10 Categories in {pie_col}", fontsize = 30, color = 'black', weight = 'bold')
    
    # Create the boxplot:
    if categorical_columns:
        st.subheader("Box Plot: ")
        box_col = st.selectbox("Select a Column for Box Plot:", categorical_columns, key = 'box', index = 0)
        sns.boxplot(data, x = box_col, ax = ax[1,1])
        ax[1,1].set_title(f"Box Plot of {box_col}", fontsize = 30, color = 'black', weight = 'bold')
        ax[1,1].tick_params(axis = 'x', rotation = 90, labelsize = 15)
    
    plt.tight_layout()
    display_plot(fig)

elif page == "Bivariate Analysis":
    st.title("Bivariate Analysis")
    st.header('Explore The Relationship Between Two Viariables.')
    st.write('Bivariate Analysis with dynamic column selection.')

    fig, ax= plt.subplots(2,2, figsize=(25,15))

    # Create the line plot:
    st.subheader("Line Plot: ")
    line_x = st.selectbox("Select variable for X axis:", numeric_columns, key = 'linex', index = 0)
    line_y = st.selectbox("Select variable for Y axis:", numeric_columns, key = 'liney', index = 0)
    sns.lineplot(data, x = line_x, y = line_y, ax = ax[0,0])
    ax[0,0].set_title(f"Line Plot: {line_x} VS {line_y}", fontsize = 30, color = 'black', weight = 'bold')
    ax[0,0].tick_params(axis = 'both', labelsize = 15, color = 'black')

    # Create the Scatter Plot:
    st.subheader("Scatter Plot: ")
    scatter_x = st.selectbox("Select X axis variable:", numeric_columns, key = 'scatterx', index = 0)
    scatter_y = st.selectbox("Select Y axis variable:", numeric_columns, key = 'scattery', index = 0)
    sns.scatterplot(data, x = scatter_x, y = scatter_y, ax = ax[0,1])
    ax[0,1].set_title(f"Scatter Plot: {scatter_x} VS {scatter_y}", fontsize = 30, color = 'black', weight = 'bold')
    ax[0,1].tick_params(axis = 'both', labelsize = 15, color = 'black')

    # Create the Bar Plot:
    if categorical_columns:
        st.subheader("Bar Plot: ")
        barx = st.selectbox("Select X axis variable:", categorical_columns, key = 'barx', index = 0)
        bary = st.selectbox("Select Y axis variable:", numeric_columns, key = 'bary', index = 0)
        sns.barplot(data, x = barx, y = bary, ax = ax[1,0])
        ax[1,0].set_title(f"Bar Plot: {barx} VS {bary}", fontsize = 30, color = 'black', weight = 'bold')
        ax[1,0].tick_params(axis = 'both', labelsize = 15, color = 'black')

    # Create the box plot:
    if categorical_columns:
        st.subheader("Box Plot: ")
        box_x = st.selectbox("Select X axis variable:", categorical_columns, key = 'box_x', index = 0)
        box_y = st.selectbox("Select Y axis variable:", numeric_columns, key = 'box_y', index = 0)
        sns.boxplot(data = data, x = box_x, y = box_y, ax = ax[1,1])
        ax[1,1].set_title(f"Box Plot: {box_x} VS {box_y}", fontsize = 30, color = 'black', weight = 'bold')
        ax[1,1].tick_params(axis = 'both', labelsize = 15, color = 'black')

    plt.tight_layout()
    display_plot(fig)

# mulivariate Analysis:
elif page == 'Multivariate Analysis':
    st.title("Multivariate Analysis")
    st.header("Explore the Relationships Between Multiple Variables.")
    st.write("Generate Pair Plot and HeatMap for multivariate analysis.")

    st.subheader('Pair Plot: ')
    if numeric_columns:
        pairplot_col = st.multiselect("Select columns for Pair Plot: ", numeric_columns, default=numeric_columns[:min(3, len(numeric_columns))])
        if pairplot_col:
            pair_fig = sns.pairplot(data[pairplot_col])
            display_plot(pair_fig)
        else:
            st.warning("Please select at least one column for Pair Plot.")
    else:
        st.error("No numeric columns found.")
    
    st.subheader("Heatmap")
    if numeric_columns:
        fig, ax = plt.subplots(figsize = (40,30))
        sns.heatmap(data[numeric_columns].corr(), ax = ax, annot = True, annot_kws={'size': 30})
        ax.set_title("Correlation Heatmap", fontsize = 30, weight = 'bold')
        ax.tick_params(axis = 'both', labelsize = 15)
        display_plot(fig)
    else:
        st.error("No Numerical columns to display Heatmap.")