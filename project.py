# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
from PyQt5.Qt import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
from PyQt5 import QtWidgets
from time import sleep
import sip
import sqlite3


# from pythonping imfgffgport ping
class Tag(QWidget):
    def __init__(self, url: str, id: int):
        self.url = url
        self.id = id
        self.site_name = self.url[:url.find('.')]
        # self.update_site_name()
        super().__init__()
        self.initUi()
        self.is_deleted = False

    def initUi(self):
        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)
        self.gridLayout.setObjectName("gridLayout")
        # self.setGeometry(200, 200, 250, 40)
        self.tag_body = QPushButton(self.site_name, self)
        # self.tag_body.resize(250, 40)
        self.del_btn = QPushButton('x', self)
        # self.del_btn.resize(26, 26)
        # self.del_btn.move(215, 7)
        self.gridLayout.addWidget(self.tag_body, 0, 0, 1, 5)
        self.gridLayout.addWidget(self.del_btn, 0, 4, 1, 1)
        self.del_btn.setStyleSheet("""
            QPushButton{
            background-color: grey;
            border-style: outset;
            border-width: 1px;
            border-radius: 20px;
            border-color: black;
            padding: 2px;
            }
            """)

    def update_site_name(self):
        if 'https://www' in self.url:
            self.site_name = self.url[12:][:self.url[12:].find('.')]
            # print(self.site_name, self.url[12:], self.url, self.url[12:].find('.'))
        elif 'https://' in self.url:
            self.site_name = self.url[8:][:self.url[8:].find('.')]
        else:
            self.site_name = self.url[:self.url.find('.')]
        self.tag_body.setText(self.site_name)


class Master_Tag(QWidget):
    def __init__(self, name: str, tags: list, id: int):
        self.name = name
        self.tags = tags
        self.id = id
        # print(type(self.tags))
        super().__init__()
        self.initUi()
        self.is_deleted = False

    def initUi(self):
        self.gridLayout = QGridLayout()
        self.setLayout(self.gridLayout)
        self.gridLayout.setObjectName("gridLayout")
        # self.setGeometry(200, 200, 250, 40)
        self.tag_body = QPushButton(self.name, self)
        # self.tag_body.resize(250, 40)
        self.del_btn = QPushButton('x', self)
        # self.del_btn.resize(26, 26)
        # self.del_btn.move(215, 7)
        self.gridLayout.addWidget(self.tag_body, 0, 0, 1, 5)  # row column row_span column_span
        self.gridLayout.addWidget(self.del_btn, 0, 4, 1, 1)
        self.del_btn.setStyleSheet("""
            QPushButton{
            background-color: grey;
            border-style: outset;
            border-width: 1px;
            border-radius: 20px;
            border-color: black;
            padding: 2px;
            }
            """)

    def add_tag(self, new: Tag):
        self.tags.append(new)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.undo = QtWidgets.QPushButton(self.centralwidget)
        self.undo.setObjectName("undo")
        self.gridLayout.addWidget(self.undo, 3, 0, 1, 1)
        self.forward = QtWidgets.QPushButton(self.centralwidget)
        self.forward.setObjectName("forward")
        self.gridLayout.addWidget(self.forward, 3, 1, 1, 1)
        self.update = QtWidgets.QPushButton(self.centralwidget)
        self.update.setObjectName("update")
        self.gridLayout.addWidget(self.update, 3, 2, 1, 1)
        self.gridLayout.addWidget(self.update, 3, 2, 1, 1)
        self.site = QtWidgets.QLineEdit(self.centralwidget)
        self.site.setObjectName("site")
        self.gridLayout.addWidget(self.site, 3, 3, 1, 15)
        self.web = QWebEngineView()
        self.web.setObjectName("web")
        self.gridLayout.addWidget(self.web, 4, 0, 155, 18)
        MainWindow.setCentralWidget(self.centralwidget)

        # self.btn = QPushButton()
        # self.btn.setObjectName("test")
        # self.gridLayout.addWidget(self.btn, 0, 0, 1, 1)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "My Browser (pre-alpha edition)"))
        self.undo.setText(_translate("MainWindow", "<-"))
        self.forward.setText(_translate("MainWindow", "->"))
        self.update.setText(_translate("MainWindow", "update"))
        # self.site.setText(_translate("MainWindow", "https://google.com "))


