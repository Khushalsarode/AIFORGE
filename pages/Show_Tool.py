import streamlit as st
import pymongo
from PIL import Image as PILImage
from io import BytesIO

import configparser

# Creating a ConfigParser object
config = configparser.ConfigParser()
# Reading from an INI file
config.read("config.ini")

# Accessing values from the loaded data
mongouri = config.get("mongodb", "uri")
mongodb = config.get("mongodb", "db_name")
mongoapprovetool = config.get("mongodb","admin")
keyword = config.get("mongodb","words")
 # Connect to MongoDB
client = pymongo.MongoClient(mongouri)
db = client[mongodb]
approved_collection = db[mongoapprovetool]
keywords_collection=db[keyword]

st.set_page_config(page_title="Show Tool Card", page_icon="🌍")

st.markdown("# Show Tool Card")

# Search bar for tool name
search_query = st.text_input("Search by Tool Name", "")

# Keywords selection
available_keywords = [kw["keyword"] for kw in keywords_collection.find()]
selected_keywords = st.multiselect("Filter by Keywords", available_keywords)

# Function to resize image data
def resize_image(image_data, size=(80, 40)):
    img = PILImage.open(BytesIO(image_data))
    img.thumbnail(size)
    resized_image_data = BytesIO()
    img.save(resized_image_data, format="PNG")
    return resized_image_data.getvalue()

# Display tool cards based on search query
if search_query:
    st.subheader(f"Search Results for '{search_query}':")
    matched_tools = approved_collection.find({"tool_name": {"$regex": f".*{search_query}.*", "$options": "i"}})
    
    for tool in matched_tools:
        st.markdown(f"## {tool['tool_name']}")
        st.image(resize_image(tool["thumbnail_data"]), caption="Tool Icon", use_column_width=False)
        st.write(f"**Description:** {tool['tool_description']}")
        st.link_button("Tool Website", approved_collection['tool_website'])
        #st.write(f"**Website:** {tool['tool_website']}")
        #st.write(f"**Email:** {tool['user_email']}")
        st.write("---")

# Display tool cards based on selected keywords
if selected_keywords:
    st.subheader(f"Tools Related to Selected Keywords:")
    keyword_matched_tools = approved_collection.find({"keywords": {"$in": selected_keywords}})
    
    # Display tools in a grid format
    tools_in_row = 2  # Number of tools to display in each row
    tools = list(keyword_matched_tools)
    
    for i in range(0, len(tools), tools_in_row):
        row_tools = tools[i:i + tools_in_row]
        col1, col2 = st.columns(2)
        
        for tool in row_tools:
            with col1:
                st.markdown(f"## {tool['tool_name']}")
                st.image(resize_image(tool["thumbnail_data"]), caption="Tool Icon", use_column_width=False)
                st.write(f"**Description:** {tool['tool_description']}")
                st.link_button("Tool Website", approved_collection['tool_website'])
                #st.write(f"**Website:** {tool['tool_website']}")
                #st.write(f"**Email:** {tool['user_email']}")
                #st.write(f"**Keywords:** {', '.join(tool['keywords'])}")
                st.write("---")
