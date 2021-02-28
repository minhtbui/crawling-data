import requests
import json
import csv

book_page_url = "https://tiki.vn/api/v2/products?category=320&urlKey=business-economics&limit=300&page=1"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

response = requests.get(book_page_url, headers=headers)
print(response.text)
