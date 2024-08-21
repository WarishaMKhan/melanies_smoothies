import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# Text input for the name on the order
title = st.text_input("Name on Order", "Aasir")
st.write("The name on your smoothie will be", title)

# Initialize Snowflake session
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON')).to_pandas()

# Display dataframe in the app for reference (optional)
st.dataframe(my_dataframe, use_container_width=True)

# Multi-select input for ingredients
fruit_names = my_dataframe['FRUIT_NAME'].tolist()
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_names,
    max_selections=5
)

# Button to submit the order
time_to_insert = st.button('Submit Order')

if time_to_insert and ingredients_list:
    # Prepare the ingredients string
    ingredients_string = ' '.join(ingredients_list)

    for fruit_chosen in ingredients_list:
        search_on = my_dataframe.loc[my_dataframe['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].values[0]
        st.write(f'The search value for {fruit_chosen} is {search_on}.')

        # Fetch nutrition information
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
        
        if fruityvice_response.status_code == 200:
            fv_data = fruityvice_response.json()
            fv_df = pd.DataFrame([fv_data])
            st.subheader(f'{fruit_chosen} Nutrition Information')
            st.dataframe(fv_df)
        else:
            st.error(f"Could not retrieve data for {fruit_chosen}")

    # Correct SQL statement with the proper variable name
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                         VALUES ('{ingredients_string}', '{title}')"""
    
    st.write(my_insert_stmt)
    
    # Execute the SQL statement
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
