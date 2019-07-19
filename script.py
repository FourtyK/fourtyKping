import requests
# ИМПОРТ REQEUSTS
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import ttk
# ИМПОРТ НУЖНЫЕ РАЗДЕЛОВ TKINTER

numbers_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


def file_save(response, average_ping, ping_list):
    file_name = fd.asksaveasfilename(filetypes=(("TXT files", "*.txt"),
                                                ("HTML files", "*.html; *.htm"),
                                                ("All files", "*.*")))
    f = open(file_name, 'w')
    f.write(f"Состояние: {response.reason}\nКод состояния: {response.status_code}\nСредний пинг: {average_ping}\n")
    f.write(str(ping_list))
    f.close()


def mean(numbers):  # ФУНКИЦИЯ НА ПОДСЧЁТ СРЕДНЕГО ЧИСЛА
    return float(sum(numbers)) / max(len(numbers), 1)


def check(*args): 
    pings_number = pings.get()  # ПОЛУЧЕНИЕ КОЛ-ВА ПИНГОВ
    adress = adress_edit.get()  # ПОЛУЧЕНИЕ АДРЕСА
    if [i in numbers_list for i in pings_number]:
        pings_number = int(pings_number)
    else:
        pings_number = 4

    if adress.startswith("http"):  # ПРОВЕРКА, С ЧЕГО НАЧИНАЕТСЯ АДРЕС САЙТА
        ping_list = []
    
        for _ in range(int(pings_number)): 
            response = requests.get(adress)  # ОТПРАВЛЕНИЕ ЗАПРОСА И ПОЛУЧЕНИЕ ИНФОРМАЦИИ

            ping = str(response.elapsed)
            ping_list.append(int(ping[8:-4])) 

        average_ping = round(mean(ping_list), 1)  # ПОИСК СРЕДНЕГО ПИНГА

        # ВКЛЮЧЕНИЕ ВСПЛЫВАЮЩЕГО ОКНА С ВОПРОСОМ О СОХРАНЕНИИ ДАННЫХ В ФАЙЛ
        answer = messagebox.askyesno(title="Вопрос", message=f"Сохранить данные?\n\nСостояние: {response.reason}\nКод состояния: {response.status_code}\nСредний пинг: {average_ping}")
        # ЕСЛИ ОТВЕТ БЫЛ ДА, ТО ОТКРЫВАЕТСЯ ОКНО СОХРАНЕНИЯ
        if answer is True:
            file_save(response, average_ping, ping_list)

        root.destroy()

    else:
        messagebox.showerror("Ошибка", "Должен быть введён адрес сайта")


root = Tk()

root.title("Пинговалка")
root.geometry("480x250")
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2 - 140
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.wm_geometry("+%d+%d" % (x, y))
root.configure(bg='#f0cd89')

Label(root, text='Введите адрес сайта', font='Arial 12', fg='black', bg='#f0cd89').pack(fill='both')
Label(root, text="Примечание: адрес должен быть вида http://...", fg='gray', bg='#f0cd89').pack()

adress_edit = ttk.Entry(root, width=40)
adress_edit.bind('<Return>', check)
adress_edit.pack()

Label(root, text="\nВведите количество запросов", font='Arial 12', fg='black', bg='#f0cd89').pack()
Label(root, text="Примечание:\nДля получения информации мин.число: 1.\nПо стандарту: 4", fg='gray', bg='#f0cd89').pack()

pings = ttk.Entry(root, width=40)
pings.bind('<Return>', check)
pings.pack()

Label(root, text='', bg='#f0cd89').pack()
ttk.Button(root, text='Принять', command=check).place(x=190, y=200, height=40, width=100)

root.mainloop()
