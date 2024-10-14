import tkinter as tk
from tkinter import messagebox
from math import sqrt

critics = {
    'Claudia Puig': {'Just My Luck': 3.0, 'Snakes on a Plane': 3.5, 'Superman Returns': 4.0, 'The Night Listener': 4.5,
                     'You, Me, and Dupree': 2.5},
    'Gene Seymour': {'Just My Luck': 1.5, 'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Superman Returns': 5.0,
                     'The Night Listener': 3.0, 'You, Me, and Dupree': 3.5},
    'Jack Mathews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Superman Returns': 5.0,
                     'The Night Listener': 3.0, 'You, Me, and Dupree': 3.5},
    'Lisa Rose': {'Just My Luck': 3.0, 'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Superman Returns': 3.5,
                  'The Night Listener': 3.0, 'You, Me, and Dupree': 2.5},
    'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5,
                         'The Night Listener': 4.0},
    'Mick LaSalle': {'Just My Luck': 2.0, 'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Superman Returns': 3.0,
                     'The Night Listener': 3.0, 'You, Me, and Dupree': 2.0},
    'Toby': {'Snakes on a Plane': 4.5, 'Superman Returns': 4.0, 'You, Me, and Dupree': 1.0},
    'Ali': {'Just My Luck': 2.0, 'Snakes on a Plane': 2.5, 'Superman Returns': 2.5, 'The Night Listener': 5.0}
}


def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    if len(si) == 0:
        return 0
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2) for item in si])
    return 1 / (1 + sqrt(sum_of_squares))


def sim_pearson(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    n = len(si)
    if n == 0:
        return

    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    return num / den


def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]


def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        if other == person:
            continue
        sim = similarity(prefs, person, other)
        if sim <= 0:
            continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                simSums.setdefault(item, 0)
                simSums[item] += sim
    rankings = [(total / simSums[item], item) for item, total in totals.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


# Tkinter UI
def recommend_books():
    person = person_entry.get()
    if person == "":
        messagebox.showwarning("Uyarı", "Lütfen bir kişi adı girin.")
        return

    # Öneri sistem fonksiyonunu çağırarak sonuçları al
    recommendations = getRecommendations(critics, person)

    # Sonuçları göster
    recommendation_text.delete("1.0", tk.END)
    for rank, book in recommendations:
        recommendation_text.insert(tk.END, f"{book}: {rank}\n")


# Tkinter arayüzü oluşturma
window = tk.Tk()
window.title("Kitap Öneri Sistemi")
window.geometry("400x400")
window.config(bg="#ffa6ff")

# Kişi adı giriş alanı
person_label = tk.Label(text="Kişi Adı :",font="Verdana 12",bg="#ffa6ff")
person_label.pack()
person_entry = tk.Entry(window,width="25")
person_entry.place(x=115,y=30)

# Öneri butonu
recommend_button = tk.Button(window, text="Kitap Öner", command=recommend_books,bg="#ffa6ff")
recommend_button.place(x=145,y=62)
recommend_button.config(height=2,width=12)

# Öneri sonuçları metin alanı
recommendation_text = tk.Text(window, width=47, height=15)
recommendation_text.place(x=10,y=120)

# Tkinter arayüzünü çalıştırma
window.mainloop()
