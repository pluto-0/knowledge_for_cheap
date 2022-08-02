import json
import requests
import pprint
import os
from api import api_key
import datetime

class Book:
    '''simple class for books'''
    def __init__(self, search):
        self.title = None
        self.author = None
        self.description= None
        self.price = None
        self.search = search
        self.img = None
        self.infoList = []

    def getbookInfo(self):
        '''Gets title, author, description and pricing of a book'''
        bookInfo = requests.get('https://www.googleapis.com/books/v1/volumes?q='+self.search+'+isbm:keyes&key='+api_key+'').json()
        for books in bookInfo:
            for i in range(len(bookInfo['items'])):
                if 'title' in bookInfo['items'][i]['volumeInfo']:
                    self.title = bookInfo['items'][i]['volumeInfo']['title']

                if 'authors' in bookInfo['items'][i]['volumeInfo']:
                    self.author = bookInfo['items'][i]['volumeInfo']['authors']
                
                if 'imageLinks' in bookInfo['items'][i]['volumeInfo']:
                    self.img =  bookInfo['items'][i]['volumeInfo']['imageLinks']['thumbnail']
                
                if 'description' in bookInfo['items'][i]['volumeInfo']:
                    self.description = bookInfo['items'][i]['volumeInfo']['description']

                if 'listPrice' in bookInfo['items'][i]['saleInfo']:
                    self.price = bookInfo['items'][i]['saleInfo']['listPrice']['amount']
                
                if self.title == self.search:
                    if self.price is not None:
                        self.infoList.append([self.title, self.author, self.description, self.img, self.price])
                        break
        return self.infoList[0]
            

booksOfTheYear = {
    '1' : 'Beloved',
    '2' : 'Lord of the Flies',
    '3' : 'The Hunger Games',
    '4' : "Charlotte's Web",
    '5' : 'Coraline',
    '6' : 'Little Women',
    '7' : "The Handmaid's Tale ",
    '8' : 'To Kill a Mockingbird',
    '9' : 'Moby-Dick',
    '10' : 'The Kite Runner',
    '11' : 'The Lord of the Rings',
    '12' : 'The Maze Runner'
}

def bookOfTheMonth():
    month = datetime.datetime.now().strftime("%m")
    if month  == '01': 
        return Book(booksOfTheYear['1']).getbookInfo()
    if month  == '02': 
        return Book(booksOfTheYear['2']).getbookInfo()
    if month  == '03': 
        return Book(booksOfTheYear['3']).getbookInfo()
    if month  == '04': 
        return Book(booksOfTheYear['4']).getbookInfo()
    if month  == '05': 
        return Book(booksOfTheYear['5']).getbookInfo()
    if month  == '06': 
        return Book(booksOfTheYear['6']).getbookInfo()
    if month  == '07': 
        return Book(booksOfTheYear['7']).getbookInfo()
    if month  == '08': 
        return Book(booksOfTheYear['8']).getbookInfo()
    if month  == '09': 
        return Book(booksOfTheYear['9']).getbookInfo()
    if month  == '10': 
        return Book(booksOfTheYear['10']).getbookInfo()
    if month  == '11': 
        return Book(booksOfTheYear['11']).getbookInfo()
    if month  == '12': 
        return Book(booksOfTheYear['12']).getbookInfo()
