import requests

# global variables
BASE_URL = "https://jcssantos.pythonanywhere.com/api/group13/group13"

def view_all_coins(access_token):
   # use the access token to make an authenticated request
   headers = {
       'Authorization': f'Bearer {access_token}'
   }

   # make a GET request with the authorization header
   api_response = requests.get(BASE_URL, headers=headers)

   if api_response.status_code == 200:
       # process the data from the API
       return api_response.json()
   else:
       print("Failed to access the API endpoint to view all coins:", api_response.status_code)

def view_balance_for_user(access_token, email):
   # use the access token to make an authenticated request
   headers = {
       'Authorization': f'Bearer {access_token}'
   }

   # make a GET request with the authorization header
   api_response = requests.get(f'{BASE_URL}/player/{email}/', headers=headers)

   if api_response.status_code == 200:
       # process the data from the API
       return api_response.json().get('amount')
   else:
       print("Failed to access the API endpoint to view balance for user:", api_response.status_code)
       return None

def user_pay(access_token, email, amount):
   # Use the access token to make an authenticated request
   headers = {
       'Authorization': f'Bearer {access_token}'
   }
   data = {"amount": amount} # non-negative integer value to be decreased
   # Make a POST request with the authorization header and data payload
   api_response = requests.post(f"{BASE_URL}/player/{email}/pay", headers=headers, data=data)


   if api_response.status_code == 200:
       # Process the data from the API
       return api_response.json()
   else:
       print("Failed to access the API endpoint to pay:", api_response.status_code)
