from tkinter import *
from tkinter import filedialog

from main import run_video

def create_gui():

    def handle_button_click():
        name = input_name.get()
        width = input_width.get()
        distance = input_distance.get()

        run_video(name, float(width), float(distance))

    def handle_button_browse():
        filename = filedialog.askopenfilename(
            initialdir='./',
            title='Выберите файл',
            filetypes=(("Video",
                        "*.mp4*"),
                        ("all files",
                         "*.*"))
        )
        
        if filename != '':
            label_file.config(text=f'Видео: {filename}')

    root = Tk()

    frame = Frame(root)
    frame.grid(padx=10, pady=10, column=10)

    input_name = Entry(frame)
    input_distance = Entry(frame)
    input_width = Entry(frame)

    label_name = Label(frame, text='Введите класс объекта')
    label_distance = Label(frame, text='Введите изначальную дистаницию до объекта (в футах)')
    label_width = Label(frame, text='Введите изначальную ширину объекта')
    label_file = Label(frame, text='Выберите файл')

    btn_run = Button(frame, text='Запуск', command=handle_button_click)
    btn_browse = Button(frame, text='Выбрать файл', command=handle_button_browse)
    btn_close = Button(frame, text='Закрыть', command=root.destroy)

    input_name.grid(row=1, column=2, sticky='w')
    input_distance.grid(row=2, column=2)
    input_width.grid(row=3, column=2)

    label_name.grid(row=1, column=1)
    label_distance.grid(row=2, column=1)
    label_width.grid(row=3, column=1)
    label_file.grid(row=4, column=1)

    btn_run.grid(row=4, column=0)
    btn_browse.grid(row=0, column=0)
    btn_close.grid(row=4, column=2)
    
    return root

def main():
    gui = create_gui()
    gui.mainloop()

    # run_video()

if __name__ == '__main__':
    main()