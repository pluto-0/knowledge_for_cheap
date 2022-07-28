import json
import requests
import pprint
import os
from api import api_key

class Book:
    '''simple class for books'''
    def __init__(self, search):
        self.title = None
        self.author = None
        self.description= None
        self.price = None
        self.search = search

    def getbookInfo(self):
        '''Gets title, author, description and pricing of a book'''
        fullInfo = []
        bookInfo = requests.get('https://www.googleapis.com/books/v1/volumes?q='+self.search+'+isbm:keyes&key='+api_key+'').json()
        for books in bookInfo:
            for i in range(len(bookInfo['items'])):
                #pprint.pprint(bookInfo['items'])
                if 'title' in bookInfo['items'][i]['volumeInfo']:
                    self.title = bookInfo['items'][i]['volumeInfo']['title']
                
                if 'authors' in bookInfo['items'][i]['volumeInfo']:
                    self.author = bookInfo['items'][i]['volumeInfo']['authors']
                
                if 'description' in bookInfo['items'][i]['volumeInfo']:
                    self.description = bookInfo['items'][i]['volumeInfo']['description']

                if 'listPrice' in bookInfo['items'][i]['saleInfo']:
                    self.price = bookInfo['items'][i]['saleInfo']['listPrice']['amount']
                fullInfo.append([self.title, self.author, self.description, self.price])
        pprint.pprint(fullInfo) 
