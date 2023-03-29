# from tkinter import *
# from tkinter import filedialog

from customtkinter import *

from main import run_video, formatMeterToInch

# TODO Добавить селектор для выбора классов из txt файла
# TODO Добавить проверку на то что все поля заполнены

def create_gui():
    video_path = ''
    img_path = ''

    def handle_button_click():
        global video_path, img_path
        
        name = input_name.get()
        width = formatMeterToInch(float(input_width.get()))
        distance = formatMeterToInch(float(input_distance.get()))

        run_video(name, width, distance, img_path, video_path)

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
            global video_path

            video_path = filename
            
            # label_file.configure(text=f'Видео: {filename}')
            label_file.configure(text="Видео выбрано ✅")    
    def handle_button_browse_image():
        filename = filedialog.askopenfilename(
            initialdir='./',
            title='Выберите файл',
            filetypes=(("image",
                        "*.png*"),
                        ("all files",
                         "*.*"))
        )
        
        if filename != '':
            global img_path
            img_path = filename

            # label_img.configure(text=f'Изображение: {filename}')
            label_img.configure(text='Изображение выбрано: ✅')
    
    root = CTk() 
    root.title('Distance Measuring')
    frame = CTkFrame(root)
    
    frame.grid(padx=10, pady=10, row=10, column=0)

    input_frame = CTkFrame(root)
    input_frame.grid(padx=10, pady=10, row=0, column=0, rowspan=2, sticky="nsew")
    input_frame.grid_columnconfigure(2, weight=1)
    
    input_name = CTkEntry(input_frame)
    input_distance = CTkEntry(input_frame)
    input_width = CTkEntry(input_frame)

    label_name = CTkLabel(input_frame, text='Класс объекта')
    label_distance = CTkLabel(input_frame, text='Дистаниция (м)')
    label_width = CTkLabel(input_frame, text='Ширина (м)')

    label_file = CTkLabel(frame, text='Видео не выбрано ❌',  wraplength=350)
    label_img = CTkLabel(frame, text='Изображение не выбрано ❌', wraplength=350)
    
    btn_run = CTkButton(frame, text='Запуск', command=handle_button_click)
    btn_browse = CTkButton(frame, text='Выбрать файл', command=handle_button_browse)
    btn_browse_image = CTkButton(frame, text='Выбрать изображение', command=handle_button_browse_image)
    btn_close = CTkButton(frame, text='Закрыть', command=root.destroy)

    input_name.grid(row=1, column=3, padx=10, pady=5, columnspan=5)
    input_distance.grid(row=2, column=3, padx=10, pady=5)
    input_width.grid(row=3, column=3, padx=10, pady=5)

    label_name.grid(row=1, column=1, padx=10,)
    label_distance.grid(row=2, column=1, padx=10,)
    label_width.grid(row=3, column=1, padx=10,)
    label_file.grid(row=0, column=1, padx=10,)
    label_img.grid(row=1, column=1, padx=10,)

    btn_browse.grid(row=0, column=0, padx=10, pady=10)
    btn_browse_image.grid(row=1, column=0)

    btn_run.grid(row=5, column=0, padx=10, pady=10)
    btn_close.grid(row=5, column=1, padx=10, pady=10)
    return root

def main():
    gui = create_gui()
    gui.mainloop()

    # run_video()

if __name__ == '__main__':
    main()