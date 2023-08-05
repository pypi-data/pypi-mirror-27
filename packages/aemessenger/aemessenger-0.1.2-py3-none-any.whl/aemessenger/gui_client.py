import sys
import textwrap
import os
from aemessenger.Client.clientcontroller import ClientController
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox, QLabel, QVBoxLayout, QStackedLayout, QHBoxLayout
from aemessenger.UI.add_contact_dialog import AddContactDialog
from aemessenger.UI.username_dialog import UsernameDialog
from aemessenger.JIM.jimmsg import JIMUserMsg, JIMMessageBuilder, JIMChatMsg


class ClientWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.package_dir = os.path.abspath(os.path.dirname(__file__))
        ui_path = os.path.join(self.package_dir, 'UI', 'client.ui')
        self.window = uic.loadUi(ui_path)
        self.contacts = QStandardItemModel(self.window.contactListView)
        self.controller = None  # контроллер клиента
        self.msg_thread = None  # поток обработки входящих сообщений

        # список лэйаутов чата вида 'contact':[index, QVBoxLayout].
        # Каждому контакту свой лэйаут
        self.chat_stackedLayout = QStackedLayout()
        self.chat_layout_indexes = {}

        self.vbar = self.window.chat_scroll.verticalScrollBar()
        self.init_ui()

    def init_ui(self):
        self.window.contactListView.setModel(self.contacts)
        self.window.contactListView.clicked.connect(self.contact_selected)
        self.window.contactListView.setAttribute(Qt.WA_MacShowFocusRect, 0)  # Убрать стремный фокус

        self.window.addContactButton.clicked.connect(self.add_contact)
        self.window.sendButton.clicked.connect(self.send_msg)

        self.window.chat_scroll_widget.setLayout(self.chat_stackedLayout)
        self.window.chat_scroll_widget.setContentsMargins(20, 20, 25, 20)

        self.window.show()

    def get_contacts(self):
        self.contacts.clear()
        result = self.controller.get_contacts()
        if result < 0:
            show_error_msg('Contacts not found', QMessageBox.Warning)
            return
        names = self.controller.db.get_contacts()
        icon_path = os.path.join(self.package_dir, 'Img', 'user.png')
        for name in names:
            item = QStandardItem(name)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(15)
            item.setFont(font)
            item.setIcon(QIcon(icon_path))
            self.contacts.appendRow(item)
        self.contacts.sort(0)
        self.fill_chat_layouts(names)

    def add_contact(self):
        contact, result = AddContactDialog().get_username()
        if contact is '' or result is False:
            return
        self.controller.add_contact(contact)
        self.get_contacts()

    def fill_chat_layouts(self, names):
        index = 0
        for name in names:
            if name in self.chat_layout_indexes:  # добавляем контакт, обновляем индекс
                self.chat_layout_indexes[name][0] = index
                index += 1
                continue
            chatWidget = QWidget()
            layout = QVBoxLayout()
            layout.addStretch(1)
            layout.setContentsMargins(0, 0, 0, 0)
            chatWidget.setLayout(layout)
            self.chat_stackedLayout.addWidget(chatWidget)
            self.chat_layout_indexes[name] = [index, layout]
            index += 1

    def contact_selected(self, modelindex):
        # Поменять заголовок при клике на контакт (nameLabel)
        name = str(self.window.contactListView.model().itemData(modelindex)[0])
        self.window.nameLabel.setText(name)
        i = self.chat_layout_indexes[name][0]
        self.chat_stackedLayout.setCurrentIndex(i)

    def send_msg(self):
        index = self.window.contactListView.selectionModel().selectedIndexes()
        # Выбран ли контакт?
        if len(index) is 0:
            return
        # Есть ли текст сообщения?
        text = self.window.textEdit.toPlainText()
        if not text:
            return
        name = self.window.contactListView.model().itemData(index[0])[0]
        if name != self.controller.username:
            self.add_gui_msg(name, text, False)  # добавить в gui
        result = self.controller.send_user_msg(text, name)
        # Успешно отправлено?
        if result == 0:
            self.window.textEdit.clear()
        else:
            show_error_msg('Not delivered', QMessageBox.Warning)

    def add_gui_msg(self, name, text, is_left):
        msg = MsgBubble(text, is_left)
        if is_left:
            self.chat_layout_indexes[name][1].addWidget(msg)
        else:
            # spacer прижмет сбоку сообщение слева для случая, когда надо сделать пузырь справа
            # а т.к. общий лэйаут вертикальный, то мы засунем spacer и пузырь
            # в горизонтальный лэйаут, а лэйаут в QWidget
            group_line = QWidget()
            horizontal_layout = QHBoxLayout()
            horizontal_layout.addStretch(1)
            spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            horizontal_layout.addItem(spacer)
            horizontal_layout.addWidget(msg)
            horizontal_layout.setContentsMargins(0, 0, 0, 0)
            group_line.setLayout(horizontal_layout)
            self.chat_layout_indexes[name][1].addWidget(group_line)
        # Скролл до упора вниз, но что-то не очень работает
        h = self.window.chat_scroll.height()
        self.vbar.setValue(h*10000)

    def on_msg_recieved(self, jimmsg):
        if type(jimmsg) is JIMUserMsg:
            left = True if jimmsg.to == self.controller.username else False
            self.add_gui_msg(jimmsg.account, jimmsg.message, left)
        elif type(jimmsg) is JIMChatMsg:
            raise NotImplemented


