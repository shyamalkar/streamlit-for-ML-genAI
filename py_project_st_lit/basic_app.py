import streamlit as st 

st.title("Python project basic app")
st.write("This is my new app")
button1 = st.button('Click me')

if button1: 
    st.write("This is some text.")

like = st.checkbox("Do you liek this app ?")

button2 = st.button("Submit")

if button2: 

    if like: 
        st.write("Thanks, i like it too.")

    else:
        st.write("I am so sorry, you have bad tastes.")

st.header("Start of the radio button section")

animal = st.radio("What animal is your fevoraite ?", ("Lion", "Tigger", "Bear"))

button3 = st.button
("Submit Animal")

if button3:
    st.write(animal)
    if animal == "Lion":
        st.write("Roar!")





st.header("Start of the Multiselect section")

options = st.multiselect("What animals do you like ? ", ['Lion', 'Tiger', 'Bear'])

button5 = st.button("Print Animals")

if button5:
    st.write(options)


st.header("Start of the slider section")

epochs_num = st.slider("How many epochs ?", 1,100,10)

if st.button("Slider button"):
    st.write(epochs_num)


st.header("start of the text input section")

user_text = st.text_input("Wat is your fevoraite movie ?", "Star wars Ep. 4")

if st.button("Text Button"):
    st.write(user_text)



user_num = st.number_input("What is your fevoraite number ?")

if st.button("Number Button"):
    st.write(user_num)


def run_sentiment_analysis(txt):
    st.write(f"Ananlysis Done.{txt}")

txt = st.text_area(
    "Text to analyze",
    """It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair""",
)
st.write("Sentiment:", run_sentiment_analysis(txt))
