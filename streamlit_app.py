# Import python packages
import streamlit as st
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
    "smoothies.public.fruit_options").select(col('FRUIT_NAME'))

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

    insert_statement = """INSERT INTO smoothies.public.orders(ingredients, name_on_order)
                                values ('""" + ingredients_string + """', '""" + order_name + """')"""
        
    # st.write(insert_statement)
    insert_but = st.button('Submit Order')
    if insert_but:
        session.sql(insert_statement).collect()
        st.success('Your Smoothie is ordered!', icon='✅')