import pymongo
import requests
import streamlit as st
from PIL import Image as PILImage
from io import BytesIO
import re

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
defaultlogo=config.get("defaultlogo","logourl")
 # Connect to MongoDB
client = pymongo.MongoClient(mongouri)
db = client[mongodb]
tools_collection = db[tools_collection]
keywords_collection = db[keyword]


st.set_page_config(page_title="Adding New Tool", page_icon="🔮")

st.markdown("# Request Tool Adding")
#st.sidebar.header("Request Tool Adding")
st.write("This demo illustrates a combination of plotting and animation with Streamlit. Were generating a bunch of random numbers in a loop for around 5 seconds. Enjoy!")

default_logo_url = defaultlogo

# Function to resize image data
def resize_image(image_data, size=(80, 40)):  # Updated logo size to 80 x 40 pixels
    img = PILImage.open(BytesIO(image_data))
    img.thumbnail(size)
    resized_image_data = BytesIO()
    img.save(resized_image_data, format="PNG")
    return resized_image_data.getvalue()

def is_valid_email(email):
    # Simple email validation using regular expression
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(email_regex, email)

def is_valid_tool_name(tool_name):
    # Validate tool name as alphanumeric
    return tool_name.isalnum()

def is_valid_website_link(link):
    # Validate a full website link using regular expression
    website_regex = r"^https?://(www\.)?([a-zA-Z0-9-]+\.?)+[^\s]+$"
    return re.match(website_regex, link)

st.header("Share Your AI Tool")

# Create a form for tool submission
with st.form(key="tool_submission_form"):
    # Add form fields
    st.subheader("Tool Information:")
    tool_icon = st.file_uploader("Upload Tool Icon (PNG, SVG, JPEG, JPG)", type=["png", "svg", "jpeg", "jpg"], key="tool_icon", help="Max size: 2MB")
    tool_name = st.text_input("Tool/book/course Name").title()
    tool_description = st.text_area("Tool Usage Description", max_chars=500)
    tool_website = st.text_input("Website Link")
    user_email = st.text_input("Your Email")

     # Fetch keywords from the MongoDB collection
    available_keywords = [kw["keyword"] for kw in keywords_collection.find()]
    
    num_required_keywords = st.empty()  # Placeholder to dynamically update the number of required keywords
    selected_keywords = st.multiselect("Select Keywords", available_keywords, key="selected_keywords")
    num_required_keywords.markdown(f"*Number of Required Keywords: {max(4 - len(selected_keywords), 0)}*")



    # Display warnings after form submission
    st.subheader("Individual Warnings:")
    
    if not tool_name:
        st.warning("- Please enter a Tool Name.")
    
    if not tool_description:
        st.warning("- Please enter a Tool Usage Description.")
    
    if not is_valid_tool_name(tool_name):
        st.warning("- Tool Name should be alphanumeric.")
    
    if not is_valid_email(user_email):
        st.warning("- Please enter a valid Email.")
    
    if not is_valid_website_link(tool_website):
        st.warning("- Please enter a valid Website Link.")
    
    if len(selected_keywords) < 4:
        st.warning("- Please select at least 4 Keywords.")

    
    # Submit button
    submit_button = st.form_submit_button(label="Submit Tool")

    # Handle form submission
if submit_button:
    
    # Validate and save the tool information to MongoDB
    if (
        tool_name 
        and tool_description 
        and tool_website 
        and user_email 
        and is_valid_tool_name(tool_name) 
        and is_valid_email(user_email) 
        and is_valid_website_link(tool_website) 
        and len(tool_description) <= 500
        and len(selected_keywords) >= 4

    ):
        if tool_icon:
            # Resize the uploaded tool icon to a thumbnail
            thumbnail_data = resize_image(tool_icon.read(), size=(80, 40))  # Updated logo size to 80 x 40 pixels
        else:
            # Use the default logo if no custom logo is provided
            default_logo_image = PILImage.open(BytesIO(requests.get(default_logo_url).content))  # Ensure you have the 'requests' library installed
            default_logo_data = resize_image(requests.get(default_logo_url).content, size=(80, 40))
            
            st.image(default_logo_image, caption='Default Logo', use_column_width=False)
            
            # Set the default logo data for saving to MongoDB
            thumbnail_data = default_logo_data


        # Save tool information to MongoDB
        tools_collection.insert_one({
            "tool_name": tool_name,
            "tool_description": tool_description,
            "tool_website": tool_website,
            "user_email": user_email,
            "thumbnail_data": thumbnail_data,
            "keywords": selected_keywords,
        })

        st.success("Tool submitted successfully!")
    else:
        st.warning("Please fill in all required fields and ensure valid input.")


# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")