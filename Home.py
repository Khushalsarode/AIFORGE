import streamlit as st
import pymongo
import datetime
import os
from datetime import timedelta

import configparser

# Creating a ConfigParser object
config = configparser.ConfigParser()
# Reading from an INI file
config.read("config.ini")

# Accessing values from the loaded data
mongouri = config.get("mongodb", "uri")
mongodb = config.get("mongodb", "db_name")
tools_collection = config.get("mongodb","user")
keyword = config.get("mongodb","words")
mongoapprovetool = config.get("mongodb","admin")

 # Connect to MongoDB
client = pymongo.MongoClient(mongouri)
db = client[mongodb]
# Get collections
approved_tools_collection = db[mongoapprovetool]
keywords_collection = db[keyword]
user_added_tools_collection = db[tools_collection]
daily_visits_collection = db["DailyVisits"]

# Set page configuration
st.set_page_config(
    page_title="AIForge",
    page_icon="🌐",
)

# Welcome message
st.write("# Welcome to All In Open Source! 🚀")

st.sidebar.success("Explore and discover AI tools.")

st.markdown(
    """
    All In Open Source is your go-to platform for discovering and sharing free
    and open-source AI tools created by the community. Whether you're in a hurry
    or looking for something specific, we've got you covered!

    **👈 Select a tool or use the search functionality** to get started.
    
    ### Why All In Open Source?
    - **One Place, Many Tools:** Find a variety of AI tools conveniently located in one place.
    - **Free to Use:** All tools on our platform are open source or free to use.
    - **Get Notified:** Receive an email when your submitted tool/content gets accepted.

    ### Want to share your AI tool?
    - Click on the **Add Tool** button in the sidebar.
    - Fill in the details and contribute to the community!

    ### Reach Out any Query or Feedback ➿
    - Mail-us: admin@aiforgetech.co

    ### Start exploring now!
    - Check out the tools in the sidebar or use the search bar.
    
    ### Stay Informed!
    - Receive email notifications when your tool or content is accepted.
    """
)

# Title and page configuration for the dashboard
st.title("All In Open Source Dashboard - AiForge📊")
st.sidebar.header("Dashboard Options")

# Create three columns layout for better organization
col1, col2, col3 = st.columns(3)

# Column 1: Display key metrics with improved styling
with col1:
    st.subheader("Total Tools Available")
    st.markdown(f"<h1 style='text-align: center; color: #4CAF50;'>{approved_tools_collection.count_documents({})}</h1>", unsafe_allow_html=True)

# Column 2: Display key metrics with improved styling
with col2:
    st.subheader("Total Categories")
    st.markdown(f"<h1 style='text-align: center; color: #3498db;'>{keywords_collection.count_documents({})}</h1>", unsafe_allow_html=True)

# Column 3: Display key metrics with improved styling
with col3:
    st.subheader("Total User Contributions")
    st.markdown(f"<h1 style='text-align: center; color: #e74c3c;'>{len(approved_tools_collection.distinct('user_email'))}</h1>", unsafe_allow_html=True)

# Function to update visit counts
def update_visit_count():
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")

    # Check if the file exists
    file_path = "visit_data.txt"
    if os.path.exists(file_path):
        # Read existing data
        with open(file_path, "r") as file:
            data = file.read().splitlines()
            daily_visits = int(data[0])
            total_visits = int(data[1])
    else:
        # If the file doesn't exist, create it and initialize counts to zero
        daily_visits = 0
        total_visits = 0
        data = []  # Declare data before the else block

    # Update visit counts
    if len(data) > 2 and today_str != data[2]:
        daily_visits = 0  # Reset daily visits if a new day has started
    daily_visits += 1
    total_visits += 1

    # Write updated data back to the file
    with open(file_path, "w") as file:
        file.write(f"{daily_visits}\n{total_visits}\n{today_str}")

    return daily_visits, total_visits

# Update visit counts
today = datetime.date.today()
daily_visits, total_visits = update_visit_count()

# Display counts with improved styling
st.markdown("<hr>", unsafe_allow_html=True)  # Add a horizontal line for separation
st.header("Visit Counts")
st.write(f"<p style='font-size: 20px; text-align: center;'>Today's Visits: <b>{daily_visits}</b></p>", unsafe_allow_html=True)
st.write(f"<p style='font-size: 20px; text-align: center;'>Total Visits: <b>{total_visits}</b></p>", unsafe_allow_html=True)

# Column 2: Display daily and total visit counts with improved styling
st.sidebar.markdown("<hr>", unsafe_allow_html=True)  # Add a horizontal line for separation
st.sidebar.subheader("Daily and Total Visits")
today_datetime = datetime.datetime(today.year, today.month, today.day)  # Convert to datetime object
daily_visits_st = st.sidebar.number_input("Today's Visits", value=daily_visits, key="today_visits", format="%d")
total_visits_st = st.sidebar.number_input("Total Visits", value=total_visits, key="total_visits", format="%d")

