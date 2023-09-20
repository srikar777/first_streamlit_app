import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')  

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')
#Let's put a pick list here so they can pick the fruit they want to include

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on page
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
#streamlit.write('The user entered ', fruit_choice)

def get_fruityvice_data(this_fruit_choice):
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # write your own comment -what does the next line do? 
     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # write your own comment - what does this do?
     return fruityvice_normalized

#import requests
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  #streamlit.text(fruityvice_response.json())
  if not fruit_choice:
    streamlit.error("Please select fruit to get a information")
  else: 
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()

#import snowflake.connector

streamlit.header("View Our Fruit List - Add Your Favourites:")
#snowflake-related functions

def get_fruit_load_list():
     with my_cnx.cursor() as my_cur:
          my_cur.execute("select * from fruit_load_list")
          return my_cur.fetchall()

#Add a button to load the fruit

if streamlit.button('Get Fruit Load List'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     my_data_rows = get_fruit_load_list()
     my_cnx.close()
     streamlit.text(my_data_rows)

def insert_row_snowflake(new_fruit):
     with my_cnx.cursor() as my_cur:
          my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
          return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add')
if streamlit.button('Add a Fruit to the List'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     back_from_function = insert_row_snowflake(add_my_fruit)
     my_cnx.close()
     streamlit.text(back_from_function)

streamlit.stop()



