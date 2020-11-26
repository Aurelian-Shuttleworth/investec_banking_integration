import requests


class Client:

    def __init__(self, token):
        self.token = token

    def get(self):
        response = requests.get()

