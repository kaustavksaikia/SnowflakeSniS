# Import python packages
import streamlit as st
import requests as req
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize Your Smoothie")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

cnx = st.connection("snowflake")
session = cnx.session()


my_dataframe = session.table(
    "smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
# st.dataframe(data=my_dataframe, use_container_width=True)

order_name = st.text_input('Name on Smoothie')
st.write('The Name on Your Smoothie will be:', order_name)

ingredients = st.multiselect(
        "Choose up to 5 ingredients:",
        my_dataframe
)

ingredients_string = ''


if ingredients:
    for each_val in ingredients:
        ingredients_string +=each_val
        ingredients_string +=' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == each_val, 'SEARCH_ON'].iloc[0]
        smoothiefroot_response = req.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        st.subheader(each_val + 'Nutritional Information')
        smoothie_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    insert_statement = """INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                                values ('""" + ingredients_string + """', '""" + order_name + """')"""
        

    insert_but = st.button('Submit Order')
    if insert_but:
        session.sql(insert_statement).collect()
        st.success('Your Smoothie is ordered!', icon='✅')