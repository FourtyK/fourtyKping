from pythonping import ping
# ИМПОРТ PP
import requests
# ИМПОРТ REQEUSTS
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import ttk
# ИМПОРТ НУЖНЫХ РАЗДЕЛОВ TKINTER
import json


def mean(numbers):  # ФУНКИЦИЯ НА ПОДСЧЁТ СРЕДНЕГО ЧИСЛА
    return float(sum(numbers)) / max(len(numbers), 1)


def on_closing():
    if messagebox.askokcancel("Закрыть", "Вы точно хотите закрыть окно?"):
        root.destroy()


def open_info_window():
    with open('texts.json', 'r', encoding='UTF-8') as file:
        texts = json.load(file)

    window = Tk()
    window.title('Справка')
    window.geometry('400x400')
    x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2 - 100
    y = (window.winfo_screenheight() - window.winfo_reqheight()) / 2 - 100
    window.wm_geometry("+%d+%d" % (x, y))
    window.configure(bg='#89b0f0')
    Label(window, text='Как пользоваться', anchor='center', font='Arial 14', fg='black', bg='#89b0f0').pack()
    Label(window, text=texts['instructions1'], font='Arial, 12', fg='black', bg='#89b0f0').pack()
    Label(window, text=texts['instructions2'], font='Arial, 12', fg='black', bg='#89b0f0').pack()
    Label(window, text='\n\n\nЕсли вы будете делать что-то не то,\nто будете получать ошибки)', font='Arial 11', fg='black', bg='#89b0f0').pack()
    Label(window, text='Pinger made by FourtyK', font='Arial, 16', fg='black', bg='#89b0f0').pack(side='bottom')


def address_formatting(address):
    if not address.startswith('http'):
        response = requests.get(f'https://{address}')
    else:
        response = requests.get(address)

    if address.startswith('http://'):
        address = address[7:]
    elif address.startswith('https://'):
        address = address[8:]

    return (address, response)


def how_many_pings(pings_number):
    if not pings_number:
        pings_number = 4
    else:
        if pings_number[0].isdigit():
            if pings_number.isdigit():
                pings_number = int(pings_number)
            elif pings_number >= 800:
                pings_number = 4
            else:
                pings_number = 4
        else:
            messagebox.showerror('Ошибка', 'В вводе количества запросов есть буквы, или другие символы!')

    return pings_number


def get_info_from_ip(address, pings_number):
    ping_list = []

    for _ in range(int(pings_number)):
        res = ping(address, size=10, count=1)
        ping_list.append(res.rtt_avg_ms)

    average_ping = round(mean(ping_list), 1)  # ПОИСК СРЕДНЕГО ПИНГА

    info = [average_ping, ping_list]
    return info


def get_info_from_address(address, pings_number):
    ping_list = []

    address_info = address_formatting(address)
    address, response = address_info

    for _ in range(int(pings_number)):
        res = ping(address, size=10, count=1)
        ping_list.append(res.rtt_avg_ms)

    average_ping = round(mean(ping_list), 1)  # ПОИСК СРЕДНЕГО ПИНГА

    info = [average_ping, ping_list, response]
    return info


def file_save(*args):
    ping_list = args[2]
    file_name = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"),
                                                ("HTML files", "*.html; *.htm"),
                                                ("All files", "*.*")))
    f = open(file_name, 'w')
    if args[0] is None:
        average_ping = args[1]
        f.write(f"Средний пинг: {average_ping}\n")
    else:
        response, average_ping = args[0], args[1]
        f.write(f"Состояние: {response.reason}\nКод состояния: {response.status_code}\nСредний пинг: {average_ping}\n")
    f.write(str(ping_list))
    f.close()


def check(*args):
    pings_number = pings.get()  # ПОЛУЧЕНИЕ КОЛ-ВА ПИНГОВ
    address = address_edit.get()  # ПОЛУЧЕНИЕ АДРЕСА

    pings_number = how_many_pings(pings_number)

    try:
        if address[0].isalpha():
            info = get_info_from_address(address, pings_number)
            average_ping, ping_list, response = info[0], info[1], info[2]
            answer = messagebox.askyesno(title="Вопрос", message=f"Сохранить данные?\n\nСостояние: {response.reason}\nКод состояния: {response.status_code}\nСредний пинг: {average_ping}")
            if answer is True:
                file_save(response, average_ping, ping_list)

        elif address[0].isdigit():
            info = get_info_from_ip(address, pings_number)
            average_ping, ping_list = info[0], info[1]
            answer = messagebox.askyesno(title="Вопрос", message=f"Сохранить данные?\n\nСредний пинг: {average_ping}")
            if answer is True:
                file_save(None, average_ping, ping_list)
    except IndexError:
        messagebox.showerror('Ошибка', 'Вы не указали что мы будем пинговать!')


def window_start():
    root = Tk()

    root.title("Пинговалка")
    root.geometry("480x250")
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2 - 140
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    root.configure(bg='#f0cd89')

    return root


root = window_start()

Label(root, text="Что пингуем?", font='Arial 12', fg='black', bg='#f0cd89').pack()

address_edit = ttk.Entry(root, width=40)
address_edit.bind('<Return>', check)
address_edit.pack()

Label(root, text="\nСколько запросов отправляем?", font='Arial 12', fg='black', bg='#f0cd89').pack()

pings = ttk.Entry(root, width=40)
pings.bind('<Return>', check)
pings.pack()

Label(root, text='', bg='#f0cd89').pack()
ttk.Button(root, text='Принять', command=check).place(x=190, y=200, height=40, width=100)

Label(root, text='', bg='#f0cd89').pack()
ttk.Button(root, text='Справка', command=open_info_window).place(x=370, y=200, height=40, width=100)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
