import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

from keras_preprocessing.image import load_img, img_to_array, array_to_img

from augmentation import fonctions


class Interface(QWidget):

    def __init__(self):
        super().__init__()

        self.status_label = None
        self.folder_path = ''
        self.list_widget = None
        self.transformation_selector = None
        self.initUI()

    def __init__(self):
        super().__init__()

        self.status_label = None
        self.folder_path = ''
        self.list_widget = None
        self.transformation_selector = None
        self.initUI()

    def initUI(self):

        self.setGeometry(300, 300, 600, 640)
        self.setWindowTitle('Data Augmentation')
        self.setWindowIcon(QIcon('folder_icon.png'))

        # Changer la couleur de fond
        self.setStyleSheet("background-color: #A4A6D5;")

        # Ajout d'une liste
        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(10, 40, 580, 300)
        self.list_widget.setStyleSheet("background-color: #F5F5F5; border: 1px solid #DDDDDD;")

        # Boîte de dialogue de sélection de dossier
        try:
            self.folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))
            sys.exit()

        # Ajout des fichiers image dans la liste
        for file_name in os.listdir(self.folder_path):
            if os.path.splitext(file_name)[1].lower() in ['.jpg', '.png', '.gif', '.bmp']:
                item = QListWidgetItem(file_name, self.list_widget)
                try:
                    item.setIcon(QIcon(QPixmap(os.path.join(self.folder_path, file_name))))
                except Exception as e:
                    QMessageBox.warning(self, 'Error', str(e))
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)

        # Titre
        title = QLabel('Files in selected folder:', self)
        title.setGeometry(10, 10, 580, 30)
        title.setStyleSheet("font-weight: bold; font-size: 16px;")

        # Ajout du menu déroulant
        self.transformation_selector = QComboBox(self)
        self.transformation_selector.addItems(
            ["Zoom", "Translate", "Flip", "Rotate", "Brightness", "Resize", "Scale", "Blur", "Noise", "Contrast",
             "Crop"])
        self.transformation_selector.setGeometry(10, 350, 580, 30)
        self.transformation_selector.setStyleSheet("background-color: white; border: 1px solid #DDDDDD;"
                                                   "font-size: 14px; padding-left: 5px;")
        self.transformation_selector.currentIndexChanged.connect(self.resetUi)

        # Ajout du bouton "Modifier"
        modifier_button = QPushButton("Modifier", self)
        modifier_button.setGeometry(10, 560, 580, 30)
        modifier_button.setStyleSheet("")
        modifier_button.clicked.connect(self.on_modifier_button_clicked)

        # Ajout du bouton "Tout cocher"
        tout_cocher_button = QPushButton("Tout cocher", self)
        tout_cocher_button.setGeometry(10, 600, 580, 30)
        tout_cocher_button.clicked.connect(self.on_cocher_button_clicked)

        self.show()

    def handle_error(self, error):
        QMessageBox.warning(self, 'Error', str(error))

    def on_cocher_button_clicked(self):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setCheckState(Qt.Checked)

    def get_checked_items(self):
        checked_items = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.Checked:
                checked_items.append(item.text())
        return checked_items

    def on_modifier_button_clicked(self):
        selected_transform = self.transformation_selector.currentText()

        if selected_transform == "Zoom":
            self.on_Zoom_clicked()
        elif selected_transform == "Translate":
            self.on_Translate_clicked()
        elif selected_transform == "Flip":
            self.on_Flip_clicked()
        elif selected_transform == "Rotate":
            self.on_Rotate_clicked()
        elif selected_transform == "Brightness":
            self.on_Brightness_clicked()
        elif selected_transform == "Resize":
            self.on_Resize_clicked()
        elif selected_transform == "Scale":
            self.on_Scale_clicked()
        elif selected_transform == "Blur":
            self.on_Blur_clicked()
        elif selected_transform == "Noise":
            self.on_Noise_clicked()
        elif selected_transform == "Contrast":
            self.on_Contrast_clicked()
        elif selected_transform == "Crop":
            self.on_Crop_clicked()
        else:
            self.handle_error("Invalid transformation selected.")

    def save_images(self, images):
        # fonction pour enregistrer les images zoomées
        for i, image in enumerate(images):
            image = array_to_img(image)
            path = self.folder_path + f'/zoomed_{i}.jpg'
            image.save(path)
        # Ajouter un QLabel pour afficher le message
        message_label = QLabel("Images enregistrées!", self)
        message_label.setGeometry(120, 490, 580, 30)
        message_label.show()

    def resetUi(self):
        # Supprimer les messages QLabel
        for child in self.children():
            if isinstance(child, QLabel) and child.text() != "Files in selected folder:":
                child.deleteLater()

        # Supprimer les boutons "Modifier" et "Enregistrer"
        for child in self.children():
            if isinstance(child, QPushButton) and child.text() == ["Modifier","Enregistrer"]:
                child.deleteLater()

    def on_Zoom_clicked(self):
        if len(self.get_checked_items()) == 0:
            self.handle_error("No images selected.")
            return

        zoomed_images = []
        for i in range(len(self.get_checked_items())):
            path = self.folder_path + '/' + self.get_checked_items()[i]
            # chargement de l'image
            img = load_img(path)
            # conversion en numpy array
            data = img_to_array(img)
            liste = fonctions.zoom(image=data, height_range=(0.5, 0.5), width_range=(0.5, 0.5), n=2)
            for j in liste:
                zoomed_images.append(j)

        # Ajouter un QLabel pour afficher le message
        message_label = QLabel("Images modifiées!", self)
        message_label.setGeometry(10, 450, 580, 30)
        message_label.show()

        # Ajouter un bouton "Enregistrer"
        save_button = QPushButton("Enregistrer", self)
        save_button.setGeometry(10, 490, 100, 30)
        print(zoomed_images)
        save_button.clicked.connect(lambda: self.save_images(zoomed_images))
        save_button.show()

    def on_Translate_clicked(self):
        pass

    def on_Flip_clicked(self):
        pass

    def on_Rotate_clicked(self):
        pass

    def on_Brightness_clicked(self):
        pass

    def on_Resize_clicked(self):
        pass

    def on_Scale_clicked(self):
        pass

    def on_Blur_clicked(self):
        pass

    def on_Noise_clicked(self):
        pass

    def on_Contrast_clicked(self):
        pass

    def on_Crop_clicked(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Interface()
    sys.exit(app.exec_())
