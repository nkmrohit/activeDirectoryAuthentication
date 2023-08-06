import streamlit as st
import msal
import requests

# Azure AD configuration
CLIENT_ID = "ab1316ee-7eee-4db5-8adc-aeb943207e39"
TENANT_ID = "5eabe8c6-2985-4e34-992a-85fcc1c8b004"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID.replace('{', '').replace('}', '')}"
SCOPE = ["https://graph.microsoft.com/.default"]
GROUP_ID = "4c604932-4c47-40d5-81da-420a0e6acaa9"

# Create a public client application
app = msal.PublicClientApplication(
    CLIENT_ID, authority=AUTHORITY
)

import streamlit as st
import msal
import requests
from flask import Flask, request, redirect
import threading

# Azure AD configuration

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID.replace('{', '').replace('}', '')}"
SCOPE = ["https://graph.microsoft.com/.default"]
REDIRECT_URI = "https://mahinm.azurewebsites.net/"  # Replace with your callback URI


# Create a public client application
app = msal.PublicClientApplication(
    CLIENT_ID, authority=AUTHORITY
)

# Streamlit app
def main():
    st.title("Streamlit Azure AD Authentication")
    st.write("This is a protected application. Only users from a specific Azure AD group can access it.")

    # Attempt to get a token from Azure AD
    result = None
    try:
        result = app.acquire_token_silent(SCOPE, account=None)
    except msal.TokenCacheMissError:
        pass

    if not result:
        st.info("Please sign in to access the application.")
        # Redirect the user to sign-in with Azure AD
        signin = st.button("Sign In")
        if signin:
            flow = app.initiate_device_flow(SCOPE)
            st.markdown(flow["message"])
            result = app.acquire_token_by_device_flow(flow)
    print("Result data",result)
    if result:
        # Check if the user is a member of the specified AD group
        graph_url = "https://graph.microsoft.com/v1.0/me/memberOf"
        headers = {"Authorization": f"Bearer {result['access_token']}"}
        response = requests.get(graph_url, headers=headers)
        groups = response.json().get("value", [])
        group_names = [group.get("displayName", "") for group in groups]
        
        if GROUP_ID in group_names:
            st.success("You are authorized to access this application.")
            st.write("You can now close this window and return to the AD-verification application.")
            # Add your application logic here
        else:
            st.error("You are not authorized to access this application.")
    else:
        st.error("Authentication failed. Please try again.")

def run_flask():
    app_flask = Flask(__name__)

    @app_flask.route("/callback")
    def callback():
        token = request.args.get("token")
        st.session_state.token = token
        return redirect("/")

    app_flask.run(port=8501)  # Use a different port to avoid conflicts

if __name__ == "__main__":
    st_thread = threading.Thread(target=run_flask)
    st_thread.start()
    main()

