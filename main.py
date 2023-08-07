import streamlit as st
import msal
from flask import Flask, request 
from concurrent.futures import ThreadPoolExecutor
from streamlit_azure_login import login_component

# Azure AD configuration
CLIENT_ID = "ab1316ee-7eee-4db5-8adc-aeb943207e39"
CLIENT_SECRET = "SRy8Q~kOYAFkLp50PBxLkfe0N0hel_OZUfUSsdvk"
TENANT_ID = "5eabe8c6-2985-4e34-992a-85fcc1c8b004"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["User.Read", "openid", "profile"]
REDIRECT_URI = "https://birlasoft.azurewebsites.net/"
GROUP_ID = "4c604932-4c47-40d5-81da-420a0e6acaa9"

import webbrowser
import requests



client_id = CLIENT_ID
tenant_id = TENANT_ID
redirect_uri = "https://birlasoft.azurewebsites.net/"
scopes = ["https://graph.microsoft.com/.default"]
authority = f"https://login.microsoftonline.com/{tenant_id}"
endpoint = "https://graph.microsoft.com/v1.0/me"

app = msal.PublicClientApplication(
    client_id, authority=authority, verify=False
)

def get_token_from_cache():
    accounts = app.get_accounts()
    if not accounts:
        return None
    
    result = app.acquire_token_silent(scopes, account=accounts[0])
    if "access_token" in result:
        return result["access_token"]
    else:
        return None

def login():
    flow = app.initiate_auth_code_flow(scopes=scopes, state=['somestupidstate'])
    print(flow)
    if "auth_uri" not in flow:
        return st.write("Failed with token")
    
    auth_uri = flow['auth_uri']
    webbrowser.open(auth_uri, new=0)
    auth_code = st.experimental_get_query_params()
    
    if 'code' not in auth_code:
        return st.write("Failed with token")
    
    result = app.acquire_token_by_authorization_code(auth_code, scopes=scopes)
    print(result)
    if "access_token" in result:
        
        return result["access_token"]
    else:
        return st.write("No token found")


if st.button("Login"):
    get_token_from_cache()
    token = login()

    st.write(st.experimental_get_query_params())
    if token:
        st.write("Logged in successfully!")
        st.write(token)
    else:
        st.write("Failed to login")
