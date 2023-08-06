import sys
import textwrap
import os
import base64
from PIL import Image, ImageQt
from aemessenger.Client.clientcontroller import ClientController
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QByteArray, QBuffer, QIODevice, QJsonValue, qUncompress, QModelIndex
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QMessageBox, QLabel, QVBoxLayout, QStackedLayout, QHBoxLayout, QFileDialog
from aemessenger.UI.add_contact_dialog import AddContactDialog
from aemessenger.UI.username_dialog import UsernameDialog
from aemessenger.JIM.jimmsg import JIMUserMsg, JIMMessageBuilder, JIMChatMsg


class ClientWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.package_dir = os.path.abspath(os.path.dirname(__file__))
        self.ui_path = os.path.join(self.package_dir, 'UI', 'client.ui')
        self.standard_icon_path = os.path.join(self.package_dir, 'Img', 'user.png')
        self.icon_new_msg_path = os.path.join(self.package_dir, 'Img', 'user_new_msg.png')
        self.window = uic.loadUi(self.ui_path)
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

        self.window.avatarLabel.mousePressEvent = self.select_avatar
        pixmap = QPixmap(self.standard_icon_path)
        pixmap_scaled = pixmap.scaled(40, 40, Qt.KeepAspectRatio)
        self.window.avatarLabel.setPixmap(pixmap_scaled)

        self.window.show()

    def get_contacts(self):
        self.contacts.clear()
        result = self.controller.get_contacts()
        if result < 0:
            show_error_msg('Contacts not found', QMessageBox.Warning)
            return
        names = self.controller.db.get_contacts()
        for name in names:
            item = QStandardItem(name)
            item.setEditable(False)
            font = item.font()
            font.setPointSize(15)
            item.setFont(font)
            item.setIcon(QIcon(self.standard_icon_path))
            self.contacts.appendRow(item)
        self.contacts.sort(0)
        self.fill_chat_layouts(names)
        self.load_history()
        # Select first contact
        index = self.contacts.index(0, 0, QModelIndex())
        self.window.contactListView.setCurrentIndex(index)
        try:
            self.contact_selected(index)
        except KeyError as e:
            pass  # nothing happened

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
            chat_widget = QWidget()
            layout = QVBoxLayout()
            layout.addStretch(1)
            layout.setContentsMargins(0, 0, 0, 0)
            chat_widget.setLayout(layout)
            self.chat_stackedLayout.addWidget(chat_widget)
            self.chat_layout_indexes[name] = [index, layout]
            index += 1

    def contact_selected(self, modelindex):
        # Поменять заголовок при клике на контакт (nameLabel)
        name = str(self.window.contactListView.model().itemData(modelindex)[0])
        self.window.nameLabel.setText(name)
        # Поменять иконку, на случай если пришло новое сообщение и она зеленая
        contact_item = self.contacts.findItems(name)
        contact_item[0].setIcon(QIcon(self.standard_icon_path))
        # Выбрать лэйаут чата этого контакта
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
            self.add_gui_msg(name, text, is_left=False, is_new=False)  # добавить в gui
        result = self.controller.send_user_msg(text, name)
        # Успешно отправлено?
        if result == 0:
            self.window.textEdit.clear()
        else:
            show_error_msg('Not delivered', QMessageBox.Warning)

    def add_gui_msg(self, name, text, is_left, is_new):
        msg = MsgBubble(text, is_left)
        if is_left:  # Входящее сообщение
            if name not in self.chat_layout_indexes:  # Если контакта нет в базе, то добавим его
                self.controller.add_contact(name)
                self.get_contacts()
            contact_items = self.contacts.findItems(name)
            if is_new:
                contact_items[0].setIcon(QIcon(self.icon_new_msg_path))
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
            is_new = False if jimmsg.to == self.controller.username else True
            self.add_gui_msg(jimmsg.account, jimmsg.message, left, is_new=is_new)
        elif type(jimmsg) is JIMChatMsg:
            raise NotImplemented
        self.controller.add_user_msg_to_db(jimmsg)

    def select_avatar(self, event):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "Image Files (*.png *.jpeg *.jpg);;All Files (*)", options=options)
        pixmap = ''
        size = 40, 40
        if file_name:
            image = Image.open(file_name)
            image.thumbnail(size)  # Сжать до 100px c сохранением пропорций
            pil_image = ImageQt.ImageQt(image)
            qt_image = QtGui.QImage(pil_image)
            pixmap = QPixmap.fromImage(qt_image)
            # self.window.avatarLabel.setPixmap(pixmap)  # что-то не работает с JPG - черная фотка=/

            # преобразовать в байты
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            buffer.open(QIODevice.WriteOnly)
            pixmap.save(buffer, 'PNG')
            encoded_bytes = buffer.data().toBase64()
            encoded_str = str(encoded_bytes).replace('b\'', '').replace('\'', '')

            # Отправить в базу
            self.controller.send_avatar_to_server(encoded_str)
            # И теперь вытащить и установить
            self.get_avatar_from_server()

    def get_avatar_from_server(self):
        data = self.controller.get_avatar_from_server(self.controller.username)
        if data != -1:
            img_bytes = QByteArray.fromBase64(data.encode('ascii'))
            pixmap = QPixmap()
            pixmap.loadFromData(img_bytes, 'PNG')
            # pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio)
            self.window.avatarLabel.setPixmap(pixmap)

    def load_history(self):
        for name in self.chat_layout_indexes.keys():
            history = self.controller.db.get_last_history(name, self.controller.username)
            for msg in history:
                is_left = msg.to_username == self.controller.username
                self.add_gui_msg(name, msg.msg, is_left, is_new=False)


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
    client.window.selfnameLabel.setText(username)

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
    client.get_avatar_from_server()

    sys.exit(app.exec_())

if __name__ == '__main__':
    mainloop()