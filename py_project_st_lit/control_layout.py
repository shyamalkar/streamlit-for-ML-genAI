import streamlit as st 

def clean_txt(txt):
    text = text.replace("`","").replace("\n", "".replace("&&***&&", "\n\n").strip())

    return(text)

st.title("Lesson 01.02: Intro to Layouts and Images")

st.sidebar.image("/Users/shyamalkar/Desktop/Python_project/py_project_st_lit/Screenshot 2026-09-22 at 8.53.42 PM.png", width=1000000)

st.sidebar.header("Options")
text = st.sidebar.text_area("paste Text Here")

button1 = st.sidebar.button("Clean Text")

