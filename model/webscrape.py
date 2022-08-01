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


def is_isbn(title):
    if len(title) == 10 or len(title) == 13:
        for letter in title:
            if letter not in ('0, 1, 2, 3, 4, 5, 6, 7, 8, 9'):
                return False
        return True
    return False


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
    books = set()
    for i in range(len(prices)):
        try:
            books.add(Book(titles[i].text,
                        authors[i].text,
                        prices[i].text,
                        'https://www.thriftbooks.com/' + titles[i].find('a')['href'],
                        pics[i].find('img')['src']))
        except:
            books.add(Book(titles[i].text,
                        authors[i].text,
                        prices[i].text,
                        'https://www.thriftbooks.com/' + titles[i].find('a')['href'],
                        pics[i].find('img')['data-src']))
        finally:
            continue
    return books


def cheapest_textbooks(title='', isbn=''):
    # Getting list of isbns, could be different function?
    isbns = set()
    if isbn == '':
        url = 'https://www.cheapesttextbooks.com/IM/?keyval=' + title
        response = requests.get(url)
        soup = bs(response.content, "html.parser")
        tags = soup.find_all('dd', {"class": "isbn10"})
        for tag in tags:
            isbns.add(tag.find('a').text)
    else:
        isbns.add(isbn)
    
    books = set()
    for isbn in isbns:
        url = 'https://www.cheapesttextbooks.com/IM/?keyval=' +isbn + '&submit=1'
        response = requests.get(url)
        soup = bs(response.content, "html.parser")
        title = soup.find('h1', {'itemprop': 'name'})
        author = soup.find('dd', {'class': 'authors first'})
        pic = soup.find('img', {'class': 'medium'})
        table = soup.find('table', {'class': 'h price-table'})
        prices = table.find_all("div", {"class": "g30"})
        links = table.find_all('a', {'class': 'multi-line-button stopProp'})
        print(len(prices))
        [print(len(links))]
        for i in range(len(prices)):
            books.add(Book(title.find('a').text,
                      author.text,
                      prices[i].find('span', {'class': 'price'}).text,
                      links[i]['href'],
                      pic['src']))
        return books
