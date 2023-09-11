import os
import shutil
import sqlite3


# переносит файл из директории в другую директорию под новым именем
# os.replace(path1, "E:\papka2\\1.txt")

def main():
    cache_status = 1
    while True:
        print("Выберите действие: \n"
              "1. Перенести настройки аккаунта \n"
              "2. Удалять кэш? \n"
              "3. Сохраненные переносы")
        x = input()
        if x == "1":
            transf_sett(cache_status)
        elif x == "2":
            try:
                print("Удалять кэш? \n1. ДА \n2. НЕТ \n")
                y = int(input())
                cache_status = y
            except:
                print("Введите корректное число")
        elif x == "3":
            load_in_db()
        else:
            print("Введите корректное число")


def transf_sett(cache_status):
    while True:
        try:
            print("Укажите путь до игры ИЗ КОТОРОЙ будут переноситься настройки")
            path1 = input() + "\\WTF\\Account\\"
            if "Data" not in os.listdir(path1[:-12]):
                qwe = 7/0
            else:
                break
        except:
            print("Укажите путь до файлов игры(где находится wow.exe, data, interdace...)")

    while True:
        try:
            print("Укажите путь до игры КУДА будут переноситься настройки")
            path2 = input() + "\\WTF\\Account\\"
            if "Data" not in os.listdir(path2[:-12]):
                qwe = 7/0
            else:
                break
        except:
            print("Укажите путь до файлов игры(где находится wow.exe, data, interdace...)")

    if cache_status == 1:
        clear_cache(path1, path2)

    print("Выберите аккаунт ИЗ КОТОРОГО буду переноситься настройки")
    for i in os.listdir(path1):
        print(os.listdir(path1).index(i), i)

    while True:
        try:
            path1 += os.listdir(path1)[int(input())] + "\\"

            if "cache.md5" not in os.listdir(path1):
                wqe = 7/0
            else:
                break
        except:
            print("Введите корректное число")

    print("Выберите аккаунт КУДА будут переноситься настройки")
    for i in os.listdir(path2):
        print(os.listdir(path2).index(i), i)

    while True:
        try:
            path2 += os.listdir(path2)[int(input())] + "\\"

            if "cache.md5" not in os.listdir(path2):
                wqe = 7/0
            else:
                break
        except:
            print("Введите корректное число")

    list_files_from = ["bindings-cache.old", 'bindings-cache.wtf',
                       'cache.md5', 'config-cache.old', 'config-cache.wtf', 'macros-cache.old', 'macros-cache.txt', 'SavedVariables.lua',
                       'SavedVariables.lua.bak', 'SavedVariables']
    list_file_to = os.listdir(path2)

    char_path_from = get_path_char_from(path1, list_files_from)
    char_path_to = get_path_char_to(path2, list_files_from)

    from_to(path1, path2, list_files_from, list_file_to, char_path_from, char_path_to)


def from_to(p1, p2, l1, l2, p3, p4):
    if p1 != p2:
        for i in l1:
            try:
                if i in l2:
                    if i == l1[-1]:
                        shutil.rmtree(p2 + i)
                        shutil.copytree(p1 + i, p2 + i)
                        continue

                    os.remove(p2 + i)
                    shutil.copyfile(p1 + i, p2 + i)
                else:
                    if i == l1[-1]:
                        shutil.copytree(p1 + i, p2 + i)
                        continue
                    shutil.copyfile(p1 + i, p2 + i)
            except:
                print(i, "не найден или возникла другая ошибка \n")

    for i in os.listdir(p3):
        if p3 != p4:
            try:
                if i in os.listdir(p4):
                    if i == "SavedVariables":
                        shutil.rmtree(p4 + i)
                        shutil.copytree(p3 + i, p4 + i)
                        continue

                    os.remove(p4 + i)
                    shutil.copyfile(p3 + i, p4 + i)
                else:
                    if i == "SavedVariables":
                        shutil.copytree(p3 + i, p4 + i)
                        continue
                    shutil.copyfile(p3 + i, p4 + i)
            except:
                print(i, "не найден или возникла другая ошибка \n")
    else:
        print("Копирование файлов завершено\n")
        print("Запомнить пути переноса настроек? \n1. ДА \n2. НЕТ \n")
        while True:
                x = int(input())
                if x == 1:
                    print("Название пресета:")
                    name = input()
                    save_in_db(name, p1, p2, p3, p4)
                elif x == 2:
                    main()
                else:
                    print("Введите корректное число")


