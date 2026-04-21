import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Hello , Mr Uesr")
st.subheader("Wellcome to language selection")
st.text("Which is ur fav language ")
st.write("Select one ")

language = st.selectbox("Your Fav Language is : ",["HTML","JAVA", "PYTHON","PHP","JAVASCRIPT"])

st.write(f'tou favorate lanhuage is {language}. Thankyou ')

st.success("Thanks for chooseing")


st.title("☕ Chai Streamlit Dashboard")


data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "Sales": [15000, 18000, 12000, 22000, 25000],
}


df = pd.DataFrame(data)
st.dataframe(df)

st.subheader("Monthly sales")

fig,ax  = plt.subplots()
ax.plot(df["Month"], df["Sales"], marker =  'o', color = "g")
st.pyplot(fig)  


st.title("Stramlit")
st.markdown("""Wellcome
            
**Hello Every one i am :rainbow[Avinash]**
""")

if st.button("Send ballon"):
    st.balloons()
    st.success("look the Ballons")

if st.button("Snow"):
    st.snow()
    st.success("look the snow")

tc = st.checkbox("Terms and condition")

if tc :
    st.write("Thanks")

fav = st.radio("Tour favourate color is : ",["RED", "Pink", "Balck", "Blue"])

if fav:
    st.write(f"Nice to herar that ur fav color is {fav}") 

volume =  st.slider("vaolum", 0,10,5 )
st.write(f"Current volume is {volume}") 

amount =  st.number_input("Tell the amount : ", min_value= 1, max_value= 10, step=1)
st.write(f"Amount taken  : {amount}")

name =  st.text_input("Enter Your name : ")
if name:
    st.write(f"Wellcome  : {name}")

dao =   st.date_input("Choose the order date")

st.write(f"Your order date is {dao}")




all_user = ["Avinash", "Avi", "Roshni", "Ankita"]
with st.container(border=  True):
    users =  st.multiselect("User", all_user)
    rolling_average  =  st.toggle("Rolling Average ")



fixed_data = {
    "Avinash": [5, 6, 7, 8, 7, 6, 5, 8, 9, 10, 9, 8, 7, 6, 5, 4, 5, 6, 7, 8],
    "Avi":   [3, 4, 5, 5, 6, 7, 6, 5, 7, 8, 7, 6, 5, 4, 3, 4, 5, 5, 6, 7],
    "Roshni":[2, 3, 4, 4, 5, 6, 5, 4, 5, 6, 6, 5, 4, 3, 2, 3, 4, 5, 5, 6],
    "Ankita":[2, 2, 4, 5, 5, 6, 5, 2, 5, 6, 4, 5, 6, 3, 5, 6, 4, 5, 4, 6]
}


data =  pd.DataFrame(fixed_data)[users]


if rolling_average:
    data  = data.rolling(7).mean().dropna()

t1 ,t2 = st.tabs(["Chart", "DataFrame"])
t1.line_chart(data , height=250)
t2.dataframe(data ,  height=250 , use_container_width=True)


st.warning("⚠️ Please select at least one user to display data.")


st.title("Vote ")

col1,col2 = st.columns(2)

with col1:
    st.header("Cold Coffee")
    st.image("https://cdn.uengage.io/uploads/18085/image-877948-1717587970.jpeg", width = 200)
    votte1 = st.button("Vote cold Cofee")
with col2:
    st.header("Hot Coffee")
    st.image("https://www.acouplecooks.com/wp-content/uploads/2021/09/Almond-Milk-Coffee-001.jpg", width = 200)
    votte2 = st.button("Vote hot coffee")

if votte1 :
    st.success("Thanks For voting Cold Coffee")
elif votte2:
    st.success("Thanks fro voting the Hot Coffee")

name = st.sidebar.text_input("Enter Your name :")
if name:
    st.sidebar.write(f"Wellcome {name}")

with st.expander("Show the Procees of Making Maggie"):
    st.write("""
1. Tear the Maggie
2. Put it into the hot water.
3. Add masala
4. Wait for few min
5. Maggie is ready


""")
    
st.markdown('### Wellcome Friend')
st.markdown('> Bookmark')


file = st.file_uploader("Upload Your CSV file",  type=["csv"])
if file:
    df = pd.read_csv(file)
    st.subheader("Data Preview")
    st.dataframe(df)

if file:
    st.subheader("Summary  Stats")
    st.write(df.describe())


if file  :
    cites = df["City"].unique()
    selected_city = st.selectbox("Filter by sities" , cites)
    filter_city = df[df["City"] == selected_city]
    st.dataframe(filter_city)