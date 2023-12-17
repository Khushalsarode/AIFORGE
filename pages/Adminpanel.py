import pymongo
import redis
import streamlit as st
from PIL import Image as PILImage, UnidentifiedImageError
from io import BytesIO
import configparser
from trycourier import Courier


def is_username_unique(username):
    # Check if the username already exists in Redis
    return redis_client.hget("users", username) is None

def is_user_logged_in():
    return "username" in st.session_state

def logout():
    if is_user_logged_in():
        del st.session_state["username"]
        st.success("Logged out successfully")


# Creating a ConfigParser object
config = configparser.ConfigParser()
# Reading from an INI file
config.read("config.ini")

# Accessing values from the loaded data
mongouri = config.get("mongodb", "uri")
mongodb = config.get("mongodb", "db_name")
mongousetool = config.get("mongodb","user")
mongoapprovetool = config.get("mongodb","admin")
defaultlogo=config.get("defaultlogo","logourl")

 # Connect to MongoDB
client = pymongo.MongoClient(mongouri)
db = client[mongodb]
initial_collection = db[mongousetool]
approved_collection = db[mongoapprovetool]

auth_token = config.get("mail","auth_token")
sendermail = config.get("mail","email")

client = Courier(auth_token=auth_token)


st.set_page_config(page_title="Admin Panel", page_icon="🛠️")

st.markdown("# Admin Panel - Tool Approval")



# Accessing values from the loaded data
REDIS_HOST = config.get("redis", "host")
REDIS_PORT = config.get("redis", "port")
REDIS_PASSWORD = config.get("redis","password")
# Your login logic here

# Connect to Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, decode_responses=True)

def adminpanel():
   
   
    # Fetch tool submissions from the initial collection
    tool_submissions = initial_collection.find()


    # Specify the number of columns in the grid (2 by 2 or 3 by 3)
    num_columns = 2

    # Calculate column width based on the number of columns
    column_width = int(12 / num_columns)

    # Default logo or placeholder image
    default_logo_url = defaultlogo
    for i, tool_submission in enumerate(tool_submissions):
        if i % num_columns == 0:
            # Create columns for each row
            columns = st.columns(num_columns)

        with columns[i % num_columns]:
            st.subheader(f"Tool Submission ID: {tool_submission['_id']}")
            st.write(f"Tool Name: {tool_submission['tool_name']}")
            st.write(f"Tool Description: {tool_submission['tool_description']}")
            st.write(f"Tool Website: {tool_submission['tool_website']}")
            #st.link_button("Tool Website", tool_submission['tool_website'])
            st.write(f"User Email: {tool_submission['user_email']}")
            st.write(f"Keywords: {tool_submission.get('keywords', [])}")

            try:
                # Display the tool icon with a smaller size (e.g., 80 x 40 pixels)
                if 'thumbnail_data' in tool_submission:
                    logo_image = PILImage.open(BytesIO(tool_submission['thumbnail_data']))
                    resized_logo = logo_image.resize((80, 40))
                    st.image(resized_logo, caption='Tool Icon', use_column_width=False)
                else:
                    # Display the default logo with a smaller size (e.g., 80 x 40 pixels)
                    st.image(default_logo_url, caption='Default Logo', width=80, height=40, use_column_width=False)
            except UnidentifiedImageError:
                st.text("Invalid image format. Unable to display tool icon.")

            # Approve and reject buttons
            approve_button = st.button(f"Approve Tool Submission {tool_submission['_id']}")
            reject_button = st.button(f"Reject Tool Submission {tool_submission['_id']}")

            # Handle button actions
            if approve_button:
                # Move the record to the approved collection
                approved_collection.insert_one(tool_submission)
                st.success(f"Tool Submission {tool_submission['_id']} approved and moved to the approved collection.")
                
                # Delete the record from the initial collection
                initial_collection.delete_one({'_id': tool_submission['_id']})
                st.info(f"Tool Submission {tool_submission['_id']} deleted from the initial collection.")
                resp = client.send_message(
                message={
                "to": {
                 "email": tool_submission['user_email']
                },
                "content": {
                 "title": "Your Tool Passed Reviev! & approved!",
                 "body": " {{msg}}"
                },
                "data":{
                "msg": f"Hey! Thanks for contributing and expanding the community app!"
                }
                }
                )

            
            elif reject_button:
                # Delete the record from the initial collection
                initial_collection.delete_one({'_id': tool_submission['_id']})
                st.warning(f"Tool Submission {tool_submission['_id']} rejected and deleted from the initial collection.")

    # Optionally, you can add a button to refresh the admin panel
    if st.button("Refresh"):
        st.experimental_rerun()


username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if redis_client.hexists("users", username):
        stored_data_str = redis_client.hget("users", username)
        stored_data_dict = eval(stored_data_str)

        if stored_data_dict["password"] == password:
            st.session_state["username"] = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid password. Please try again.")
    else:
        st.error("Username not found. Please check your username or create a new account.")

# Admin panel section
if is_user_logged_in():
    adminpanel()

# Always display the logout button
if is_user_logged_in():
    st.sidebar.button("Logout", on_click=logout)