from tkinter import *
from tkinter import messagebox, ttk, filedialog, colorchooser
import PIL
from PIL import ImageTk, Image, ImageDraw
import os
import datetime
import time
from random import *
import sys
from threading import Thread
from pyautogui import screenshot
from googletrans import Translator
import ctypes
import re
import string
import pathlib
import calendar

expression = ""
stop = False
startFolder = os.getcwd()
previousText = ''
path = ''
global month, year
days = []
now = datetime.datetime.now()
year = now.year
month = now.month




def updateRoot(imagen):
    try:
        pilImage = Image.open(imagen)
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        image = ImageTk.PhotoImage(pilImage.resize((w, h)))
        canvas.itemconfig(imgbox, image=image)
        canvas.image = image
    except Exception:
        pass


def updateImg():
    global stop
    stop = True
    file_path = filedialog.askopenfilename(title='Выбор файла', filetypes=(
        ('Изображения (*.png)', '*.png'), ('Все файлы', '*.*')))
    if file_path:
        updateRoot(file_path)


def ShowImg():
    global stop
    stop = False
    # (startFolder + '\icon.ico')
    bgs = os.listdir(startFolder + '/background')
    while not stop:
        for filename in bgs:
            Thread(target=updateRoot(startFolder + '/background/' + filename)).start()
            time.sleep(5)


def add_folder():
    Button(root, width=70, height=70, image=imgFolder, command=folder).place(x=x, y=y)
    canvas.pack(side="top", fill="both", expand=True)
    text_canvas = canvas.create_text(x+37, y+90)
    canvas.itemconfig(text_canvas, text="Папка", font=("Arial 15 bold"), fill='white')


def folder():
    def on_select(event):
        def open_file_txt():
            file_path = lstt
            if file_path:
                notepad(file_path)

        lstt = os.getcwd() + '\\' + lst.get(lst.curselection())
        filename, file_extension = os.path.splitext(lstt)
        if file_extension == '.txt':
            open_file_txt()
        elif file_extension == '.py':
            open_file_txt()

        try:
            os.chdir(lstt)
            files = os.listdir()
            addressBar['state'] = "normal"
            addressBar.delete(0, END)
            addressBar.insert(0, lstt)
            addressBar['state'] = "readonly"
            lst.delete(0, END)

            for i in files:
                lst.insert(END, i)
        except Exception:
            pass

    def back_btn():
        try:
            beginning.insert(0, os.getcwd())
            os.chdir('..')
            files = os.listdir()

            addressBar['state'] = "normal"
            addressBar.delete(0, END)
            addressBar.insert(0, os.getcwd())
            addressBar['state'] = "readonly"

            lst.delete(0, END)

            for i in files:
                lst.insert(END, i)
        except Exception:
            pass

    def next_btn():
        try:
            os.chdir(beginning[0])
            beginning.pop(0)
            files = os.listdir()

            addressBar['state'] = "normal"
            addressBar.delete(0, END)
            addressBar.insert(0, os.getcwd())
            addressBar['state'] = "readonly"

            lst.delete(0, END)

            for i in files:
                lst.insert(END, i)
        except Exception:
            pass

    beginning = []

    window = Toplevel(root)
    window.attributes("-topmost", True)
    window.title('Папка')
    window.geometry('500x400')
    window.resizable(0, 0)
    window.iconbitmap(startFolder + '\wikus.ico')

    addressBar = Entry(window)
    addressBar.insert(0, startFolder)
    addressBar['state'] = "readonly"
    addressBar.place(relwidth=0.80, x=50, y=5)
    f = Frame(window)

    btnNext = Button(window, text='>>', font='Arial 6 bold', command=next_btn)
    btnNext.place(x=28, y=5)

    btnBack = Button(window, text='<<', font='Arial 6 bold', command=back_btn)
    btnBack.place(x=5, y=5)

    scrollbar = Scrollbar(f)
    scrollbar.pack(side=RIGHT, fill=Y)

    files = os.listdir()
    f.place(y=30, relwidth=1, relheight=0.95)
    lst = Listbox(f, font='Arial 13 bold', yscrollcommand=scrollbar.set, width=40)
    lst.pack(fill=BOTH, expand=1)
    scrollbar.config(command=lst.yview)

    for i in files:
        lst.insert(END, i)

    lst.bind('<<ListboxSelect>>', on_select)

    if window.quit:

        os.chdir(startFolder)
        files = os.listdir()

        addressBar.delete(0, END)
        addressBar.insert(0, os.getcwd())

        lst.delete(0, END)

        for i in files:
            lst.insert(END, i)
    window.mainloop()


# Нажатие на ПКМ
def popup(event):
    global x, y
    x = event.x
    y = event.y
    menu.post(event.x_root, event.y_root)