def get_path_char_to(p2, l1):
    server_list_to = []
    for i in os.listdir(p2):
        if i not in l1:
            server_list_to.append(i)

    print("Выберите сервер куда будут переноситься настройки:")
    for i in server_list_to:
        print(str(server_list_to.index(i)) + ".", i)

    while True:
        try:
            server = server_list_to[int(input())]
            acc_list_to = os.listdir(p2 + server)
            break
        except:
            print("Введите корректное число")

    print("Выберите персонажа на которого будут переносится настройки:")
    for i in acc_list_to:
        print(str(acc_list_to.index(i)) + ".", i)

    while True:
        try:
            character = acc_list_to[int(input())]
            break
        except:
            print("Введите корректное число")

    return p2 + server + "\\" + character + "\\"


def get_path_char_from(p1, l1):
    server_list_from = []
    for i in os.listdir(p1):
        if i not in l1:
            server_list_from.append(i)

    print("Выберите сервер откуда будут переносится настройки:")
    for i in server_list_from:
        print(str(server_list_from.index(i)) + ".", i)

    while True:
        try:
            server = server_list_from[int(input())]
            acc_list_from = os.listdir(p1 + server)
            break
        except:
            print("Введите корректное число")

    print("Выберите персонажа с которого будут переносится настройки:")
    for i in acc_list_from:
        print(str(acc_list_from.index(i)) + ".", i)

    while True:
        try:
            character = acc_list_from[int(input())]
            break
        except:
            print("Введите корректное число")

    return p1 + server + "\\" + character + "\\"


def clear_cache(p1, p2):
    if p1 == p2:
        if "Cache" in os.listdir(p2[:-12]):
            shutil.rmtree(p1[:-12] + "Cache")
            print("Кэш удален \n")
            return
        else:
            print("Кэш не найден")
            return
    else:
        if "Cache" in os.listdir(p2[:-12]):
            shutil.rmtree(p2[:-12] + "Cache")

        if "Cache" in os.listdir(p1[:-12]):
            shutil.rmtree(p1[:-12] + "Cache")
            print("Кэш удален \n")
        else:
            print("Кэш не найден")


def save_in_db(name, p1, p2, p3, p4):
    print("Save_in_db")
    print(p1,p2,p3,p4)
    connection = sqlite3.connect('paths.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Paths (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    p1 TEXT NOT NULL,
    p2 TEXT NOT NULL,
    p3 TEXT NOT NULL,
    p4 TEXT NOT NULL
    )
    ''')

    cursor.execute(f'INSERT INTO Paths (name, p1, p2, p3, p4) VALUES (?, ?, ?, ?, ?)', (name, p1, p2, p3, p4))

    connection.commit()
    connection.close()


def load_in_db():
    connection = sqlite3.connect('paths.db')
    cursor = connection.cursor()

    cursor.execute('SELECT name FROM Paths')
    name_paths = cursor.fetchall()

    print("Выберите пресет:")
    for i in name_paths:
        print(str(name_paths.index(i)) + ".", i[0])
        if i == name_paths[-1]:
            print(str(name_paths.index(i) + 1) + ". Назад")


    while True:
        try:
            x = int(input())
            if x == len(name_paths):
                main()
            if name_paths[x]:
                break
        except:
            print("Введите корректное число")

    cursor.execute('SELECT p1,p2,p3,p4 FROM Paths')
    paths = cursor.fetchall()

    list_files_from = ["bindings-cache.old", 'bindings-cache.wtf',
                       'cache.md5', 'config-cache.old', 'config-cache.wtf', 'macros-cache.old', 'macros-cache.txt', 'SavedVariables.lua',
                       'SavedVariables.lua.bak', 'SavedVariables']
    list_file_to = os.listdir(paths[x][1])

    from_to(paths[x][0], paths[x][1], list_files_from, list_file_to, paths[x][2], paths[x][3])


if __name__ == "__main__":
    main()
