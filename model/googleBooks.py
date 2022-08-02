import json
import requests
import pprint
import os
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
        bookInfo = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:'+self.search+'').json()
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
                
                self.infoList.append([self.title, self.author, self.description, self.img, self.price])
        return self.infoList[0]

    def getTitle(self):
        '''Gets title of a book'''
        bookInfo = requests.get('https://www.googleapis.com/books/v1/volumes?q=isbn:'+self.search+'').json()
        for books in bookInfo:
            for i in range(len(bookInfo['items'])):
                if 'title' in bookInfo['items'][i]['volumeInfo']:
                    self.title = bookInfo['items'][i]['volumeInfo']['title']   
        return self.title

booksOfTheYear = {
    '1' : '1-58060-120-0',
    '2' : '0-571-05686-5',
    '3' : '978-0-439-02352-8',
    '4' : "0064400557",
    '5' : '0-06-113937-8',
    '6' : '0590225375',
    '7' : "038549081X",
    '8' : '9780871299208',
    '9' : '1509826645',
    '10' : '9781594631931',
    '11' : '0544273443',
    '12' : '978-0-385-73794-4'
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