def notepad(file_path):
    window = Toplevel(root)
    window.attributes("-topmost", True)
    window.title('Блокнот')
    window.resizable(0, 0)
    window.geometry('600x700')
    window.iconbitmap(startFolder + '\wikus.ico')
    main_menu = Menu(window)
    window.config(menu=main_menu)

    # Изменение тем
    def chenge_theme(theme):
        t['bg'] = view_colors[theme]['text_bg']
        t['fg'] = view_colors[theme]['text_fg']
        t['insertbackground'] = view_colors[theme]['cursor']
        t['selectbackground'] = view_colors[theme]['select_bg']

    # Изменение шрифтов
    def chenge_fonts(fontss):
        t['font'] = fonts[fontss]['font']

    # Выход
    def notepad_exit():
        answer = messagebox.askokcancel('Выход', 'Вы точно хотите выйти?')
        if answer:
            window.destroy()

    def open_file():
        file_path = filedialog.askopenfilename(title='Выбор файла', filetypes=(
            ('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*')))
        if file_path:
            t.delete('1.0', END)
            t.insert('1.0', open(file_path, encoding='utf-8').read())

    def save_file():
        file_path = filedialog.asksaveasfilename(
            filetypes=(('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*')))
        f = open(file_path + '.txt', 'w', encoding='utf-8')
        text = t.get('1.0', END)
        f.write(text)
        f.close()

    # Файл
    file_menu = Menu(main_menu, tearoff=0)
    file_menu.add_command(label='Открыть', command=open_file)
    file_menu.add_command(label='Сохранить', command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label='Закрыть', command=notepad_exit)
    window.config(menu=file_menu)

    # Вид
    view_menu = Menu(main_menu, tearoff=0)
    view_menu_sub = Menu(view_menu, tearoff=0)
    font_menu_sub = Menu(view_menu, tearoff=0)
    view_menu_sub.add_command(label='Тёмная', command=lambda: chenge_theme('dark'))
    view_menu_sub.add_command(label='Светлая', command=lambda: chenge_theme('light'))
    view_menu.add_cascade(label='Тема', menu=view_menu_sub)

    font_menu_sub.add_command(label='Arial', command=lambda: chenge_fonts('Arial'))
    font_menu_sub.add_command(label='Comic Sans MS', command=lambda: chenge_fonts('CSMS'))
    font_menu_sub.add_command(label='Times New Roman', command=lambda: chenge_fonts('TNR'))
    view_menu.add_cascade(label='Шрифт...', menu=font_menu_sub)
    window.config(menu=view_menu)

    # Добавление списков меню
    main_menu.add_cascade(label='Файл', menu=file_menu)
    main_menu.add_cascade(label='Вид', menu=view_menu)
    window.config(menu=main_menu)

    f_text = Frame(window)
    f_text.pack(fill=BOTH, expand=1)

    # Темы
    view_colors = {
        'dark': {
            'text_bg': 'black', 'text_fg': 'lime', 'cursor': 'brown', 'select_bg': '#8D917A'
        },
        'light': {
            'text_bg': 'white', 'text_fg': 'black', 'cursor': '#A5A5A5', 'select_bg': '#FAEEDD'
        }
    }

    # Шрифты
    fonts = {
        'Arial': {
            'font': 'Arial 14 bold'
        },
        'CSMS': {
            'font': ('Comic Sans MS', 14, 'bold')
        },
        'TNR': {
            'font': ('Times New Roman', 14, 'bold')
        }
    }

    # Текстовое поле
    t = Text(f_text,
             bg=view_colors['dark']['text_bg'],
             fg=view_colors['dark']['text_fg'],
             padx=10,
             pady=10,
             wrap=WORD,
             insertbackground=view_colors['dark']['cursor'],
             selectbackground=view_colors['dark']['select_bg'],
             spacing3=10,
             width=30,
             font='Arial 14 bold')
    t.pack(expand=1, fill=BOTH, side=LEFT)

    # Скроллбар
    scroll = Scrollbar(f_text, command=t.yview)
    scroll.pack(fill=Y, side=LEFT)
    t.config(yscrollcommand=scroll.set)

    if file_path:
        t.insert('1.0', open(file_path, encoding='utf-8').read())


def addNotepad():
    Button(canvas, width=70, height=70, image=imgNotepad, command=lambda: notepad(0)).place(x=x, y=y)
    canvas.pack(side="top", fill="both", expand=True)
    text_canvas = canvas.create_text(x + 37, y + 90)
    canvas.itemconfig(text_canvas, text="Блокнот", font=("Arial 15 bold"), fill='white')


brush_size = 1
color = 'black'
x = 0
y = 0


