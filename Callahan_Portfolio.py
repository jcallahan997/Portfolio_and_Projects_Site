import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
# from st_pages import Page, show_pages, add_page_title
st.set_page_config( page_title="Callahan Portfolio", )
st.title("Welcome to my portfolio!")

st.write("Hi, I'm James. I work as a data scientist and am passionate about\
          the field. In my free time, I like to work out, travel, and latin dance! Working on cars\
         and reading are some other things that bring me joy.")
#add pic of myself here
st.image("IMG_5550.jpeg", caption="A picture of me on a trip to Sri Lanka.")
# present resume and a download button for it here

pdf_viewer("Callahan_James_Resume (v5.4) copy.pdf")

with open('Callahan_James_Resume (v5.4) copy.pdf', 'rb') as f:
   st.download_button('Download resume as .pdf', f, file_name='Callahan_James_Resume.pdf')

st.write("Go to my LinkedIn: https://www.linkedin.com/in/jamesacallahan/")
st.write("Check out my GitHub: https://github.com/jcallahan997")
st.write("Thank you for visiting my page!")