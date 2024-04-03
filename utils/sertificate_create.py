from PIL import Image, ImageDraw, ImageFont


def certificate(fio, result):
    fio = fio[0]
    result = result[0]
    im = Image.open("C:/Users/user/PycharmProjects/DvijeniePervih/utils/test.jpg")
    font = ImageFont.truetype(
        font="C:/Users/user/PycharmProjects/DvijeniePervih/utils/fonts/DejaVu_Sans/DejaVuSans.ttf",
        size=30)
    draw_text = ImageDraw.Draw(im)
    draw_text.text((200, 710), text=str(fio), font=font, fill='#1C0606')
    draw_text.text((200, 780), text=f'Результат: {str(result)}', font=font, fill='#1C0606')
    im.save(f'C:/Users/user/PycharmProjects/DvijeniePervih/utils/upload/{fio}.pdf')
