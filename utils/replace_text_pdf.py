import PyPDF2
import pytesseract
from pdf2image import convert_from_path


def replace_text(pdf_path, search_text, replace_text):
    # Преобразуем PDF в изображения
    images = convert_from_path(pdf_path)

    writer = PyPDF2.PdfWriter()

    # Проходим по всем страницам (изображениям)
    for i, image in enumerate(images, 1):
        # Распознаем текст на изображении
        text = pytesseract.image_to_string(image)

        # Находим и заменяем текстовый фрагмент
        if search_text in text:
            text = text.replace(search_text, replace_text)

        # Создаем новую PDF страницу с текстом
        page = PyPDF2.pdf.PageObject.create_blank_page(width=image.width, height=image.height)
        page.merge_page(image)
        writer.add_page(page)

    # Сохраняем измененный PDF в новый файл
    with open('output.pdf', 'wb') as output_file:
        writer.write(output_file)


# Пример использования
replace_text("C:/Users/user/PycharmProjects/DvijeniePervih/Тулинов Артем.pdf", 'Тулинов Артем', 'Иванов Иван')
