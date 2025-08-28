# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col  

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom smoothie!
  """
)


name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)
  

#------------Usamos la sesion disposible y tomamos el data_frame (datos especficos de una tabla)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

#------------Multiselect
ingredients_list = st.multiselect (
    'Choose up 5 ingredients: '
    , my_dataframe
    , max_selections = 5
)

if ingredients_list :
    #st.write(ingredients_list) #Muestra la lista junto a sun posicion (mas dinamico)
    #st.text(ingredients_list) #muestra la lista de forma normal

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += f"{fruit_chosen} "
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """' , '""" + name_on_order + """')"""
    
    #st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!', icon="✅")



import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)









    
