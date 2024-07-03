import requests

# API 서버의 URL
BASE_URL = "http://localhost:8000"

def get_token(username: str, password: str):
    url = f"{BASE_URL}/token"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, data=data)
    return response.json()

def get_user_details(token: str):
    url = f"{BASE_URL}/users/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers= headers)
    return response.json()

# 사용자의 username과 password
username = "yeachan"
password = "secret"

# 토큰 받아오기
token_response = get_token(username, password)
if "access_token" in token_response:
    token = token_response["access_token"]
    print("Token received:-", token)
    #토큰을 사용해 유저 정보 가져오기
    user_details = get_user_details(token)
    print("User details:", user_details)
else:
    print("Failed to login")

# 테스트
token = "faketoken"
user_details = get_user_details(token)
print(user_details)
