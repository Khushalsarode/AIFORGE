import configparser
import re
from trycourier import Courier
import streamlit as st

# Page configuration
st.set_page_config(page_title="Contact Form", page_icon="💌")

# Creating a ConfigParser object
config = configparser.ConfigParser()

# Reading from an INI file
config.read("config.ini")

# Accessing values from the loaded data
auth_token = config.get("mail", "auth_token")
tomail = config.get("mail", "email")

# Display form header
st.markdown("# Contact/Request Form!")

# Form input fields
frommail = st.text_input("Your Email").lower()
subject = st.text_input("Subject").title()
message = st.text_area("Enter Message")

# Create a Courier client
client = Courier(auth_token=auth_token)

# Send message when submit button is clicked
if st.button("Submit"):
    # Simple email validation using regular expression
    email_regex = r"[^@]+@[^@]+\.[^@]+"
    
    # Validate input fields
    if not re.match(email_regex, frommail):
        st.warning("Please enter a valid Email.")
    elif not subject:
        st.warning("Please enter a Subject.")
    elif not message:
        st.warning("Please enter a Message.")
    else:
        try:
            # Send message using Courier
            resp = client.send_message(
                message={
                    "to": {"email": tomail},
                    "content": {"title": subject, "body": f"{{msg}}"},
                    "data": {"msg": message},
                }
            )
            st.success("Message submitted successfully!")
        except Exception as e:
            st.error(f"An error occurred while submitting the message: {e}")
