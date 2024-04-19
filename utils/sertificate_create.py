import tkinter
from tkinter import font

from PIL import Image, ImageDraw, ImageFont


def certificate(fio, result):
    tkinter.Frame().destroy()
    txt = font.Font(family="Pragmatica", size=55)
    # Значения в пикселях начала "поля ввода" для ФИО, результата и конца.
    name_start = (100, 933)
    name_end = (1554, 933)
    result_start = (1169, 1251)
    result_end = (1257, 1251)
    fio = fio[0]
    result = result[0]
    width_name = txt.measure(fio)  # Длина ФИО в пикселях
    width_result = txt.measure(str(result))  # Длина результата в пикселях
    im = Image.open("/root/bots/DvijeniePervih/utils/test.jpg")  # Открываем изображение
    font_fio = ImageFont.truetype(
        font="/root/bots/DvijeniePervih/utils/fonts/Pragmatica/Pragmatica-Black.ttf",
        size=55)  # Шрифт для ФИО
    font_result = ImageFont.truetype(
        font="/root/bots/DvijeniePervih/utils/fonts/Pragmatica/Pragmatica-Black.ttf",
        size=55)  # Шрифт для результата
    draw_text = ImageDraw.Draw(im)
    # Пишем ФИО. ХУ - находим середину поля ввода и середину ФИО и вычисляем как написать ФИО по центру поля ввода
    draw_text.text(((((name_start[0] + name_end[0]) / 2) - width_name / 2) + 155, 730 + 125), text=str(fio),
                   font=font_fio,
                   fill='#000000', align="center")
    # Пишем результат, тем же самым образом ищем центр
    draw_text.text(((((result_start[0] + result_end[0]) / 2) - width_result / 2) + 14, 1185), text=f'{str(result)}',
                   font=font_result,
                   fill='#000000')
    # Пробуем сохранить изменённую фотографию в формате pdf
    try:
        im.save(f'/root/bots/DvijeniePervih/utils/upload/{fio}.pdf')
    except OSError as e:
        print(f"Ошибка при сохранении файла: {e}")
