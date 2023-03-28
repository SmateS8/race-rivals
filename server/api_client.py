import requests

SERVER_URL = "http://localhost:5000/register"


data = { "username":"DEFAULT",
        "password" : "PASSWORD"

}
response = requests.post(SERVER_URL,json=data)
print(response.json())
