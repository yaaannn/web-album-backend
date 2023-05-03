from django.test import TestCase
import requests

# Create your tests here.

baseURL = "http://127.0.0.1:8000"

r = requests.get(baseURL + "/api/v1/photo/info?id=8")

print(r.elapsed.microseconds)
