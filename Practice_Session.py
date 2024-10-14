from recommendations import *
import os

path = os.getcwd()
print(path)
#  critics = {User-ID:{ISBN:Book-Rating,.....},...}
File1 = open(f"{path}\BX-Book-Ratings.csv", 'r')
File2 = open(f"{path}\BX-Books.csv", 'r')

book_critics = {}
File1.readline()
for line in File1.readlines():
    Kullanici = line[0:-1].split(';')[0].strip('"')
    ISBN = line[0:-1].split(';')[1].strip('"')
    puan = int(line[0:-1].split(';')[2].strip('"')) / 2
    book_critics.setdefault(Kullanici, {})
    book_critics[Kullanici][ISBN] = puan

print(book_critics)
kitablar = getRecommendations(book_critics, '277042', sim_distance)
top = topMatches(book_critics, '277042', 3, sim_distance)

book_critics_tf = transformPrefs(book_critics)
sim = calculateSimilarItems(book_critics, 3)
kitablar2 = getRecommendedItems(book_critics, sim, '277042')
print(kitablar2)
print(book_critics_tf)
book_details = {}
File2.readline()
for line in File2.readlines():
    ISBN = line[0:-1].split(';')[0].strip('"')
    Book_Title = line[0:-1].split(';')[1].strip('"')
    Book_Author = line[0:-1].split(';')[2].strip('"')
    Year_Of_Publication = line[0:-1].split(';')[3].strip('"')
    Publisher = line[0:-1].split(';')[4].strip('"')
    Image_URL_S = line[0:-1].split(';')[5].strip('"')
    Image_URL_M = line[0:-1].split(';')[6].strip('"')
    Image_URL_L = line[0:-1].split(';')[7].strip('"')
    book_details.setdefault(ISBN, [])
    book_details[ISBN].extend(
        [Book_Title, Book_Author, Year_Of_Publication, Publisher, Image_URL_S, Image_URL_M, Image_URL_L])

print(book_details['8445072919'])

book_critics_Title = {}
for key in book_critics:
    book_critics_Title.setdefault(key, {})
    for icerdeki_key in book_critics[key]:
        try:
            title = book_details[icerdeki_key][0]
            book_critics_Title[key][title] = book_critics[key][icerdeki_key]
        except:
            book_critics_Title[key][icerdeki_key] = book_critics[key][icerdeki_key]
print(book_critics_Title)

print(getRecommendations(book_critics_Title, '277042', sim_distance)[0:3])

File1.close()
File2.close()
