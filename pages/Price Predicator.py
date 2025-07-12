import streamlit as st
import pickle
import pandas as pd
import numpy as np
from joblib import load

st.set_page_config(page_title="Smart Price Estimator", page_icon="🏡")
st.title('page1')
#property_type,sector,bedRoom,bathroom,balcony,agePossession,built_up_area,servant,room,store,room,furnishing_type,luxury_category,floor_category
with open('df.pkl','rb') as file:
    df=pickle.load(file)
pipeline = load('pipeline_comp.joblib')

st.header('Enter your inputs')
# property_type
property_type=st.selectbox('Property Type',['flat','house'])
# sector
sector=st.selectbox('Sector',sorted(df['sector'].unique().tolist()))
# bedRoom
bedRooms=float(st.selectbox('No Of Bedrooms',sorted(df['bedRoom'].unique().tolist())))
# bathrooms
bathrooms=float(st.selectbox('No Of Bathrooms',sorted(df['bathroom'].unique().tolist())))
# balcony
balcony=st.selectbox('Balconies',sorted(df['balcony'].unique().tolist()))
# age Possession
property_age=st.selectbox('Property Age',sorted(df['agePossession'].unique().tolist()))
# built_up_area
built_up_area=float(st.number_input('Built Up Area'))
# servant room
servant_room=float(st.selectbox('Servant Room',['0','1']))
# store room
store_room=float(st.selectbox('Store Room',['1','0']))
# furnishing type
furnishing_type=st.selectbox('Furnishing Type',sorted(df['furnishing_type'].unique().tolist()))
# luxury category
luxury_category=st.selectbox('Luxury Category',sorted(df['luxury_category'].unique().tolist()))
# floor_category
floor_category=st.selectbox('Floor Category',sorted(df['floor_category'].unique().tolist()))
# button
if st.button('Predict'):
    # form a datframe
    data = [[property_type,sector, bedRooms, bathrooms, balcony, property_age, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)
    st.dataframe(one_df)


    # predict

    base_price = np.expm1(pipeline.predict(one_df)[0])  # Undo log1p
    low = base_price - 0.22  # Adjust based on MAE
    high = base_price + 0.22
    # display
    st.text("The price of flat is between {} and {} crores".format(round(low,2),round(high,2)))

