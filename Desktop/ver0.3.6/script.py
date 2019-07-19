import requests

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import ttk


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


def check(*args):
    adress = adress_edit.get()
    pings_number = int(pings.get())

    if adress.startswith("http"):
        ping_list = []

        for _ in range(pings_number):
            response = requests.get(adress)

            ping = str(response.elapsed)
            ping = ping[8:-4]
            ping_list.append(int(ping))

        average_ping = mean(ping_list)

        answer = messagebox.askyesno(title="Вопрос", message=f"Сохранить данные?\n\nСостояние: {response.reason}\nКод состояния: {response.status_code}\nСредний пинг: {average_ping}")
        if answer is True:
            file_name = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"),
                                                        ("HTML files", "*.html; *.htm"),
                                                        ("All files", "*.*")))
            f = open(file_name, 'w')
            f.write(f"Состояние: {response.reason}\nКод состояния: {response.status_code}\nСредний пинг: {average_ping}\n")
            f.write(str(ping_list))
            f.close()

        root.destroy()

    else:
        messagebox.showerror("Ошибка", "Должен быть введён адрес сайта")


root = Tk()

root.title("Пинговалка")
root.geometry("500x250")
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2 - 140
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.wm_geometry("+%d+%d" % (x, y))
root.configure(bg='#f0cd89')

Label(root, text='Введите адрес сайта', height=2, fg='black', bg='#f0cd89').pack()
Label(root, text="Примечание: адрес должен быть вида http://...", fg='gray', bg='#f0cd89').pack()

adress_edit = ttk.Entry(root, width=40)
adress_edit.bind('<Return>', check)
adress_edit.pack()

Label(root, text="\nВведите количество запросов", fg='black', bg='#f0cd89').pack()
Label(root, text="Примечание: для получения информации мин.число: 1", fg='gray', bg='#f0cd89').pack()

pings = ttk.Entry(root, width=10)
pings.bind('<Return>', check)
pings.pack()

Label(root, text='', bg='#f0cd89').pack()
ttk.Button(root, text='Принять', command=check).place(x=212, y=210)

root.mainloop()
