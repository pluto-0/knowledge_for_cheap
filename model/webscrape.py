from bs4 import BeautifulSoup as bs
import requests
import pprint


class Book:
    def __init__(self, title, author, price, link, pic):
        self.title = title
        self.author = author
        self.price = price
        self.link = link
        self.pic = pic


def thriftbooks(title):
    url = ("https://www.thriftbooks.com/browse/?b.search="
           + title
           + "#b.s=mostPopular-desc&b.p=1&b.pp=30&b.oos&b.tile")
    response = requests.get(url)
    soup = bs(response.content, "html.parser")
    prices = soup.find_all("div", {"class": "SearchResultListItem-dollarAmount"})
    titles = soup.find_all("div", {"class": "AllEditionsItem-tileTitle"})
    pics = soup.find_all("div", {"class": "SearchResultTileItem-photo"})
    authors = soup.find_all("a", {"itemprop": "author"})
    books = []
    for i in range(len(prices)):
        try:
            books.append(Book(titles[i].text,
                        authors[i].text,
                        prices[i].text,
                        'https://www.thriftbooks.com/' + titles[i].find('a')['href'],
                        pics[i].find('img')['src']))
        except:
            books.append(Book(titles[i].text,
                        authors[i].text,
                        prices[i].text,
                        'https://www.thriftbooks.com/' + titles[i].find('a')['href'],
                        pics[i].find('img')['data-src']))
        finally:
            continue
    return books
    
    

thriftbooks('it')
