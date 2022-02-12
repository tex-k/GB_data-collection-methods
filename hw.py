import requests
import json


user = "tex-k"

responce = requests.get(f"https://api.github.com/users/{user}/repos")

repositories = responce.json()

with open("json.json", "w") as f:
    json.dump(repositories, f)

print(f"Список репозиториев пользователя {user}:")
for repo in repositories:
    print(repo["name"])