def addPaint():
    def paint():
        def pour():
            canv['bg'] = color
            draw_img.rectangle((0, 0, 1280, 720), width=0, fill=color)

        def clear_canv():
            canv.delete('all')
            draw_img.rectangle((0, 0, 1280, 720), width=0, fill='white')
            canv['bg'] = 'white'

        def draw(event):
            x1, y1 = (event.x - brush_size), (event.y - brush_size)
            x2, y2 = (event.x + brush_size), (event.y + brush_size)
            canv.create_oval(x1, y1, x2, y2, fill=color, width=0)
            draw_img.ellipse((x1, y1, x2, y2), fill=color, width=0)

        def square():
            canv.create_rectangle(
                x, y, x + brush_size, y + brush_size, fill=color, width=0)
            draw_img.polygon((x, y, x + brush_size, y, x + brush_size, y + brush_size, x, y + brush_size), fill=color)

        def circle():
            canv.create_oval(
                x, y, x + brush_size, y + brush_size, fill=color, width=0)
            draw_img.ellipse((x, y, x + brush_size, y + brush_size), fill=color)

        def onChoose():
            global color
            (rgb, hx) = colorchooser.askcolor()
            color = hx
            color_lab['bg'] = hx

        def select(value):
            global brush_size
            brush_size = int(value)

        def save_img():
            filename = f'image_{randint(0, 10000)}.png'
            image1.save(filename)

        def popup(event):
            global x, y
            x = event.x
            y = event.y
            menu.post(event.x_root, event.y_root)

        window = Tk()
        window.attributes('-topmost', True)
        window.title('Paint')
        window.resizable(0, 1)
        window.geometry('1280x720')
        window.iconbitmap(startFolder + '\wikus.ico')

        window.columnconfigure(6, weight=1)
        window.rowconfigure(2, weight=1)

        canv = Canvas(window, bg='white')
        canv.grid(row=2, column=0, columnspan=7, padx=5, pady=5, sticky=E + W + S + N)

        canv.bind('<B1-Motion>', draw)
        canv.bind("<Button-3>", popup)

        menu = Menu(tearoff=0)
        menu.add_command(label="Квадрат", command=square)
        menu.add_command(label="Круг", command=circle)

        image1 = PIL.Image.new('RGB', (1280, 640), 'white')

        draw_img = ImageDraw.Draw(image1)

        parameters_lab = Label(window, text='Параметры: ')
        parameters_lab.grid(row=0, column=0, padx=6)

        test_btn = Button(window, text='Выбрать цвет', width=11, command=onChoose)
        test_btn.grid(row=0, column=1, padx=6)

        color_lab = Label(window, bg=color, width=10)
        color_lab.grid(row=0, column=2, padx=6)

        v = DoubleVar(value=1)
        scale = Scale(window, variable=v, from_=1, to=100, orient=HORIZONTAL, command=select)
        scale.grid(row=0, column=3, padx=6)

        action_lab = Label(window, text='Действия: ')
        action_lab.grid(row=1, column=0, padx=6)

        pour_btn = Button(window, text='Заливка', width=10, command=pour)
        pour_btn.grid(row=1, column=1)

        clear_btn = Button(window, text='Очистить', width=10, command=clear_canv)
        clear_btn.grid(row=1, column=2)

        save_btn = Button(window, text='Сохранить', width=10, command=save_img)
        save_btn.grid(row=1, column=6)
        window.mainloop()

    Button(canvas, width=70, height=70, image=imgPaint, command=paint).place(x=x, y=y)
    canvas.pack(side="top", fill="both", expand=True)
    text_canvas = canvas.create_text(x+37, y+90)
    canvas.itemconfig(text_canvas, text="Paint", font=("Arial 15 bold"), fill='white')


def tick():
    watch.after(1000, tick)
    watch['text'] = "{}  {}.".format(time.strftime("%H:%M:%S"), datetime.date.today())


def stop_pz():
    watch.pack_forget()
    btn.place_forget()
    btn_2.place_forget()


def start_pz():
    watch.pack(side=BOTTOM, anchor=SE)
    Thread(target=tick).start()

    def screen():
        img = screenshot()
        img.save(r"screen.png")
        messagebox.showinfo('Оповещение', 'Скриншот сделан!')

    btn['command'] = screen
    btn_2.place(anchor=S, bordermode=OUTSIDE, relx=.01, rely=1)
    btn.place(anchor=S, bordermode=OUTSIDE, relx=.5, rely=1)


def quit_os():
    global stop
    stop = True
    root.quit()


def addAnagrammi():
    def anagrammi():
        def start():
            global word, guessEntry, wordMix
            btnYes.place_forget()
            btnNo.place_forget()
            btn['text'] = 'Проверить'
            btn['width'] = 10
            btn['command'] = check
            btn.place(relx=0.5, y=130, anchor=CENTER)
            word = choice(words)
            wordMix = sample(word, k=len(word))
            label1['text'] = 'Загаданное слово: ' + ''.join(wordMix)
            guessEntry = Entry(window, font='Arial 15 bold')
            guessEntry.place(relx=0.5, y=80, anchor=CENTER)

        def check():
            guess = guessEntry.get()
            if guess.lower() == word:
                guessEntry.place_forget()
                btn.place_forget()
                label1['text'] = 'Вы угадали!\n Хотите ещё раз?'
                btnYes.place(x=120, y=70)
                btnNo.place(x=220, y=70)
            else:
                label1['text'] = 'Вы не угадали, попробуйте ещё раз\nЗагаданное слово: ' + ''.join(wordMix)

        def exitGame():
            answer = messagebox.askokcancel('Выход', 'Вы точно хотите выйти?')
            if answer:
                window.destroy()

        window = Toplevel(root)
        window.title('Анаграммы')
        window.resizable(0, 0)
        window.geometry('500x300')
        window.iconbitmap(startFolder + '\wikus.ico')
        words = ['анаграммы', 'мышь', 'клавиатура', 'телефон', 'программирование', 'педагогика', 'движок',
                 'фреймворк', 'исходник', 'костыль', 'лист', 'список', 'словарь']

        label1 = Label(window, text='', font='Arial 15 bold')
        label1.place(relx=0.5, y=30, anchor=CENTER)

        btn = Button(window, text='Начать', font='Arial 15 bold', width=20, command=start)
        btn.place(relx=0.5, y=90, anchor=CENTER)

        btnYes = Button(window, text='Да', font='Arial 15 bold', width=5, command=start)
        btnNo = Button(window, text='Нет', font='Arial 15 bold', width=5, command=exitGame)

    Button(canvas, width=70, height=70, image=imgAnagrammi, command=anagrammi).place(x=x, y=y)
    canvas.pack(side="top", fill="both", expand=True)
    text_canvas = canvas.create_text(x+37, y+90)
    canvas.itemconfig(text_canvas, text="Анаграммы", font=("Arial 15 bold"), fill='white')