class WebEnginePage(QWebEnginePage):
    def createWindow(self, _type):
        page = WebEnginePage(self)
        page.urlChanged.connect(self.on_url_changed)
        return page

    @pyqtSlot(QUrl)
    def on_url_changed(self, url):
        page = self.sender()
        self.setUrl(url)
        page.deleteLater()


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        # self.master_tags = [Master_Tag('Недавние', [Tag('ya.ru'), Tag('google.com'),
        #                                             Tag('apple.com')]),
        #                     Master_Tag('Учеба',
        #                                [Tag('wikipedia.com'), Tag('wolframalpha.com'),
        #                                 Tag('dnevnik.ru')])]  # потом из БД доставать буду
        # текущие вкладки надо хранить в виде индексов дабы избежать проблем с ссылками на переменные и копирование и удаление
        self.current_master_index = 0  # тоже достаьт из бд
        self.current_tag_index = 0  # ну и это

        self.max_tag_count = 6

        super().__init__()
        self.setupUi(self)


        self.setGeometry(1, 1, 1, 1)
        self.start_browser()

    def start_browser(self):
        # print('start')
        self.con = sqlite3.connect('BrowserDB.db')
        self.cur = self.con.cursor()
        # self.clear_db()
        self.master_tags = self.import_tags()
        self.make_master_tags()
        self.make_all_tags()
        self.hide_all_tags()
        self.show_current_tags()
        self.site.setText(self.master_tags[self.current_master_index].tags[self.current_tag_index].url)
        self.update_web()
        self.site.returnPressed.connect(self.update_web)
        self.update.pressed.connect(self.update_web)
        self.web.urlChanged.connect(self.change_url_line)
        self.undo.pressed.connect(self.undo_func)
        self.forward.pressed.connect(self.forward_func)
        # print('end')

    def clear_db(self):
        self.cur.execute("DELETE FROM Tags WHERE is_deleted=True")
        self.cur.execute("DELETE FROM Masters WHERE is_deleted=True")

    def import_tags(self):
        master_tags = []
        data = self.cur.execute("SELECT title, tags, id FROM Masters").fetchall()
        for elem in data:
            tags = []
            for tag_id in elem[1].split(';'):
                tag_data = self.cur.execute("SELECT url, id FROM Tags WHERE id=?", (tag_id,)).fetchall()
                # print(tag_data)
                tags.append(Tag(tag_data[0][0], tag_data[0][1]))
            master_tags.append(Master_Tag(elem[0], tags, elem[2]))
        return master_tags


    def make_master_tags(self):
        for i in range(len(self.master_tags)):  # создаем все мастер-теги в дизайне
            self.gridLayout.addWidget(self.master_tags[i], 0, i * 2, 1, 2)
            self.master_tags[i].tag_body.pressed.connect(self.change_master)
            self.master_tags[i].del_btn.pressed.connect(self.delete_master)
            self.master_tags[i].tag_body.index = i
            self.master_tags[i].del_btn.index = i

    def show_current_master_tags(self):
        g = 0

        for i in range(len(self.master_tags)):
            if not self.master_tags[i].is_deleted:
                self.master_tags[i].show()
                if g >= 1:
                    self.gridLayout.removeWidget(self.master_tags[i])
                    self.gridLayout.addWidget(self.master_tags[i], 1, 2 * (i - g), 1, 2)
            else:
                g += 1
                # del self.master_tags[i]

    def delete_master(self):
        not_deleted_tag = sum([0 if i.is_deleted else 1 for i in self.master_tags[self.sender().index]])
        if not_deleted_tag > 1:
            self.master_tags[self.sender().index].is_deleted = True
            master_id = self.master_tags[self.sender().index].id
            self.cur.execute("UPDATE Masters SET is_deleted=True WHERE id=?", (master_id, ))
            self.show_current_master_tags()
            self.current_master_index = 0   # брать из истории
            self.current_tag_index = 0  # тоже брать из истории ОБРАБАТЫВАТЬ ЗАКРЫТЫЕ ВКЛАДКИ
            self.hide_all_master()
            self.show_current_master_tags()
            self.site.setText(self.master_tags[self.current_master_index].tags[self.current_tag_index].url)
            self.update_web()


    def delete_all_current_tags(self):  # убираем все тэги из поля зрения пользователя
        for i in range(len(self.master_tags[self.current_master_index].tags)):
            # self.master_tags[self.current_master_index].tags[i].hide()
            self.gridLayout.removeWidget(self.master_tags[self.current_master_index].tags[i])
            sip.delete(self.master_tags[self.current_master_index].tags[i])
            self.master_tags[self.current_master_index].tags[i].deleteLater()

    def show_current_tags(self):  # показываем тэги текущего мастер-тэга
        g = 0
        # print(self.master_tags[0], [i.url + ' ' + str(i.is_deleted) for i in self.master_tags[0].tags])
        # print(self.master_tags[1], [i.url + ' ' + str(i.is_deleted) for i in self.master_tags[1].tags])
        # print(self.current_master_index)
        for i in range(len(self.master_tags[self.current_master_index].tags)):
            if not self.master_tags[self.current_master_index].tags[i].is_deleted:
                self.master_tags[self.current_master_index].tags[i].show()
                if g >= 1:
                    self.gridLayout.removeWidget(self.master_tags[self.current_master_index].tags[i])
                    self.gridLayout.addWidget(self.master_tags[self.current_master_index].tags[i], 1, 2 * (i - g), 1, 2)
            else:
                g += 1
        deleted_num = sum([0 if i.is_deleted else 1 for i in self.master_tags[self.current_master_index].tags])
        if deleted_num < self.max_tag_count:  # создание кнопочки для добавления вкладки в текущий мастер
            #   deleted_num = sum([1 if i.is_deleted else 0 for i in self.master_tags[self.current_master_index].tags])
            #   print(deleted_num)
            try:
                self.add_btn.hide()
            except Exception:
                pass
            self.add_btn = QPushButton('+')
            self.gridLayout.addWidget(self.add_btn, 1, 2 * deleted_num, 1, 1)
            self.add_btn.pressed.connect(self.create_tag)

    # del self.master_tags[self.current_master_index].tags[i]

    def create_tag(self):
        new_id = self.cur.execute("SELECT id FROM Tags ORDER BY id DESC LIMIT 1").fetchall()[0][0] + 1
        print(new_id)
        self.master_tags[self.current_master_index].add_tag(Tag('google.com', new_id))
        print('hello')
        self.cur.execute("INSERT INTO Tags values (?, ?, ?)", (new_id, 'google.com', False, ))
        print('here')
        not_deleted_num = sum([0 if i.is_deleted else 1 for i in self.master_tags[self.current_master_index]])
        self.current_tag_index = not_deleted_num - 1
        not_deleted_num = sum([0 if i.is_deleted else 1 for i in self.master_tags[self.current_master_index].tags])
        self.gridLayout.addWidget(self.master_tags[self.current_master_index].tags[-1], 1, 2 * (not_deleted_num - 1), 1,
                                  2)
        self.master_tags[self.current_master_index].tags[self.current_tag_index].tag_body.pressed.connect(
            self.click_tag)
        self.master_tags[self.current_master_index].tags[self.current_tag_index].del_btn.pressed.connect(
            self.delete_tag)
        self.master_tags[self.current_master_index].tags[self.current_tag_index].tag_body.index = self.current_tag_index
        self.master_tags[self.current_master_index].tags[self.current_tag_index].del_btn.index = self.current_tag_index
        self.master_tags[self.current_master_index].tags[
            self.current_tag_index].del_btn.master_index = self.current_master_index
        self.add_btn.hide()

        self.show_current_tags()
        # fgprint('added')
        self.update_web()

    def make_all_tags(self):
        for j in range(len(self.master_tags)):
            for i in range(len(self.master_tags[j].tags)):  # а здесь создаем все тэги
                self.gridLayout.addWidget(self.master_tags[j].tags[i], 1, i * 2, 1, 2)
                self.master_tags[j].tags[i].tag_body.url = self.master_tags[j].tags[i].url
                self.master_tags[j].tags[i].tag_body.pressed.connect(self.click_tag)
                self.master_tags[j].tags[i].del_btn.pressed.connect(self.delete_tag)
                self.master_tags[j].tags[i].tag_body.index = i
                self.master_tags[j].tags[i].del_btn.index = i
                self.master_tags[j].tags[i].del_btn.master_index = j
                # self.master_tags[self.current_master_index].tags[i].is_deleted = False

    def hide_all_tags(self):
        for j in range(len(self.master_tags)):
            for i in range(len(self.master_tags[j].tags)):  # а здесь прячем все тэги
                self.master_tags[j].tags[i].hide()

    def hide_all_master(self):
        for i in range(len(self.master_tags)):
            self.master_tags[i].hide()

    def make_tags(self):  # создаем все тэги текущнго мастер-тэга
        self.master_tags[self.current_master_index].tags = [i for i in self.master_tags[self.current_master_index].tags
                                                            if i is not None]
        # print(self.master_tags[self.current_master_index].tags, self.current_master_index)
        for i in range(len(self.master_tags[self.current_master_index].tags)):  # а здесь создаем все тэги
            self.gridLayout.addWidget(self.master_tags[self.current_master_index].tags[i], 1, i * 2, 1, 2)
            self.master_tags[self.current_master_index].tags[i].tag_body.url = \
                self.master_tags[self.current_master_index].tags[i].url
            self.master_tags[self.current_master_index].tags[i].tag_body.pressed.connect(self.click_tag)
            self.master_tags[self.current_master_index].tags[i].del_btn.pressed.connect(self.delete_tag)
            self.master_tags[self.current_master_index].tags[i].tag_body.index = i
            self.master_tags[self.current_master_index].tags[i].del_btn.index = i

    def change_master(self):
        self.current_master_index = self.sender().index
        self.current_tag_index = 0
        self.site.setText(self.master_tags[self.current_master_index].tags[self.current_tag_index].url)
        self.hide_all_tags()
        self.show_current_tags()
        self.update_web()

    def click_tag(self):
        new_url = self.sender().url
        self.site.setText(new_url)
        self.current_tag_index = self.sender().index  # self.master_tags[self.master_tags_index]self.sender()
        self.master_tags[self.current_master_index].tags[self.current_tag_index].update_site_name()
        self.update_web()

    def delete_tag(self):  # еще все индексы переназначить
        print(self.sender().master_index)
        deleted_num = sum([0 if i.is_deleted else 1 for i in self.master_tags[self.sender().master_index].tags])
        if deleted_num > 1:
            self.master_tags[self.sender().master_index].tags[self.sender().index].is_deleted = True
            tag_id = self.master_tags[self.sender().master_index].tags[self.sender().index].id
            self.cur.execute("UPDATE Tags SET is_deleted=True WHERE id=?", (tag_id, ))
            self.current_tag_index = 0  # брать из истории
            self.hide_all_tags()
            self.show_current_tags()
            self.site.setText(self.master_tags[self.sender().master_index].tags[self.current_tag_index].url)
            self.update_web()
            # print(self.master_tags[self.sender().master_index].tags[self.sender().index], self.sender().master_index)

    def update_web(self):
        url = self.site.text()
        if 'https://' in url:
            url = url[8:]
        url = url.strip()
        if '' in url.split('.') or ' ' in url:
            url = 'google.com/search?q=' + '+'.join(url.split())
        page = WebEnginePage(self.web)
        self.web.setPage(page)
        self.web.load(QUrl('https://' + url))
        self.site.setText('https://' + url)
        self.web.show()
        # self.master_tags[self.current_master_index].tags[self.current_tag_index].update_site_name()

    def change_url_line(self):
        new_url = self.web.url().toString()
        self.master_tags[self.current_master_index].tags[self.current_tag_index].url = new_url
        self.master_tags[self.current_master_index].tags[self.current_tag_index].tag_body.url = new_url
        self.master_tags[self.current_master_index].tags[self.current_tag_index].update_site_name()
        self.site.setText(new_url)

    def undo_func(self):
        self.web.back()

    def forward_func(self):
        self.web.forward()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
