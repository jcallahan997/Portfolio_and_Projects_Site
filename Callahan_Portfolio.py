import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
st.set_page_config( page_title="My Page Title", )
st.title("Welcome to my portfolio!")

st.write("Hi, I'm James. I work as a data scientist and am passionate about the field. In my free time, I like to boulder, travel, and dance!")
#add pic of myself here
st.image("IMG_5550.jpeg", caption="A picture of me on a recent trip I took with a friend to Sri Lanka.")
# present resume and a download button for it here

pdf_viewer("Callahan_James_Resume(v1.0).pdf")

with open('Callahan_James_Resume(v1.0).docx', 'rb') as f:
   st.download_button('Download resume as .docx', f, file_name='Callahan_James_Resume.docx')

st.write("Check out my GitHub: https://github.com/jcallahan997")
st.write("Thank you for visiting my page!")