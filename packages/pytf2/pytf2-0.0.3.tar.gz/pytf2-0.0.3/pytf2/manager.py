import requests


class Manager:
    def __init__(self, bp_api_key=''):
        self.bp_api_key = bp_api_key
        print(self.bp_api_key)