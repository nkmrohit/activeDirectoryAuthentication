from flask import Flask, redirect, request, render_template_string
import msal
import threading

app = Flask(__name__)

# Azure AD configuration
CLIENT_ID = "ab1316ee-7eee-4db5-8adc-aeb943207e39"
CLIENT_SECRET = "SRy8Q~kOYAFkLp50PBxLkfe0N0hel_OZUfUSsdvk"
TENANT_ID = "5eabe8c6-2985-4e34-992a-85fcc1c8b004"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["User.ReadBasic.All","User.Read", "openid", "profile","http://127.0.0.1:5000/login","http://127.0.0.1:5000"]  # Define the scopes here
REDIRECT_URI = "http://localhost:5000/callback"

# Create a public client application
app_msal = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)

@app.route("/")
def home():
    return "Welcome to the app!"

@app.route("/login")
def login():
    auth_url = app_msal.get_authorization_request_url(scopes=SCOPE, redirect_uri=REDIRECT_URI)
    return render_template_string(
        '<script>window.location="{{ auth_url }}"</script>', auth_url=auth_url
    )

@app.route("/callback")
def callback():
    result = app_msal.acquire_token_by_authorization_code(
        request.args["code"], scopes=SCOPE, redirect_uri=REDIRECT_URI
    )
    if "access_token" in result:
        return render_template_string(
            '<script>window.close(); window.opener.postMessage("authenticated", "*");</script>'
        )
    else:
        return "Authentication failed."

if __name__ == "__main__":
    app.run(debug=True)
