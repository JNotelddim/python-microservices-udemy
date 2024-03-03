import requests
from flask import session

from . import USER_API_URL

class UserClient:
    @staticmethod
    def login(form):
        print('[UserClient] get user...')
        api_key = None
        payload = {
            'username': form.username.data,
            'password': form.password.data,
        }

        url = USER_API_URL + '/api/user/login'

        response = requests.post(url, data=payload)
        if response:
            api_key = response.json().get('api_key')

        print(f'[UserClient] repsonse: {response}, api_key: {api_key}')

        return api_key

    @staticmethod
    def logout():
        url = USER_API_URL + '/api/user/logout'
        response = requests.post(url)
        print('[UserClient] logout result' + str(response))
        return response

    @staticmethod
    def get_user():
        headers = {
            'Authorization': session['user_api_key']
        }
        print(f'[UserClient get_user()] headers: {headers}')
        url = USER_API_URL + '/api/user/'

        response = requests.get(url, headers=headers)
        print(f'[UserClient get_user()] response: {response}')
        return response.json()

    @staticmethod
    def create_user(form):
        user = None
        payload = {
            'username': form.username.data,
            'password': form.password.data,
        }

        url = USER_API_URL + '/api/user/create'

        response = requests.post(url, data=payload)
        if response:
            user = response.json()

        return user

    @staticmethod
    def user_exists(username):
        url = USER_API_URL + f'/api/user/{username}/exists'

        response = requests.get(url)
        return response.status_code == 200