from os.path import exists
from csv import DictReader, DictWriter


class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt


class NameError(Exception):
    def __init__(self, txt):
        self.txt = txt


def get_name_input(prompt):
    while True:
        try:
            name = input(prompt)
            if len(name) < 2:
                raise NameError("Не валидное имя")
            else:
                return name
        except NameError as err:
            print(err)


def get_info():
    first_name = get_name_input("Введите имя: ")
    last_name = get_name_input("Введите фамилию: ")

    is_valid_phone = False
    while not is_valid_phone:
        try:
            phone_number = int(input("Введите номер: "))
            if len(str(phone_number)) != 11:
                raise LenNumberError("Неверная длина номера")
            else:
                is_valid_phone = True
        except ValueError:
            print("Не валидный номер!!!")
        except LenNumberError as err:
            print(err)

    return [first_name, last_name, phone_number]


def create_file(file_name):
    # with - Менеджер контекста
    with open(file_name, "w", encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()


def read_file(file_name):
    if not exists(file_name):
        print(f"Файл '{file_name}' не существует. Создаем пустой файл.")
        create_file(file_name)

    with open(file_name, "r", encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)


def write_file(file_name, lst):
    res = read_file(file_name)
    for el in res:
        if el["Телефон"] == str(lst[2]):
            print("Такой телефон уже есть")
            return

    obj = {"Имя": lst[0], "Фамилия": lst[1], "Телефон": lst[2]}
    res.append(obj)
    with open(file_name, "w", encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)


def copy_row(src_file, dest_file, row_number):
    src_data = read_file(src_file)
    if row_number < 1 or row_number > len(src_data):
        print("Неверный номер строки")
        return

    row_to_copy = src_data[row_number - 1]
    write_file(dest_file, [row_to_copy["Имя"],
               row_to_copy["Фамилия"], row_to_copy["Телефон"]])


file_name = 'phone.csv'


def main():
    while True:
        command = input("Введите команду: ")
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name, get_info())
        elif command == 'r':
            if not exists(file_name):
                print("Файл отсутствует. Создайте его")
                continue
            print(*read_file(file_name))
        elif command == 'c':
            src_file = input("Введите имя исходного файла: ")
            dest_file = input(
                "Введите имя файла, в который нужно скопировать: ")
            row_number = int(input("Введите номер строки для копирования: "))
            copy_row(src_file, dest_file, row_number)


main()
