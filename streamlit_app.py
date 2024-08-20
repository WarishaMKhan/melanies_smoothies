import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# Text input for the name on the order
title = st.text_input("Name on Order", "Aasir")
st.write("The name on your smoothie will be", title)

# Initialize Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Multi-select input for ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients: ', my_dataframe)

# Button to submit the order
time_to_insert = st.button('Submit Order')

if time_to_insert and ingredients_list:
    # Prepare the ingredients string
    ingredients_string = ' '.join(ingredients_list)
    
    # Correct SQL statement with the proper variable name
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                         VALUES ('{ingredients_string}', '{title}')"""
    
    st.write(my_insert_stmt)
    
    # Execute the SQL statement
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
    st.stop()
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
