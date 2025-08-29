import requests

def call_git(owner, repo, path, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"}
    
    # Fetch file from GitHub
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # raise error if something goes wrong
    
    # Decode base64 content returned by GitHub API
    return response.json()["content"]