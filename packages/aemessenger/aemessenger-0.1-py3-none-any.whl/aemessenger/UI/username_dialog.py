from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox


class UsernameDialog(QDialog):
    def __init__(self, parent=None):
        super(UsernameDialog, self).__init__(parent)

        self.setWindowTitle('Enter username')
        layout = QVBoxLayout(self)

        # поле для имени
        self.username_edit = QLineEdit(self)
        layout.addWidget(self.username_edit)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # Получить имя из диалога
    def username(self):
        return self.username_edit.text()

    # Создать диалог и вернуть юзернейм
    @staticmethod
    def get_username(parent=None):
        dialog = UsernameDialog(parent)
        result = dialog.exec_()
        name = dialog.username()
        return name, result == QDialog.Accepted
