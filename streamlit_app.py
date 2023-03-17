import streamlit
import pandas
import requests 

#snowflake connection
import snowflake.connector

from urllib.error import URLError

streamlit.title('My Mom\'s new healthy diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
 
# Filter the DataFrame based on the selected fruits
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

#Fruit choice to Snowflake procedure

def get_fruitvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice)
   #convert json output into a dataframe
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized

def get_fruit_load_list():
 with my_cnx.cursor() as my_cur:
   my_cur.execute("select * from fruit_load_list")
   my_data_rows = my_cur.fetchall()
   return my_data_rows2
  
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
   #add fruit to snowflake
   my_cur.execute("insert into fruit_load_list values(new_fruit)")
   return "Thanks for adding " + new_fruit
 
streamlit.header('Fruityvice Fruit Advice!')
try:
 #pass fruit name to api
 fruit_choice = streamlit.text_input('What fruit would you like information about?')
 if not fruit_choice:
  streamlit.error("Please select a fruit to get information.")
 else:
  #send api request with fruit name using function
  fruit_from_function=get_fruitvice_data(fruit_choice)
  streamlit.dataframe(fruit_from_function)
  

except URLError as e:
 streamlit.error()
 

#Add Streamlit button to fetch from snowflake
if streamlit.button("Get Fruit load list"):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 my_data_rows = get_fruit_load_list()
 streamlit.dataframe(my_data_rows)

#streamlit.text("The fruit load list contains:")
#streamlit.dataframe(my_data_rows)

#pass fruit name to text
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button("Get Fruit load list"):
 my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
 back_from_function = insert_row_snowflake(add_my_fruit)
streamlit.text(back_from_function)



