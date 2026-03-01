import streamlit as st

st.title("Hello Streamliter 👋")
st.markdown(
    """
    # Introduction
    This is a playground for you to try Streamlit and have fun. 

    **There's :rainbow[so much] you can build!**
    
    We prepared a few examples for you to get started. With Streamlit, you can build:
    * App 1
    * App 2
    * App 3
    """
)

if st.button("Send balloons!"):
    st.balloons()