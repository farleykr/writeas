import json
import requests


class User:
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers_auth = {
            "Content-Type": "application/json",
            "Authorization": access_token
        }

    def get_access_token(self, username, password):
        headers = {"Content-Type": "application/json"}
        data = {
            "alias": username,
            "pass": password
        }
        res = requests.post(
            "https://write.as/api/auth/login",
            headers=headers, data=f'{json.dumps(data)}'
        )
        access_token = json.dumps(res.json()["data"]["access_token"])
        return access_token

    def get_my_info(self):
        res = requests.get(
            "https://write.as/api/me",
            headers=self.headers_auth
        )
        return json.dumps(res.json(), indent=2)

    def get_my_posts(self):
        res = requests.get(
            "https://write.as/api/me/posts",
            headers=self.headers_auth
        )
        return json.dumps(res.json(), indent=2)

    def get_my_collections(self):
        res = requests.get(
            "https://write.as/api/me/collections",
            headers=self.headers_auth
        )
        return json.dumps(res.json(), indent=2)

    # this doesn't work for me because i don't have any channels
    def get_my_channels(self):
        res = requests.get(
            "https://write.as/api/me/channels",
            headers=self.headers_auth
        )
        return json.dumps(res.json(), indent=2)

    def log_out(self):
        res = requests.delete(
            "https://write.as/api/auth/me",
            headers=self.headers_auth
        )
        if res.status_code != 204:
            return f'Log out attempt was unsuccessful: \
                    Status code: {res.status_code}'
        return 'You have been successfully logged out.'


class Posts:

    def __init__(self, access_token=None):
        self.access_token = access_token
        self.headers = {
            "Content-Type": "application/json"
        }
        self.headers_auth = {
            "Content-Type": "application/json",
            "Authorization": access_token
        }
    
    def publish_post(self, body, title):
        # make option to have auth or standard headers
        data = {
            "body": body,
            "title": title 
        }
        res = requests.post(
            "https://write.as/api/posts",
            headers=self.headers, data=f'{json.dumps(data)}'
        )
        return json.dumps(res.json(), indent=2)

    def get_post(self, post_id):
        res = requests.get(
            f"https://write.as/api/posts/{post_id}"
        )
        return json.dumps(res.json(), indent=2)
    
    def update_post(self, post_id, token, body):
        data = {
            "token": token,
            "body": body
        }
        res = requests.post(
            f"https://write.as/api/posts/{post_id}",
            headers=self.headers, data=f'{json.dumps(data)}'
        )
        return json.dumps(res.json(), indent=2)
    
    def unpublish_post(self, post_id, token):
        data = {
            "body": "",
            "token": token 
        }
        res = requests.post(
            f"https://write.as/api/posts/{post_id}",
            headers=self.headers_auth, data=f'{json.dumps(data)}'
        )
        return json.dumps(res.json(), indent=2)
    
    def delete_post(self, post_id, token):
        params = {
            "token": token
        }
        res = requests.delete(
            f"https://write.as/api/posts/{post_id}",
            headers=self.headers_auth, params=params
        )
        if res.status_code != 204:
            return f"Post could not be deleted. Status code: {res.status_code}"
        return "Post was successfully deleted."
    
    def claim_post(self, post_id, token):
        data = {
            "id": post_id,
            "token": token  
        }
        res = requests.post(
            "https://write.as/api/posts/claim",
            headers=self.headers_auth, data=f'[{json.dumps(data)}]'
        )
        return json.dumps(res.json(), indent=2)


class Collections:

    def __init__(self, access_token=None):
        self.access_token = access_token
        self.headers_auth = {
            "Content-Type": "application/json",
            "Authorization": access_token
        }

    # need to upgrade account to atleast casual before this will work,
    # but the code is correct
    def create_collection(self, alias, title):
        data = {
            "alias": alias,
            "title": title
        }
        res = requests.post(
            f"https://write.as/api/collections",
            headers=self.headers_auth, data=f'{json.dumps(data)}'
        )
        return json.dumps(res.json(), indent=2)

    def get_collection(self, col_alias):
        res = requests.get(
            f"https://write.as/api/collections/{col_alias}",
            headers=self.headers_auth
        )
        return json.dumps(res.json(), indent=2)
    
    def delete_collection(self, col_alias):
        res = requests.delete(
            f"https://write.as/api/collections/{col_alias}",
            headers=self.headers_auth
        )
        if res.status_code != 204:
            return f'Collection could not be deleted. \
                    Status code: {res.status_code}'
        return f'Collection {col_alias} was successfully deleted'

    def get_collection_post(self, alias, slug):
        res = requests.get(
            f"https://write.as//api/collections/{alias}/posts/{slug}",
            headers=self.headers_auth
        )
        return json.dumps(res.json(), indent=2)
        
    def publish_collection_post(self, alias, body, title):
        data = {
            "body": body,
            "title": title
        }
        res = requests.post(
            f"https://write.as/api/collections/{alias}/posts",
            headers=self.headers_auth, data=f'{json.dumps(data)}'
        )
        return json.dumps(res.json(), indent=2)
        
    def get_collection_posts(self, alias):
        res = requests.get(
            f"https://write.as/api/collections/{alias}/posts",
            headers=self.headers_auth
        )
        return json.dumps(res.json(), indent=2)

    # needs more work; returns error even though post is successfully moved.
    def move_post_to_collection(self, alias, post_id, token):
        data = {
            "id": post_id,
            "token": token
        }
        res = requests.post(
            f"https://write.as/api/collections/{alias}/collect",
            headers=self.headers_auth, data=f'[{json.dumps(data)}]'
        )
        return json.dumps(res.json(), indent=2)
        
    def pin_post_to_collection(self, alias, post_id, pos=None):
        data = {
            "id": post_id,
            "position": pos
        }
        res = requests.post(
            f"https://write.as/api/collections/{alias}/pin",
            headers=self.headers_auth, data=f'[{json.dumps(data)}]'
        )
        return json.dumps(res.json(), indent=2)
    
    def unpin_post_from_collection(self, alias, post_id):
        data = {
            "id": post_id,
        }
        res = requests.post(
            f"https://write.as/api/collections/{alias}/unpin",
            headers=self.headers_auth, data=f'[{json.dumps(data)}]'
        )
        return json.dumps(res.json(), indent=2)
