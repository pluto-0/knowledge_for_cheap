import googleBooks
import pprint

book = googleBooks.Book('9781501142970')
pprint.pprint(book.getbookInfo)