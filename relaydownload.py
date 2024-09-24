import streamlit as st
import requests
from urllib.parse import urlparse, unquote

# Function to download file in chunks from URL
def download_file(url):
    try:
        # Streaming the download to avoid loading large files into memory all at once
        with requests.get(url, stream=True) as response:
            response.raise_for_status()  # Check if the request was successful

            # Attempt to get the filename from the 'Content-Disposition' header
            if 'Content-Disposition' in response.headers:
                content_disposition = response.headers['Content-Disposition']
                file_name = content_disposition.split('filename=')[1].strip('"')
            else:
                # Fallback: Extract the filename from the URL
                parsed_url = urlparse(url)
                file_name = unquote(parsed_url.path.split('/')[-1])  # Get the last part of the URL path as filename

            # Download the file in chunks
            file_content = b""
            for chunk in response.iter_content(chunk_size=8192):  # 8 KB per chunk
                if chunk:
                    file_content += chunk  # Accumulate file content

            return file_content, file_name
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
