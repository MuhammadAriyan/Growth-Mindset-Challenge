# imports
import os 
from io import BytesIO
import streamlit as st
import pandas as pd

# set up of my app
st.set_page_config(page_title='Data Sweeper', layout='wide')

# Mark down
st.markdown("""
    <link rel="stylesheet" 
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL,GRAD@400,0,0" />
""", unsafe_allow_html=True)


st.markdown(""" <h1 style="display: flex; align-items: center; gap: 10px;">
            <span class="material-symbols-outlined" style="font-size:50px;"></span> Data Sweeper</h1>"""
            , unsafe_allow_html=True)

st.write('Transform your files between CSV and Excel formats with built-in data cleaning and visualization')

# file uploader
upload_files = st.file_uploader(
    'Upload your files (CSV or Excel):' , 
      type=['csv','xlsx'],
      accept_multiple_files=True
      )

# if files are true run a loop
if upload_files:
    for file in upload_files:
        # gets extension
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # checks for extension
        
        # if extension is .csv
        if file_ext == ".csv":
            # then the dataframe will be
            df = pd.read_csv(file)
            
        # if extension is .xlsx
        elif file_ext == ".xlsx":
            # then the dataframe will be
            df = pd.read_excel(file)
            
        #  if extension is not .cv or .xlsx ( "basically an unsupported file" )
        else: 
            #  then throw an error of 'Unsupported file type : {file_ext e.g png jpeg pdf}'
            st.error(f"Unsupported file type: {file_ext}")
            # then continue ( this continue means the loop continues toward the next file)
            continue
        
        
        # file info
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024} MB")
        
        # show 5 rows of our df
        st.write("Preview the head of Dataframe")
        # head from pd returns 5 rows from the top
        st.dataframe(df.head())
        
        st.subheader('Data Cleaning Options')
        if st.checkbox(f"Clean Data for {file.name}"):
            
            # makes 2 columns in UI
            col1,col2 = st.columns(2)
            
            with col1:   # Using "with" ensures everything inside this block belongs to col1
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=(True))
                    st.write("Duplicates removed")
                    #  then automatically closes it
                    
            with col2:   # Using "with" ensures everything inside this block belongs to col2
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns # select numeric cols only
                    df[numeric_cols]= df[numeric_cols].fillna(df[numeric_cols].mean()) # Replace missing values (NaN) in all numeric columns with their respective column mean
                    st.write("missing values have been filled")
                    #  then automatically closes it
                    
        # choose specific columns to keep or convert
        st.subheader("Select columns to convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns ) # choose the cols from drop down and chooses all columns by default 
        df = df[columns]
        
        # create a visualization
        st.markdown(""" <h2 style=`display: flex; align-items: center; gap: 10px;">
            <span class="material-symbols-outlined"></span> Data Visulization</h2>"""
            , unsafe_allow_html=True)
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
            
        # conversion option
        st.markdown(""" <h2 style=`display: flex; align-items: center; gap: 10px;">
            <span class="material-symbols-outlined"></span>Conversion Options</h2>"""
            , unsafe_allow_html=True)
        
        conversion_type = st.radio(f"Convert {file.name} to:",["CSV","EXCEL"],key=file.name)
        
        # This line creates an in-memory buffer using BytesIO
        buffer = BytesIO() # Think of it as a temporary file that exists in RAM instead of on disk.
        if conversion_type == "CSV":
            df.to_csv(buffer,index=False)
            file_name = file.name.replace(file_ext,".csv") # replace the extension
            mime_type= "text/csv" # MIME type of the file, used to identify its format (e.g., 'image/png', 'application/pdf')
            
        elif conversion_type == "EXCEL":
            df.to_excel(buffer,index=False, engine="openpyxl")
            file_name = file.name.replace(file_ext,".xlsx") # replace the extension
            mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" # MIME type of the file, used to identify its format (e.g., 'image/png', 'application/pdf')
            
        buffer.seek(0)

        st.markdown(f"""
        <h2 style="display: flex; align-items: center; gap: 10px;">
        <span class="material-symbols-outlined"></span> Download {file.name} as {conversion_type}
        </h2>
        """, unsafe_allow_html=True)
        
        # download button
        if st.download_button(
        label=f"⬇️ Download {file.name} as {conversion_type}", 
        data=buffer,
        file_name=file_name,
        mime=mime_type
        ):
            st.toast("🎉 Boom! File Downloaded Successfully!", icon="🎇")
            st.balloons()
            
        st.snow()  
