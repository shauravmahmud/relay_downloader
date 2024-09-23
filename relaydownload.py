import streamlit as st
import requests

# Function to download file from URL
def download_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.content, response.headers['Content-Disposition'].split('filename=')[1]
    except Exception as e:
        st.error(f"Error downloading file: {e}")
        return None, None

# Streamlit app interface
st.title("File Downloader")

# Input field for the file download link
url = st.text_input("Enter the file URL:")

if url:
    file_content, file_name = download_file(url)
    
    if file_content and file_name:
        st.success(f"File '{file_name}' downloaded successfully!")
        
        # Provide a download button
        st.download_button(
            label="Download File",
            data=file_content,
            file_name=file_name,
            mime="application/octet-stream"
        )
    else:
        st.warning("Unable to fetch the file. Please check the URL.")