class MsgThread(QThread):
    msg_ready = pyqtSignal(object)

    def __init__(self, client_widget, queue):
        QThread.__init__(self)
        self.client = client_widget
        if not queue:
            self.isAlive = False
        self.queue = queue

    def run(self):
        while True:
            msg = self.queue.get()
            if msg:
                print('recieved msg:', msg)
                jimmsg = JIMMessageBuilder.get_msg_from_json(msg)
                self.msg_ready.emit(jimmsg)
                self.queue.task_done()


class MsgBubble(QLabel):
    """Красивый пузырь для сообщений.
    При is_left == True, покрасится в зеленый"""
    def __init__(self, text, is_left):
        text = textwrap.fill(text, 20)  # разбить текст по 20 знаков, чтобы он влез в пузырь
        super(MsgBubble, self).__init__(text)
        self.is_left = is_left
        width = len(text) * 10 if len(text) < 20 else 200  # Если текст не очень большой, можно сделать пузырь поменьше
        self.setMaximumWidth(width + 10)
        self.setMinimumWidth(width)
        self.setWordWrap(True)
        self.setContentsMargins(5, 5, 5, 5)

    def paintEvent(self, e):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        if self.is_left:
            p.setBrush(Qt.green)
        p.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 8, 8)

        super(MsgBubble, self).paintEvent(e)


def show_error_msg(text, status):
    msg = QMessageBox()
    msg.setText(text)
    msg.setIcon(status)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def mainloop():
    app = QtWidgets.QApplication(sys.argv)
    client = ClientWidget()

    # Получить username
    username, result = UsernameDialog.get_username()
    if username == '' or result is False:
        username = 'Guest'
    print(username)
    title = 'Messenger - ' + username
    print(title)
    client.window.setWindowTitle(title)

    # Создать контроллер
    try:
        client.controller = ClientController(username)
    except ConnectionRefusedError as e:
        show_error_msg('Server is not available', QMessageBox.Critical)
        sys.exit()

    # Отправить presense
    if client.controller.send_presense() < 0:
        show_error_msg('Username already exists', QMessageBox.Critical)
        sys.exit()

    # Подключить поток обработки входящих сообщений msg
    client.msg_thread = MsgThread(client, client.controller.client.msg_queue)
    client.msg_thread.msg_ready.connect(client.on_msg_recieved)
    client.msg_thread.finished.connect(app.exit)
    client.msg_thread.start()

    # Получить список контактов
    client.get_contacts()

    sys.exit(app.exec_())

if __name__ == '__main__':
    mainloop()