import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QListWidget, QPushButton, \
    QGridLayout, QListWidgetItem, QLabel
from PyQt5.QtGui import QIcon, QPixmap


class FolderSelector(QWidget):

    def __init__(self):
        super().__init__()

        self.list_widget = None
        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 600, 500)
        self.setWindowTitle('Select Folder')
        self.setWindowIcon(QIcon('folder_icon.png'))

        # Ajout d'une liste
        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(10, 40, 580, 300)
        self.list_widget.setStyleSheet("background-color: #F5F5F5; border: 1px solid #DDDDDD;")

        # Boîte de dialogue de sélection de dossier
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')

        # Ajout des fichiers image dans la liste
        for file_name in os.listdir(folder_path):
            if os.path.splitext(file_name)[1].lower() in ['.jpg', '.png', '.gif', '.bmp']:
                item = QListWidgetItem(file_name, self.list_widget)
                item.setIcon(QIcon(QPixmap(os.path.join(folder_path, file_name))))

        # Titre
        title = QLabel('Files in selected folder:', self)
        title.setGeometry(10, 10, 580, 30)
        title.setStyleSheet("font-weight: bold;")

        # Ajout des boutons
        button_layout = QGridLayout()
        for i in range(1, 12):
            button = QPushButton('Button {}'.format(i), self)
            button.setFixedSize(100, 50)
            button.clicked.connect(getattr(self, 'on_button_{}_clicked'.format(i)))
            row = (i - 1) // 3
            col = (i - 1) % 3
            button_layout.addWidget(button, row, col)

        button_widget = QWidget(self)
        button_widget.setLayout(button_layout)
        button_widget.setGeometry(10, 360, 580, 120)

        self.show()

    def on_button_1_clicked(self):
        print('bouton 1')

    def on_button_2_clicked(self):
        pass

    def on_button_3_clicked(self):
        pass

    def on_button_4_clicked(self):
        pass

    def on_button_5_clicked(self):
        pass

    def on_button_6_clicked(self):
        pass

    def on_button_7_clicked(self):
        pass

    def on_button_8_clicked(self):
        pass

    def on_button_9_clicked(self):
        pass

    def on_button_10_clicked(self):
        pass

    def on_button_11_clicked(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FolderSelector()
    sys.exit(app.exec_())
