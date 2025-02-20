# imports
import os 
from io import BytesIO
import streamlit as st
import pandas as pd
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

# set up of my app
st.set_page_config(page_title='Data Sweeper', layout='wide')

data = {
    "Name":['luffy','cr7','claudie'],
    "Age":[17,None,56]
}

df0 = pd.DataFrame(data)
csv = df0.to_csv(index=False)
# Mark down
st.title('Data Sweeper ❄')
st.subheader('Want a dummy file? ✨') 
st.download_button(
    label='Download 🍃',
    data=csv,
    file_name='people.csv',
    mime='text/csv'
)
st.write('Transform your files between CSV and Excel formats with built-in data cleaning and visualization 🍁')

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
        st.subheader('Data Visulization 📉')
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
        
        st.subheader('Generate a summary 🍂')
        
        if st.button(f'Generate summary about {file.name}'):
            api_key = os.getenv('api_key')
            model = 'mistral-large-latest'
            
            client = Mistral(api_key=api_key)
            
            chat_response = client.chat.complete(
                model=model,
                messages= [
                    {
                        "role":'user',
                        "content": f"Give a fun yet professional summary of '{file.name}' in 4-5 lines. Keep it simple, avoid fancy words, and make it engaging with emojis. Use bullet points to highlight key stats. No bold text, just keep it clean and easy to read. Here’s the data: {df}"
  }
                ]
            )
            
            st.text(chat_response.choices[0].message.content)
        # conversion option
        st.subheader('Conversion Options 🔃')
        
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

        st.subheader(f"Download {file.name} as {conversion_type} 🌊")
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
