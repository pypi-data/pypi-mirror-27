-*- coding: utf-8 -*-

import requests


def gcallres():
        status = requests.get('https://www.google.co.in')
        return status
