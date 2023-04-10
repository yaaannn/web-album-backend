from django.test import TestCase
from django.conf import settings

# Create your tests here.
list = ["1", "2"]
print(list)

lists = ["c" + i for i in list]
print(lists)

print(settings.UPLOAD_DIR)