def addCalculator():
    def calculator():
        window = Toplevel(root)
        window.geometry("350x370")
        window.resizable(0, 0)
        window.title("Калькулятор")
        window.attributes('-topmost', True)
        window.iconbitmap(startFolder + '\wikus.ico')

        def btn_click(item):
            global expression
            try:
                input_field['state'] = "normal"
                expression += item
                input_field.insert(END, item)

                if item == '=':
                    result = str(eval(expression[:-1]))
                    input_field.insert(END, result)
                    expression = ""

                input_field['state'] = "readonly"

            except ZeroDivisionError:
                input_field.delete(0, END)
                input_field.insert(0, 'Ошибка (деление на 0)')
            finally:
                pass

        def bt_clear():
            try:
                global expression
                expression = ""
                input_field['state'] = "normal"
                input_field.delete(0, END)
                input_field['state'] = "readonly"
            except:
                pass

        frame_input = Frame(window)
        frame_input.grid(row=0, column=0, columnspan=4, sticky="nsew")
        input_field = Entry(frame_input, font=('arial', 15, 'bold'), width=24)

        input_field.pack(fill=BOTH)

        buttons = (('7', '8', '9', '/', '4'),
                   ('4', '5', '6', '*', '4'),
                   ('1', '2', '3', '-', '4'),
                   ('0', '.', '=', '+', '4')
                   )

        button = Button(window, text='C', command=lambda: bt_clear())
        button.grid(row=1, column=3, sticky="nsew")
        for row in range(4):
            for col in range(4):
                Button(window, width=2, height=3, text=buttons[row][col],
                       command=lambda row=row, col=col: btn_click(buttons[row][col])).grid \
                    (row=row + 2, column=col, sticky="nsew", padx=1, pady=1)

    Button(canvas, width=70, height=70, image=imgCalculator, command=calculator).place(x=x, y=y)
    canvas.pack(side="top", fill="both", expand=True)
    text_canvas = canvas.create_text(x+37, y+90)
    canvas.itemconfig(text_canvas, text="Калькулятор", font=("Arial 15 bold"), fill='white')


clicks = 0


