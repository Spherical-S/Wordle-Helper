from tkinter import *

def startGuess():
    a = []
    f = open("guesslist.txt", 'r')
    lines = f.readlines()
    f.close()
    for i in lines:
        word = i[0:5]
        a.append(word)
    return a


def startWords():
    a = []
    f = open("wordlist.txt", 'r')
    lines = f.readlines()
    f.close()
    for i in lines:
        word = i[0:5]
        a.append(word)
    return a


def limit_entry(str_var, length):
    def callback(str_var):
        c = str_var.get()[0:length]
        str_var.set(c)
    str_var.trace("w", lambda name, index, mode, str_var=str_var: callback(str_var))


def updateGuesses(availableguesses, cantUse):
    a = []
    for word in availableguesses:
        count = 0
        for char in word:
            count += 1
            if char in cantUse:
                break
            if count == 5:
                a.append(word)
    a2 = []
    for word in a:
        temp = {}
        temp[word[0:1]] = ""
        temp[word[1:2]] = ""
        temp[word[2:3]] = ""
        temp[word[3:4]] = ""
        temp[word[4:5]] = ""
        if len(temp) == 5:
            a2.append(word)
    return a2


def updateWords(availablewords, cantUse2, mustUse, placement):
    a = []
    for word in availablewords:
        count = 0
        for char in word:
            count += 1
            if char in cantUse2:
                break
            if count == 5:
                a.append(word)
    a2 = []
    for i in a:
        valid = True
        temp = {i[0:1], i[1:2], i[2:3], i[3:4], i[4:5]}
        for j in mustUse:
            if j not in temp:
                valid = False
        if valid:
            a2.append(i)
    a3 = []
    if len(placement) != 0:
        for i in a2:
            valid = False
            for j in range(len(placement)):
                if i[placement[j][1] - 1:placement[j][1]] != placement[j][0]:
                    valid = False
                    break
                else:
                    valid = True
            if valid:
                a3.append(i)
        return a3
    return a2


def stringify(a_list):
    a_string = ""
    if len(a_list) <= 23:
        for i in a_list:
            a_string += (i + "\n")
    else:
        for i in range(23):
            a_string += (a_list[i] + "\n")
    return a_string

def button_update(self, row, column):
    if buttons_list[row][column]['bg'] == 'grey':
        entrys_list[row][column]['bg'] = 'yellow'
        buttons_list[row][column]['bg'] = 'yellow'
    elif buttons_list[row][column]['bg'] == 'yellow':
        entrys_list[row][column]['bg'] = 'green'
        buttons_list[row][column]['bg'] = 'green'
    elif buttons_list[row][column]['bg'] == 'green':
        entrys_list[row][column]['bg'] = '#6B6A6A'
        buttons_list[row][column]['bg'] = 'grey'


def submit(self):
    global availablewords
    global availableguesses
    global string_availableguesses
    global string_availablewords
    global currentRow
    all_entries_filled = True
    for i in range(5):
        entry = entrys_list[currentRow][i].get()
        if entry == '':
            error_label['text'] = "Please fill all entry boxes!"
            all_entries_filled = False
            break
        elif not entry.isalpha():
            error_label['text'] = "Only letters please!"
            all_entries_filled = False
            break
    if all_entries_filled:
        error_label['text'] = ""
        for i in range(5):
            letter = entrys_list[currentRow][i].get().lower()
            if buttons_list[currentRow][i]['bg'] == 'grey':
                cantUse[letter] = ''
                cantUse2[letter] = ''
            elif buttons_list[currentRow][i]['bg'] == 'yellow':
                cantUse[letter] = ''
                mustUse[letter] = ''
            else:
                cantUse[letter] = ''
                mustUse[letter] = ''
                placement[len(placement)] = [letter, i+1]
        availableguesses = updateGuesses(availableguesses, cantUse)
        availablewords = updateWords(availablewords, cantUse2, mustUse, placement)
        string_availableguesses = stringify(availableguesses)
        string_availablewords = stringify(availablewords)
        guesses_label['text'] = string_availableguesses
        words_label['text'] = string_availablewords
        if currentRow != 5:
            for i in range(5):
                entrys_list[currentRow][i]['state'] = "disabled"
                buttons_list[currentRow][i]['state'] = "disabled"
                entrys_list[currentRow+1][i]['state'] = "normal"
                buttons_list[currentRow+1][i]['state'] = "normal"
            currentRow += 1
        else:
            for i in range(5):
                entrys_list[5][i]['state'] = "disabled"
                buttons_list[5][i]['state'] = "disabled"


cantUse = {}
cantUse2 = {}
mustUse = {}
placement = {}
currentRow = 0
availableguesses = startGuess()
availablewords = startWords()
string_availableguesses = stringify(availableguesses)
string_availablewords = stringify(availablewords)

window = Tk()
window.geometry("800x600")
window.title("Wordle Helper")
icon = PhotoImage(file="icon.png")
window.iconphoto(True, icon)
window.config(background="grey")
window.resizable(True, True)
next_guess_label = Label(window, text="Next guesses to\ngain more data:", font=('Arial', 15), bg="grey")
potential_correct_label = Label(window, text="Potential correct\nguesses:", font=('Arial', 15), bg="grey")
submit_button = Button(text="Submit", bg="white", font=('Arial', 25), command=lambda self=window: submit(self))
error_label = Label(text='', bg='grey', fg='red', font=('Arial', 15))
guesses_label = Label(text=string_availableguesses, bg='grey', font=('Arial', 15))
words_label = Label(text=string_availablewords, bg='grey', font=('Arial', 15))
entrys_list = []
buttons_list = []
for row in range(6):
    temp = []
    entrys_list.append(temp)
    for column in range(5):
        entry_limiter = StringVar()
        limit_entry(entry_limiter, 1)
        temp = Entry(window, font=('Arial', 30), bg="#6B6A6A", width=2, textvariable=entry_limiter, state='readonly')
        entrys_list[row].append(temp)

for row in range(6):
    temp = []
    buttons_list.append(temp)
    for column in range(5):
        temp = Button(window, bg="grey", height=1, width=5, state="disabled", command=lambda row=row, column=column, self=window: button_update(self, row, column))
        buttons_list[row].append(temp)
for i in range(5):
    entrys_list[0][i]['state'] = "normal"
    buttons_list[0][i]['state'] = "normal"

y = -70
for row in range(6):
    x = 200
    y += 80
    for column in range(5):
        x += 70
        entrys_list[row][column].place(x=x, y=y)
        buttons_list[row][column].place(x=x+1, y=y+51)

next_guess_label.place(x=5, y=5)
potential_correct_label.place(x=650, y=5)
submit_button.pack(side='bottom', pady=10)
error_label.pack(side='bottom')
guesses_label.place(x=50, y=50)
words_label.place(x=700, y=50)

window.mainloop()