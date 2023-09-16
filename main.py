import os
import shutil
import sqlite3
import sys
import psutil

from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog
from ui_main import Ui_MainWindow
from save_in_bd import Ui_Dialog
from PyQt6 import QtCore, QtGui, QtWidgets

# переносит файл из директории в другую директорию под новым именем
# os.replace(path1, "E:\papka2\\1.txt")


class move_WTF(QMainWindow):
    def __init__(self):
        super(move_WTF, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_5.clicked.connect(self.move_wtf)
        self.list_paths()
        self.ui.pushButton.clicked.connect(self.open_file_dialog)
        self.ui.pushButton_2.clicked.connect(self.open_file_dialog)
        self.ui.pushButton_3.clicked.connect(self.open_file_dialog)
        self.ui.pushButton_4.clicked.connect(self.open_file_dialog)

        self.ui.pushButton_7.clicked.connect(self.open_save_dialog)

        self.ui.comboBox.currentIndexChanged.connect(self.load_from_bd)

    def move_wtf(self):
        p1 = self.ui.textEdit.toPlainText() + "\\"
        p2 = self.ui.textEdit_2.toPlainText() + "\\"
        p3 = self.ui.textEdit_3.toPlainText() + "\\"
        p4 = self.ui.textEdit_4.toPlainText() + "\\"
        cache_status = str(self.ui.checkBox.checkState())

        if cache_status == "CheckState.Checked":
            clear_cache(p1, p2)

        list_files_from = ["bindings-cache.old", 'bindings-cache.wtf',
                           'cache.md5', 'config-cache.old', 'config-cache.wtf', 'macros-cache.old', 'macros-cache.txt',
                           'SavedVariables.lua',
                           'SavedVariables.lua.bak', 'SavedVariables']
        list_file_to = os.listdir(p2)
        try:
            from_to(p1, p2, list_files_from, list_file_to, p3, p4)
        except:
            self.window_modal()

    def open_file_dialog(self):
        file_path = QFileDialog.getExistingDirectory()
        sender = self.sender()

        if str(sender.objectName()) == "pushButton":
            self.ui.textEdit.setText(file_path)
        elif sender.objectName() == "pushButton_2":
            self.ui.textEdit_2.setText(file_path)
        elif sender.objectName() == "pushButton_3":
            self.ui.textEdit_3.setText(file_path)
        elif sender.objectName() == "pushButton_4":
            self.ui.textEdit_4.setText(file_path)

    def save_preset(self):
        name = self.ui_window.textEdit.toPlainText()
        p1 = self.ui.textEdit.toPlainText()
        p2 = self.ui.textEdit_2.toPlainText()
        p3 = self.ui.textEdit_3.toPlainText()
        p4 = self.ui.textEdit_4.toPlainText()

        save_preset_in_db(name, p1, p2, p3, p4)
        self.new_window.close()

    def open_save_dialog(self):
        self.new_window = QDialog()
        self.ui_window = Ui_Dialog()
        self.ui_window.setupUi(self.new_window)
        self.new_window.show()
        self.ui_window.pushButton_5.clicked.connect(self.save_preset)

    def list_paths(self):
        #pathdb = str(__file__)[:str(__file__).rfind("\\")]
        #pathdb = "C:\\Users\\pokam\\AppData\\LocalLow\\move_WTF"

        proc_name = 'main.exe'  # 'cmd.exe'

        for proc in psutil.process_iter():
            # Пока скрипт работает, процесс уже может перестать существовать
            # (поскольку между psutil.process_iter() и proc.name() проходит время)
            # и будет выброшено исключение psutil.NoSuchProcess
            try:
                proc_name_in_loop = proc.name()
            except psutil.NoSuchProcess:
                pass
            else:
                if proc_name_in_loop == proc_name:
                    pathdb = proc.cwd()
                    print(proc.exe())

        connection = sqlite3.connect(pathdb + '\\paths.db')
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

        cursor.execute('SELECT name FROM Paths')
        name_paths = cursor.fetchall()
        for i in name_paths:
            self.ui.comboBox.addItem(str(i[0]))

    def load_from_bd(self): #p1, p2, p3, p4
        p1, p2, p3, p4 = load_in_db(self.ui.comboBox.currentIndex() - 1)
        self.ui.textEdit.setText(p1)
        self.ui.textEdit_2.setText(p2)
        self.ui.textEdit_3.setText(p3)
        self.ui.textEdit_4.setText(p4)

    def window_modal(self):
        self.app2 = Modal()
        self.app2.resize(300, 60)
        self.app2.setWindowTitle("ERROR!!")
        self.app2.setStyleSheet(
            "background: radial-gradient(50% 50% at 50% 50%, rgba(255, 255, 255, 0.17) 0%, rgba(60, 60, 60, 0) 85.42%), #18181B;\n"
            "    background-repeat: no-repeat;\n"
            "    background-size: cover;")
        self.app2.label = QtWidgets.QLabel(parent=self.app2)
        self.app2.label.setGeometry(QtCore.QRect(70, 10, 300, 31))
        self.app2.label.setStyleSheet("color: #fff;\n"
                                 "font: 8pt \"Yu Gothic UI Semilight\";\n"
                                 "font-size: 14px;")
        self.app2.label.setObjectName("label")
        self.app2.label.setText("Введите корректный паз")
        self.app2.show()


class Modal(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setWindowModality(Qt.WindowModal)
        # self.setModal(True)
        self.resize(200, 200)



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


def transf_sett(
        cache_status):
    while True:
        try:
            print("Укажите путь до игры ИЗ КОТОРОЙ будут переноситься настройки")
            path1 = input() + "\\WTF\\Account\\"
            if "Data" not in os.listdir(path1[:-12]):
                qwe = 7/0
            else:
                break
        except:
            print("Укажите путь до файлов игры(где находится wow.exe, data, interface...)")


    while True:
        try:
            print("Укажите путь до игры КУДА будут переноситься настройки")
            path2 = input() + "\\WTF\\Account\\"
            if "Data" not in os.listdir(path2[:-12]):
                qwe = 7/0
            else:
                break
        except:
            print("Укажите путь до файлов игры(где находится wow.exe, data, interface...)")

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

    for i in os.listdir(p3):
        if p3 != p4:
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
    else:
        print("Копирование файлов завершено\n")


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
        if "Cache" in os.listdir(p2):
            shutil.rmtree(p1 + "Cache")
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


def save_preset_in_db(name, p1, p2, p3, p4):

    proc_name = 'main.exe'  # 'cmd.exe'

    for proc in psutil.process_iter():
        # Пока скрипт работает, процесс уже может перестать существовать
        # (поскольку между psutil.process_iter() и proc.name() проходит время)
        # и будет выброшено исключение psutil.NoSuchProcess
        try:
            proc_name_in_loop = proc.name()
        except psutil.NoSuchProcess:
            pass
        else:
            if proc_name_in_loop == proc_name:
                pathdb = proc.cwd()
                print(proc.exe())

    connection = sqlite3.connect(pathdb + '\\paths.db')
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


def load_in_db(x):
    # pathdb = str(__file__)[:str(__file__).rfind("\\")]
    #pathdb = "C:\\Users\\pokam\\AppData\\Local\\move_WTF"

    proc_name = 'main.exe'  # 'cmd.exe'

    for proc in psutil.process_iter():
        # Пока скрипт работает, процесс уже может перестать существовать
        # (поскольку между psutil.process_iter() и proc.name() проходит время)
        # и будет выброшено исключение psutil.NoSuchProcess
        try:
            proc_name_in_loop = proc.name()
        except psutil.NoSuchProcess:
            pass
        else:
            if proc_name_in_loop == proc_name:
                pathdb = proc.cwd()
                print(proc.exe())

    connection = sqlite3.connect(pathdb + '\\paths.db')
    cursor = connection.cursor()

    cursor.execute('SELECT p1,p2,p3,p4 FROM Paths')
    paths = cursor.fetchall()

    return paths[x][0], paths[x][1], paths[x][2], paths[x][3]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = move_WTF()
    window.show()

    sys.exit(app.exec())
