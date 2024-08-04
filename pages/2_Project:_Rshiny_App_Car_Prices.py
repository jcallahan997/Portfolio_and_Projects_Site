import streamlit as st
import streamlit.components.v1 as components
st.header("An Rshiny app presented here through an iframe. The app itself is hosted on Shinyapps, and explores the relationship between car prices and mileage")
components.iframe("https://fxyqh7-james-callahan.shinyapps.io/car_shinyapp/", height=1950)
st.write(" ")