def addClicker():
    def clicker():
        def game():
            def countdown():
                try:
                    num_of_secs = 60
                    while num_of_secs:
                        m, s = divmod(num_of_secs, 60)
                        min_sec_format = '{:02d}:{:02d}'.format(m, s)
                        timer_label['text'] = min_sec_format
                        time.sleep(1)
                        num_of_secs -= 1

                    if num_of_secs == 0:
                        messagebox.askokcancel('Конец', 'Время закончилось, ваш результат: ' + str(clicks))
                        WindowGame.quit()
                except:
                    pass

            def randomize():
                global clicks
                x = randint(0, int(rand_btn_pos[0]) - (int(rand_btn_pos[0]) // 9))
                y = randint(0, int(rand_btn_pos[1]) - (int(rand_btn_pos[0]) // 5))
                btnClick.place(x=x, y=y)
                clicks += 1
                labelClick['text'] = str(clicks)
                labelClick.pack()

            global clicks
            clicks = 0
            WindowGame = Toplevel(window)
            WindowGame.title('Кликер')
            WindowGame.attributes('-topmost', True)
            WindowGame.iconbitmap(startFolder + '\wikus.ico')
            WindowGame.geometry(comboExample.get())

            WindowGame['bg'] = 'black'
            timer_label = Label(WindowGame, text='', font=('Comic Sans MS', 30, 'bold'), bg='black', fg='white')
            timer_label.pack()

            labelClick = Label(WindowGame, text='0', font=('Comic Sans MS', 30, 'bold'), bg='black', fg='white')
            labelClick.pack()
            frame = Frame(WindowGame, bg='black')
            frame.pack(fill=BOTH, expand=1)

            Thread(target=countdown).start()

            rand_btn_pos = comboExample.get().split('x')
            btn_width = 20
            btn_height = 8
            btnClick = Button(frame,
                              text='Click',
                              bg='lime',
                              fg='black',
                              padx=btn_width,
                              pady=btn_height,
                              font=('Comic Sans MS', 13, 'bold'),
                              command=randomize
                              )
            x = randint(0, int(rand_btn_pos[0]) - (int(rand_btn_pos[0]) // 9))
            y = randint(0, int(rand_btn_pos[1]) - (int(rand_btn_pos[0]) // 5))

            btnClick.place(x=x, y=y)

        window = Tk()
        window.title('Кликер')
        window.geometry('300x150')
        window.resizable(width=False, height=False)
        window.attributes('-topmost', True)
        window.iconbitmap(startFolder + '\wikus.ico')

        window['bg'] = 'black'
        value = StringVar()
        label_resolution = Label(window, text='Разрешение окна', bg='black', fg='lime', font=('Comic Sans MS', 17, 'bold'))
        label_resolution.pack()
        comboExample = ttk.Combobox(window, values=[
                                        '1280x720',
                                        '1024x768'], textvariable=value, state='readonly')
        comboExample.current(0)
        comboExample.pack(pady=10)

        btn = Button(window, text='Начать игру', font=('Comic Sans MS', 15, 'bold'), command=game)
        btn.pack()
        window.mainloop()

    Button(canvas, width=70, height=70, image=imgClicker, command=clicker).place(x=x, y=y)
    canvas.pack(side="top", fill="both", expand=True)
    text_canvas = canvas.create_text(x + 37, y + 90)
    canvas.itemconfig(text_canvas, text="Кликер", font=("Arial 15 bold"), fill='white')


def addKnb():
    def Knb():
        def Whyknb():
            knb = ['Камень', 'Ножницы', 'Бумага']
            labelText.configure(text=choice(knb))

        window = Tk()
        window.title('Камень ножницы бумага')
        window.geometry('500x200')
        window.resizable(width=False, height=False)
        window.attributes('-topmost', True)
        window.iconbitmap(startFolder + '\wikus.ico')
        window['bg'] = 'black'

        labelText = Label(window, text='', fg='white', font=('Comic Sans MS', 20), bg='black')
        labelText.pack(pady=20)

        stone = Button(window,
                       text='Камень',
                       font=('Comic Sans MS', 20),
                       bg='white',
                       command=Whyknb
                       )
        stone.pack(side=LEFT, padx=20)

        scissors = Button(window,
                          text='Ножницы',
                          font=('Comic Sans MS', 20),
                          bg='white',
                          command=Whyknb
                          )
        scissors.pack(side=LEFT, padx=20)

        paper = Button(window,
                       text='Бумага',
                       font=('Comic Sans MS', 20),
                       bg='white',
                       command=Whyknb
                       )
        paper.pack(side=LEFT, padx=20)

    Button(canvas, width=70, height=70, image=imgKnb, command=Knb).place(x=x, y=y)
    canvas.pack(side="top", fill="both", expand=True)
    text_canvas = canvas.create_text(x + 37, y + 90)
    canvas.itemconfig(text_canvas, text="КНБ", font=("Arial 15 bold"), fill='white')


temp = 0
after_id = ''


def addStopwatch():
    def Stopwatch():
        def tick():
            global temp, after_id
            after_id = root.after(1000, tick)
            f_temp = datetime.datetime.fromtimestamp(temp).strftime("%M:%S")
            label1.configure(text=str(f_temp))
            temp += 1

        def start_tick():
            btnStart.pack_forget()
            btnStop.pack()
            tick()

        def stop_tick():
            btnStop.pack_forget()
            btnContinue.pack()
            btnReset.pack()
            root.after_cancel(after_id)

        def continue_tick():
            btnContinue.pack_forget()
            btnReset.pack_forget()
            btnStop.pack()
            tick()

        def reset_tick():
            global temp
            temp = 0
            label1.configure(text='00:00')
            btnContinue.pack_forget()
            btnReset.pack_forget()
            btnStart.pack()

        window = Tk()
        window.title('Секундомер')
        window.resizable(width=False, height=False)
        window.geometry('300x200')
        window.attributes('-topmost', True)
        window.iconbitmap(startFolder + '\wikus.ico')

        label1 = Label(window, width=10, font=('Comic Sans MS', 30), text='00:00')
        label1.pack()

        btnStart = Button(window, text='Старт', font=('Comic Sans MS', 20), width=15, command=start_tick)
        btnStop = Button(window, text='Стоп', font=('Comic Sans MS', 20), width=15, command=stop_tick)
        btnContinue = Button(window, text='Продолжить', font=('Comic Sans MS', 20), width=15, command=continue_tick)
        btnReset = Button(window, text='Сброс', font=('Comic Sans MS', 20), width=15, command=reset_tick)
        btnStart.pack()

        window.mainloop()

    Button(canvas, width=70, height=70, image=imgStopwatch, command=Stopwatch).place(x=x, y=y)
    canvas.pack(side="top", fill="both", expand=True)
    text_canvas = canvas.create_text(x + 37, y + 90)
    canvas.itemconfig(text_canvas, text="Секундомер", font=("Arial 15 bold"), fill='white')


def addTranslator():
    def translator():
        def tran():
            for language, suffix in languages.items():

                if comboTwo.get() == language:
                    text = t.get('1.0', END)
                    a = translator.translate(text, dest=suffix)
                    t1.delete('1.0', END)
                    t1.insert('1.0', a.text)

        window = Tk()
        window.geometry('500x500')
        window.title('Переводчик')
        window.resizable(width=False, height=False)
        window['bg'] = 'black'
        window.attributes('-topmost', True)
        window.iconbitmap(startFolder + '\wikus.ico')
        translator = Translator()

        languages = {'Русский': 'ru', 'Английский': 'en', 'Французский': 'fr'}

        header_frame = Frame(window, bg='black')
        header_frame.pack(fill=X)

        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_columnconfigure(2, weight=1)

        valueOne = StringVar()
        valueTwo = StringVar()

        comboOne = ttk.Combobox(header_frame,
                                values=[
                                    "Русский",
                                    "Английский",
                                    "Французский"], textvariable=valueOne, state='readonly')
        comboOne.current(0)
        comboOne.grid(row=0, column=0)

        label = Label(header_frame, fg='white', bg='black', font='Arial 17 bold', text='->')
        label.grid(row=0, column=1)

        comboTwo = ttk.Combobox(header_frame,
                                values=[
                                    "Русский",
                                    "Английский",
                                    "Французский"], textvariable=valueTwo, state='readonly')
        comboTwo.current(1)
        comboTwo.grid(row=0, column=2)

        t = Text(window, width=35, height=5, font='Arial 12 bold')
        t.place(relx=0.5, rely=0.3, anchor=CENTER)

        btn = Button(window, width=45, text='Перевести', command=tran)
        btn.place(relx=0.5, rely=0.55, anchor=CENTER)

        t1 = Text(window, width=35, height=5, font='Arial 12 bold')
        t1.place(relx=0.5, rely=0.8, anchor=CENTER)

        window.mainloop()

    Button(canvas, width=70, height=70, image=imgTranslator, command=translator).place(x=x, y=y)
    canvas.pack(side="top", fill="both", expand=True)
    text_canvas = canvas.create_text(x + 37, y + 90)
    canvas.itemconfig(text_canvas, text="Переводчик", font=("Arial 15 bold"), fill='white')




def add_ide():
    def ide():
        def execute(event=None):
            global path
            print(path)
            if path != '':
                with open(f'{path}', 'w', encoding='utf-8') as f:
                    f.write(editArea.get('1.0', END))

                os.system(f'start cmd /K "python {path}"')
            else:
                with open('run.py', 'w', encoding='utf-8') as f:
                    f.write(editArea.get('1.0', END))

                os.system(f'start cmd /K "python run.py"')

        def changes(event=None):
            global previousText

            if editArea.get('1.0', END) == previousText:
                return

            for tag in editArea.tag_names():
                editArea.tag_remove(tag, "1.0", "end")

            i = 0
            for pattern, color in repl:
                for start, end in search_re(pattern, editArea.get('1.0', END)):
                    editArea.tag_add(f'{i}', start, end)
                    editArea.tag_config(f'{i}', foreground=color)

                    i += 1

            previousText = editArea.get('1.0', END)

        def search_re(pattern, text):
            matches = []
            text = text.splitlines()

            for i, line in enumerate(text):
                for match in re.finditer(pattern, line):
                    matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))

            return matches

        def rgb(rgb):
            return "#%02x%02x%02x" % rgb

        def open_file():
            global path
            file_path = filedialog.askopenfilename(title='Выбор файла', filetypes=(
            ('Текстовые документы (*.py)', '*.py'), ('Все файлы', '*.*')))
            if file_path:
                path = os.path.basename(file_path)
                editArea.delete('1.0', END)
                editArea.insert('1.0', open(file_path, encoding='utf-8').read())

        def save_file():
            file_path = filedialog.asksaveasfilename(
                filetypes=(('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*')))
            f = open(file_path, 'w', encoding='utf-8')
            text = editArea.get('1.0', END)
            f.write(text)
            f.close()

        window = Tk()
        window.geometry('700x500')
        window.title('Редактор кода')
        window.attributes('-topmost', True)

        normal = rgb((234, 234, 234))
        keywords = rgb((234, 95, 95))
        comments = rgb((95, 234, 165))
        string = rgb((234, 162, 95))
        function = rgb((95, 211, 234))
        background = rgb((42, 42, 42))
        font = 'Consolas 15'

        main_menu = Menu(window)
        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(label='Открыть', command=open_file)
        file_menu.add_command(label='Сохранить', command=save_file)
        window.config(menu=file_menu)

        repl = [
            [
                '(^| )(False|None|True|and|as|assert|print|async|await|break|class|continue|def|del|elif|else|else:|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )',
                keywords],
            ['".*?"', string],
            ['\".*?\"', string],
            ['#.*?$', comments],
        ]

        editArea = Text(
            window, background=background, foreground=normal, insertbackground=normal, relief=FLAT, borderwidth=30,
            font=font
        )
        editArea.pack(fill=BOTH, expand=1)

        editArea.insert('1.0', """#Для запуска программы введите: CTRL+R

        """)

        editArea.bind('<KeyRelease>', changes)

        window.bind('<Control-r>', execute)

        changes()

        window.mainloop()

    Button(canvas, width=70, height=70, image=imgIDE, command=ide).place(x=x, y=y)
    canvas.pack(side="top", fill="both", expand=True)
    text_canvas = canvas.create_text(x + 37, y + 90)
    canvas.itemconfig(text_canvas, text="Редактор кода", font=("Arial 15 bold"), fill='white')





def addTable():
    def table():
        xAxis = string.ascii_lowercase[0:5]
        yAxis = range(0, 10)

        cells = {}


        def evaluateCell(cellId):
            content = cells[cellId][0].get()
            content = content.lower()

            label = cells[cellId][1]

            if content.startswith('='):
                for cell in cells:
                    if cell in content.lower():
                        content = content.replace(cell, str(evaluateCell(cell)))

                content = content[1:]
                try:
                    content = eval(content)
                except:
                    content = 'NAN'
                label['text'] = content
                return content

            else:
                label['text'] = content
                return content


        def updateAllCells():
            window.after(10, updateAllCells)

            for cell in cells:
                evaluateCell(cell)

        window = Tk()
       

        window.title('Приложение для электронных таблиц')
        window.resizable(0, 0)
        
        window.attributes('-topmost', True)
        window.iconbitmap(startFolder + '\wikus.ico')
        

        for y in yAxis:
            label = Label(window, text=y, width=5, background='white')
            label.grid(row=y + 1, column=0)

        for i, x in enumerate(xAxis):
            label = Label(window, text=x, width=35, background='white')
            label.grid(row=0, column=i + 1, sticky='n')

        for y in yAxis:
            for xcoor, x in enumerate(xAxis):
                id = f'{x}{y}'

                var = StringVar(window, '', id)

                e = Entry(window, textvariable=var, width=30)
                e.grid(row=y + 1, column=xcoor + 1)

                label = Label(window, text='', width=5)
                label.grid(row=y + 1, column=xcoor + 1, sticky='e')

                cells[id] = [var, label]

        updateAllCells()


        window.mainloop()

    Button(canvas, width=70, height=70, image=imgTable, command=table).place(x=x, y=y)
    canvas.pack(side="top", fill="both", expand=True)
    text_canvas = canvas.create_text(x + 37, y + 90)
    canvas.itemconfig(text_canvas, text="Эл. таблицы", font=("Arial 15 bold"), fill='white')






def addExplorer():
    def explorer():
        ctypes.windll.shcore.SetProcessDpiAwareness(True)


        def path_change(*event):
            directory = os.listdir(current_path.get())
            list.delete(0, END)

            for file in directory:
                list.insert(0, file)


        def change_path_by_click(event=None):
            picked = list.get(list.curselection()[0])
            path = os.path.join(current_path.get(), picked)

            if os.path.isfile(path):
                os.startfile(path)
            else:
                current_path.set(path)


        def go_back(event=None):
            new_path = pathlib.Path(current_path.get()).parent
            current_path.set(new_path)


        def window_new_file_or_folder():
            global new_window
            new_window = Toplevel(root)
            new_window.geometry("250x150")
            new_window.resizable(0, 0)
            new_window.title("Новый файл/папка")

            new_window.columnconfigure(0, weight=1)

            Label(new_window, text='Введите название нового файла/папки').grid()
            Entry(new_window, textvariable=new_file_name).grid(column=0, pady=10, sticky=NSEW)
            Button(new_window, text="Создать", command=new_file_or_folder).grid(pady=10, sticky=NSEW)


        def new_file_or_folder():
            if len(new_file_name.get().split('.')) != 1:
                open(os.path.join(current_path.get(), new_file_name.get()), 'w').close()
            else:
                os.mkdir(os.path.join(current_path.get(), new_file_name.get()))

            new_window.destroy()
            path_change()

        window = Tk()
        window.geometry('400x250')
        window.title('Проводник файлов')
        
        window.attributes('-topmost', True)
        window.iconbitmap(startFolder + '\wikus.ico')
        window.grid_columnconfigure(1, weight=1)
        window.grid_rowconfigure(1, weight=1)

        new_window = ''

        new_file_name = StringVar(window, "Блокнот.txt", 'new_name')
        current_path = StringVar(window, name='current_path', value=pathlib.Path.cwd())

        current_path.trace('w', path_change)

        Button(window, text='Назад', command=go_back).grid(sticky=NSEW, column=0, row=0)

        window.bind("<Alt-Left>", go_back)

        Button(window, text='Создать', command=window_new_file_or_folder).grid(sticky=NSEW, column=0, row=1)

        Entry(window, textvariable=current_path).grid(sticky=NSEW, column=1, row=0, ipady=10, ipadx=10)

        list = Listbox(window)
        list.grid(sticky=NSEW, column=1, row=1, ipady=10, ipadx=10)

        list.bind('<Double-1>', change_path_by_click)
        list.bind('<Return>', change_path_by_click)

        path_change('')

        window.mainloop()

    Button(canvas, width=70, height=70, image=imgExplorer, command=explorer).place(x=x, y=y)
    canvas.pack(side="top", fill="both", expand=True)
    text_canvas = canvas.create_text(x + 37, y + 90)
    canvas.itemconfig(text_canvas, text="Проводник файлов", font=("Arial 15 bold"), fill='white')






def addCalendar():
    def calendar1():
        def back():
            
            month -= 1
            if month == 0:
                month = 12
                year -= 1
            fill()


        def next():
            
            month += 1
            if month == 13:
                month = 1
                year += 1
            fill()



        def fill():
            info_label['text'] = calendar.month_name[month] + ', ' + str(year)
            month_days = calendar.monthrange(year, month)[1]
            if month == 1:
                back_month_days = calendar.monthrange(year - 1, 12)[1]
            else:
                back_month_days = calendar.monthrange(year, month - 1)[1]
            week_day = calendar.monthrange(year, month)[0]

            for n in range(month_days):
                days[n + week_day]['text'] = n + 1
                days[n + week_day]['fg'] = 'black'
                if year == now.year and month == now.month and n ==now.day:
                    days[n + week_day - 1]['bg'] = 'green'
                    days[n + week_day]['bg'] = 'grey'
                else:
                    days[n + week_day]['bg'] = 'gray'

            for n in range(week_day):
                days[week_day - n - 1]['text'] = back_month_days - n
                days[week_day - n - 1]['fg'] = 'gray'
                days[week_day - n - 1]['bg'] = '#f3f3f3'
            for n in range(6 * 7 - month_days - week_day):
                days[week_day + month_days + n]['text'] = n + 1
                days[week_day + month_days + n]['fg'] = 'gray'
                days[week_day + month_days + n]['bg'] = '#f3f3f3'

        window = Tk()
        window.geometry('500x500')
        window.title('Календарь')
        
        window.attributes('-topmost', True)
        window.iconbitmap(startFolder + '\wikus.ico')
        

        
        back_button = Button(window, text='<', command=back)
        back_button.grid(row=0, column=0, sticky=NSEW)
        next_button = Button(window, text='>', command=next)
        next_button.grid(row=0, column=6, sticky=NSEW)
        info_label = Label(window, text='0', width=1, height=1, font='Arial 16 bold', fg='blue')
        info_label.grid(row=0, column=1, columnspan=5, sticky=NSEW)

        for n in range(7):
            lbl = Label(window, text=calendar.day_abbr[n], width=1, height=1, font='Arial 10 bold', fg='darkblue')
            lbl.grid(row=1, column=n, sticky=NSEW)

        for row in range(6):
            for col in range(7):
                lbl = Label(window, text='0', width=4, height=2, font='Arial 16 bold')
                lbl.grid(row=row+2, column=col, sticky=NSEW)
                days.append(lbl)

        fill()

        window.mainloop()

    Button(canvas, width=70, height=70, image=imgCalendar, command=calendar1).place(x=x, y=y)
    canvas.pack(side="top", fill="both", expand=True)
    text_canvas = canvas.create_text(x + 37, y + 90)
    canvas.itemconfig(text_canvas, text="Календарь", font=("Arial 15 bold"), fill='white')






################
# Окно tkinter #
################

root = Tk()
root.attributes('-fullscreen', True)
root.bind('<Escape>', lambda _: root.destroy())
root.title('Лучшая ОС')
root.iconbitmap(startFolder + '\wikus.ico')
########
# Меню #
########

root.bind("<Button-3>", popup)
menu = Menu(tearoff=0)
menu.add_command(label="Создать папку", command=add_folder)
menu.add_command(label="Создать блокнот", command=addNotepad)
menu.add_command(label="Создать paint", command=addPaint)
menu.add_command(label="Калькулятор", command=addCalculator)
menu.add_command(label="Секундомер", command=addStopwatch)
menu.add_command(label="Переводчик", command=addTranslator)
menu.add_command(label="Редактор кода", command=add_ide)
menu.add_command(label="Эл. Таблицы", command=addTable)
menu.add_command(label="Проводник файлов", command=addExplorer)
menu.add_command(label="Календарь", command=addCalendar)

# Фон
bg_menu_sub = Menu(menu, tearoff=0)
bg_menu_sub.add_command(label='Изображение', command=updateImg)
# bg_menu_sub.add_command(label='GIF')  # , command=gifBg
bg_menu_sub.add_command(label='Слайд-шоу', command=Thread(target=ShowImg).start)
menu.add_cascade(label='Фон', menu=bg_menu_sub)

# Игры
game_menu_sub = Menu(menu, tearoff=0)
game_menu_sub.add_command(label='Анаграммы', command=addAnagrammi)
game_menu_sub.add_command(label="Кликер", command=addClicker)
game_menu_sub.add_command(label="Камень ножницы бумага", command=addKnb)
menu.add_cascade(label='Игры', menu=game_menu_sub)

# Панель задач
pz_menu_sub = Menu(menu, tearoff=0)
pz_menu_sub.add_command(label='Показать', command=start_pz)
pz_menu_sub.add_command(label='Скрыть', command=stop_pz)
menu.add_cascade(label='Панель задач', menu=pz_menu_sub)

# Закрыть ОС
menu.add_command(label="Закрыть ОС", command=quit_os)

############
# Фон окна #
############

canvas = Canvas(root, highlightthickness=0)
canvas.pack(fill=BOTH, expand=1)
imgbox = canvas.create_image(0, 0, image=None, anchor='nw')

# Сменить изображениt
updateRoot('background/bg8.png')
# root.after(500, updateRoot, 'image/bg2.png')

################
# Панель задач #
################
watch = Label(root, font="Arial 20")
btn = Button(root, text='Сделать скриншот', font=('Comic Sans MS', 11, 'bold'), borderwidth=2)

imgIcon = ImageTk.PhotoImage(Image.open("wikus.ico").resize((30, 32), Image.ANTIALIAS))
btn_2 = Button(root, font=('Comic Sans MS', 11, 'bold'), image=imgIcon, borderwidth=2)
start_pz()
#################
# Иконки кнопок #
#################

imgFolder = ImageTk.PhotoImage(Image.open("image/folder.png").resize((90, 60), Image.ANTIALIAS))
imgNotepad = ImageTk.PhotoImage(Image.open("image/notepad.png").resize((90, 60), Image.ANTIALIAS))
imgPaint = ImageTk.PhotoImage(Image.open("image/paint.png").resize((90, 60), Image.ANTIALIAS))
imgAnagrammi = ImageTk.PhotoImage(Image.open("image/anagrammi.png").resize((90, 60), Image.ANTIALIAS))
imgCalculator = ImageTk.PhotoImage(Image.open("image/calculator.png").resize((90, 60), Image.ANTIALIAS))
imgClicker = ImageTk.PhotoImage(Image.open("image/clicker.png").resize((90, 60), Image.ANTIALIAS))
imgKnb = ImageTk.PhotoImage(Image.open("image/knb.png").resize((90, 60), Image.ANTIALIAS))
imgStopwatch = ImageTk.PhotoImage(Image.open("image/stopwatch.png").resize((90, 60), Image.ANTIALIAS))
imgTranslator = ImageTk.PhotoImage(Image.open("image/translator.png").resize((90, 60), Image.ANTIALIAS))
imgIDE = ImageTk.PhotoImage(Image.open("image/ide.png").resize((90, 60), Image.ANTIALIAS))
imgTable = ImageTk.PhotoImage(Image.open("image/table.png").resize((90, 60), Image.ANTIALIAS))
imgExplorer = ImageTk.PhotoImage(Image.open("image/explorer.png").resize((90, 60), Image.ANTIALIAS))
imgCalendar = ImageTk.PhotoImage(Image.open("image/calendar.png").resize((90, 60), Image.ANTIALIAS))

root.mainloop()
