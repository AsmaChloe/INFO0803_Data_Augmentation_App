import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt, QByteArray
from keras_preprocessing.image import load_img, img_to_array, array_to_img
from augmentation import fonctions
from superqt import QRangeSlider
from qtrangeslider.qtcompat import QtCore


class Interface(QWidget):

    def __init__(self):
        super().__init__()

        ## QWIDGETS ##
        self.list_widget = None

        # Labels
        self.label1 = None
        self.label2 = None
        self.label3 = None
        self.label4 = None
        self.label5 = None
        self.label6 = None
        self.label7 = None
        self.label8 = None
        self.value_label1 = None
        self.value_label2 = None
        self.status_label = None
        self.message_label = None

        # LineEdit
        self.le1 = None
        self.le2 = None
        self.le3 = None
        self.le4 = None
        self.le5 = None
        self.le6 = None

        self.n = None

        # Checkbox
        self.cb1 = None
        self.cb2 = None

        # Slider
        self.sl1 = None
        self.sl2 = None

        # ComboBox
        self.fm = None
        self.transformation_selector = None

        # Button
        self.reset_button = None
        self.save_button = None

        # Booléens utilisées pour savoir si les widgets de la sélection existent déjà
        self.shear = False
        self.zoom = False
        self.flip = False
        self.channel_shift = False
        self.crop = False
        self.resize = False

        self.im = None
        self.scroll = None
        self.name = None
        self.modifiedOnce = False
        self.modifiedImages = []
        self.folder_path = ''

        self.initUI()

    def initUI(self):

        # Création de la fenêtre
        self.setGeometry(300, 300, 1200, 640)
        self.setWindowTitle('Data Augmentation')
        self.setWindowIcon(QIcon('folder_icon.png'))

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
            ["Zoom", "Flip", "Rotate", "Brightness", "Shift", "Shear", "Channel_shift", "Resize", "Crop",
             "Contrast"])
        self.transformation_selector.setGeometry(10, 350, 580, 30)
        self.transformation_selector.setStyleSheet("background-color: white; border: 1px solid #DDDDDD;"
                                                   "font-size: 14px; padding-left: 5px;")
        self.transformation_selector.currentIndexChanged.connect(self.on_Index_changed)

        # Ajout du bouton "Modifier"
        modifier_button = QPushButton("Modifier", self)
        modifier_button.setGeometry(10, 560, 580, 30)
        modifier_button.setStyleSheet("")
        modifier_button.clicked.connect(self.on_modifier_button_clicked)

        # Ajout du bouton "Tout cocher"
        tout_cocher_button = QPushButton("Tout cocher", self)
        tout_cocher_button.setGeometry(10, 600, 290, 30)
        tout_cocher_button.clicked.connect(self.on_cocher_button_clicked)

        # Ajout du bouton "Tout décocher"
        tout_cocher_button = QPushButton("Tout décocher", self)
        tout_cocher_button.setGeometry(310, 600, 280, 30)
        tout_cocher_button.clicked.connect(self.on_decocher_button_clicked)

        self.on_Zoom_index()

        self.show()

    def handle_error(self, error):
        QMessageBox.warning(self, 'Error', str(error))

    def on_cocher_button_clicked(self):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setCheckState(Qt.Checked)

    def on_decocher_button_clicked(self):
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setCheckState(Qt.Unchecked)

    def on_reset_button_clicked(self):
        self.modifiedImages = []
        for child in self.children():
            if isinstance(child, QPushButton) and child.text() not in ["Modifier", "Tout cocher", "Tout décocher"]:
                child.hide()
            if isinstance(child, QLabel) and child.text() == "Images modifiées!":
                child.hide()

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
        elif selected_transform == "Flip":
            self.on_Flip_clicked()
        elif selected_transform == "Rotate":
            self.on_Rotate_clicked()
        elif selected_transform == "Brightness":
            self.on_Brightness_clicked()
        elif selected_transform == "Shift":
            self.on_Shift_clicked()
        elif selected_transform == "Shear":
            self.on_Shear_clicked()
        elif selected_transform == "Channel_shift":
            self.on_Channel_shift_clicked()
        elif selected_transform == "Resize":
            self.on_Resize_clicked()
        elif selected_transform == "Crop":
            self.on_Crop_clicked()
        elif selected_transform == "Contrast":
            self.on_Contrast_clicked()
        else:
            self.handle_error("Invalid transformation selected.")

    def save_images(self):
        # fonction pour enregistrer les images zoomées
        for i, image in enumerate(self.modifiedImages):
            image = array_to_img(image)
            path = self.folder_path + f'/{self.name}_{i}.jpg'
            image.save(path)

        # Affichage du message Images enregistrées
        QMessageBox.information(self, 'Bravo !', "Vos images ont bien été enregistrées")

    def resetUi(self):
        # Reset des boutons en les cachant via l'attribut hide
        for child in self.children():
            if isinstance(child, QLabel) and child.text() != "Files in selected folder:":
                child.hide()
            if isinstance(child, QRangeSlider):
                child.hide()
            if isinstance(child, QComboBox) and child != self.transformation_selector:
                child.hide()
            if isinstance(child, QLineEdit):
                child.hide()
            if isinstance(child, QPushButton) and child.text() not in ["Enregistrer", "Reset", "Modifier",
                                                                       "Tout cocher", "Tout décocher"]:
                child.deleteLater()
            if isinstance(child, QCheckBox):
                child.hide()

    def on_Index_changed(self):
        self.resetUi()
        selected_transform = self.transformation_selector.currentText()

        if selected_transform == "Zoom":
            self.on_Zoom_index()
        elif selected_transform == "Flip":
            self.on_Flip_index()
        elif selected_transform == "Rotate":
            self.on_Rotate_index()
        elif selected_transform == "Brightness":
            self.on_Brightness_index()
        elif selected_transform == "Shift":
            self.on_Shift_index()
        elif selected_transform == "Shear":
            self.on_Shear_index()
        elif selected_transform == "Channel_shift":
            self.on_Channel_shift_index()
        elif selected_transform == "Resize":
            self.on_Resize_index()
        elif selected_transform == "Crop":
            self.on_Crop_index()
        elif selected_transform == "Contrast":
            self.on_Contrast_index()

        else:
            self.handle_error("Invalid transformation selected.")

    def on_Zoom_clicked(self):
        if len(self.get_checked_items()) == 0:
            self.handle_error("No images selected.")
            return
        if self.n.text() is None or self.n.text().isdigit() is not True:
            self.handle_error("Select a valid images number")
            return

        zoomed_images = []
        if len(self.modifiedImages) > 0:
            for i in range(len(self.modifiedImages)):
                data = self.modifiedImages[i]
                liste = fonctions.zoom(image=data,
                                       height_range=(self.sl1.value()[0] / 50 - 1, self.sl1.value()[1] / 50 - 1),
                                       width_range=(self.sl2.value()[0] / 50 - 1, self.sl2.value()[1] / 50 - 1),
                                       n=int(self.n.text()), fill_mode=self.fm.currentText())
                for j in liste:
                    zoomed_images.append(j)
        else:
            for i in range(len(self.get_checked_items())):
                path = self.folder_path + '/' + self.get_checked_items()[i]
                # chargement de l'image
                img = load_img(path)
                # conversion en numpy array
                data = img_to_array(img)
                liste = fonctions.zoom(image=data,
                                       height_range=(self.sl1.value()[0] / 50 - 1, self.sl1.value()[1] / 50 - 1),
                                       width_range=(self.sl2.value()[0] / 50 - 1, self.sl2.value()[1] / 50 - 1),
                                       n=int(self.n.text()), fill_mode=self.fm.currentText())
                for j in liste:
                    zoomed_images.append(j)

        self.modifiedImages = zoomed_images
        self.name = "Zoom"
        self.modified()

    def on_Flip_clicked(self):
        if len(self.get_checked_items()) == 0:
            self.handle_error("No images selected.")
            return
        if self.n.text() is None or self.n.text().isdigit() is not True:
            self.handle_error("Select a valid images number")
            return

        flipped_images = []
        if len(self.modifiedImages) > 0:
            for i in range(len(self.modifiedImages)):
                data = self.modifiedImages[i]
                liste = fonctions.flip(image=data,
                                       horizontal=self.cb1.isChecked(),
                                       vertical=self.cb2.isChecked(),
                                       n=int(self.n.text()))
                for j in liste:
                    flipped_images.append(j)
        else:
            for i in range(len(self.get_checked_items())):
                path = self.folder_path + '/' + self.get_checked_items()[i]
                # chargement de l'image
                img = load_img(path)
                # conversion en numpy array
                data = img_to_array(img)
                liste = fonctions.flip(image=data,
                                       horizontal=self.cb1.isChecked(),
                                       vertical=self.cb2.isChecked(),
                                       n=int(self.n.text()))
                for j in liste:
                    flipped_images.append(j)

        self.modifiedImages = flipped_images
        self.name = "Flip"
        self.modified()

    def on_Rotate_clicked(self):
        if len(self.get_checked_items()) == 0:
            self.handle_error("No images selected.")
            return
        if self.n.text() is None or self.n.text().isdigit() is not True:
            self.handle_error("Select a valid images number")
            return

        rotated_images = []
        if len(self.modifiedImages) > 0:
            for i in range(len(self.modifiedImages)):
                data = self.modifiedImages[i]
                liste = fonctions.rotate(image=data,
                                         angle_range=(self.sl1.value()[0] / 50 - 1, self.sl1.value()[1] / 50 - 1),
                                         n=int(self.n.text()))
                for j in liste:
                    rotated_images.append(j)
        else:
            for i in range(len(self.get_checked_items())):
                path = self.folder_path + '/' + self.get_checked_items()[i]
                # chargement de l'image
                img = load_img(path)
                # conversion en numpy array
                data = img_to_array(img)
                liste = fonctions.rotate(image=data,
                                         angle_range=(self.sl1.value()[0] / 50 - 1, self.sl1.value()[1] / 50 - 1),
                                         n=int(self.n.text()))
                for j in liste:
                    rotated_images.append(j)

        self.modifiedImages = rotated_images
        self.name = "Rotate"
        self.modified()

    def on_Brightness_clicked(self):
        if len(self.get_checked_items()) == 0:
            self.handle_error("No images selected.")
            return
        if self.n.text() is None or self.n.text().isdigit() is not True:
            self.handle_error("Select a valid images number")
            return

        bright_images = []
        if len(self.modifiedImages) > 0:
            for i in range(len(self.modifiedImages)):
                data = self.modifiedImages[i]
                liste = fonctions.brightness(image=data,
                                             brightness_range=(
                                                 self.sl1.value()[0] / 50 - 1, self.sl1.value()[1] / 50 - 1),
                                             n=int(self.n.text()))
                for j in liste:
                    bright_images.append(j)
        else:
            for i in range(len(self.get_checked_items())):
                path = self.folder_path + '/' + self.get_checked_items()[i]
                # chargement de l'image
                img = load_img(path)
                # conversion en numpy array
                data = img_to_array(img)
                liste = fonctions.brightness(image=data,
                                             brightness_range=(
                                                 self.sl1.value()[0] / 50 - 1, self.sl1.value()[1] / 50 - 1),
                                             n=int(self.n.text()))
                for j in liste:
                    bright_images.append(j)

        self.modifiedImages = bright_images
        self.name = "Bright"
        self.modified()

    def on_Shift_clicked(self):
        if len(self.get_checked_items()) == 0:
            self.handle_error("No images selected.")
            return
        if self.n.text() is None or self.n.text().isdigit() is not True:
            self.handle_error("Select a valid images number")
            return

        shifted_images = []
        if len(self.modifiedImages) > 0:
            for i in range(len(self.modifiedImages)):
                data = self.modifiedImages[i]
                liste = fonctions.shift(image=data,
                                        x_range=(self.sl1.value()[0] / 50 - 1, self.sl1.value()[1] / 50 - 1),
                                        y_range=(self.sl1.value()[0] / 50 - 1, self.sl1.value()[1] / 50 - 1),
                                        n=int(self.n.text()))
                for j in liste:
                    shifted_images.append(j)
            self.modified(shifted_images, "Shift")
            return
        else:
            for i in range(len(self.get_checked_items())):
                path = self.folder_path + '/' + self.get_checked_items()[i]
                # chargement de l'image
                img = load_img(path)
                # conversion en numpy array
                data = img_to_array(img)
                liste = fonctions.shift(image=data,
                                        x_range=(self.sl1.value()[0] / 50 - 1, self.sl1.value()[1] / 50 - 1),
                                        y_range=(self.sl1.value()[0] / 50 - 1, self.sl1.value()[1] / 50 - 1),
                                        n=int(self.n.text()))
                for j in liste:
                    shifted_images.append(j)

        self.modifiedImages = shifted_images
        self.name = "Shift"
        self.modified()

    def on_Shear_clicked(self):
        if len(self.get_checked_items()) == 0:
            self.handle_error("No images selected.")
            return
        if self.n.text() is None or self.n.text().isdigit() is not True:
            self.handle_error("Select a valid images number")
            return
        if self.le1.text() is None or self.le1.text().isdigit() is not True or float(self.le1.text()) < 0 or float(
                self.le1.text()) > 360:
            self.handle_error("Select a valid shear value")
            return
        sheared_images = []
        if len(self.modifiedImages) > 0:
            for i in range(len(self.modifiedImages)):
                data = self.modifiedImages[i]
                liste = fonctions.shear(image=data,
                                        shear_value=int(self.le1.text()),
                                        n=int(self.n.text()))
                for j in liste:
                    sheared_images.append(j)

        else:
            for i in range(len(self.get_checked_items())):
                path = self.folder_path + '/' + self.get_checked_items()[i]
                # chargement de l'image
                img = load_img(path)
                # conversion en numpy array
                data = img_to_array(img)
                liste = fonctions.shear(image=data,
                                        shear_value=int(self.le1.text()),
                                        n=int(self.n.text()))
                for j in liste:
                    sheared_images.append(j)

        self.modifiedImages = sheared_images
        self.name = "Shear"
        self.modified()

    def on_Channel_shift_clicked(self):
        if len(self.get_checked_items()) == 0:
            self.handle_error("No images selected.")
            return
        if self.n.text() is None or self.n.text().isdigit() is not True:
            self.handle_error("Select a valid images number")
            return

        shifted_images = []
        if len(self.modifiedImages) > 0:
            for i in range(len(self.modifiedImages)):
                data = self.modifiedImages[i]
                liste = fonctions.channel_shift(image=data,
                                                intensity=int(self.le1.text()),
                                                n=int(self.n.text()))
                for j in liste:
                    shifted_images.append(j)
        else:
            for i in range(len(self.get_checked_items())):
                path = self.folder_path + '/' + self.get_checked_items()[i]
                # chargement de l'image
                img = load_img(path)
                # conversion en numpy array
                data = img_to_array(img)
                liste = fonctions.channel_shift(image=data,
                                                intensity=int(self.le1.text()),
                                                n=int(self.n.text()))
                for j in liste:
                    shifted_images.append(j)

        self.modifiedImages = shifted_images
        self.name = "Channel shift"
        self.modified()

    def on_Resize_clicked(self):
        if len(self.get_checked_items()) == 0:
            self.handle_error("No images selected.")
            return
        if self.n.text() is None or self.n.text().isdigit() is not True:
            self.handle_error("Select a valid images number")
            return
        if self.le3.text() is None or self.le3.text().isdigit() is False or self.le4.text() is None or self.le4.text().isdigit() is False:
            self.handle_error("Select valid resize values")
            return
        if self.le5.text() is None or self.le5.text().isdigit() is False or self.le6.text() is None or self.le6.text().isdigit() is False:
            self.handle_error("Select valid resize values")
            return
        if int(self.le3.text()) < 0 or int(self.le4.text()) < 0 or int(self.le5.text()) < 0 or int(self.le6.text()) < 0:
            self.handle_error("Select valid resize values")
            return
        if int(self.le3.text()) > int(self.le4.text()) or int(self.le5.text()) > int(self.le6.text()):
            self.handle_error("Select valid resize values")
            return

        resized_images = []
        if len(self.modifiedImages) > 0:
            for i in range(len(self.modifiedImages)):
                data = self.modifiedImages[i]
                width = (int(self.le3.text()), int(self.le4.text()))
                height = (int(self.le5.text()), int(self.le6.text()))
                liste = fonctions.resize(image=data,
                                         width_range=width,
                                         height_range=height,
                                         n=int(self.n.text()))
                for j in liste:
                    resized_images.append(j)
        else:
            for i in range(len(self.get_checked_items())):
                path = self.folder_path + '/' + self.get_checked_items()[i]
                # chargement de l'image
                img = load_img(path)
                # conversion en numpy array
                data = img_to_array(img)
                width = (int(self.le3.text()), int(self.le4.text()))
                height = (int(self.le5.text()), int(self.le6.text()))
                liste = fonctions.resize(image=data,
                                         width_range=width,
                                         height_range=height,
                                         n=int(self.n.text()))
                for j in liste:
                    resized_images.append(j)

        self.modifiedImages = resized_images
        self.name = "Resize"
        self.modified()

    def on_Crop_clicked(self):
        if len(self.get_checked_items()) == 0:
            self.handle_error("No images selected.")
            return
        if self.n.text() is None or self.n.text().isdigit() is not True:
            self.handle_error("Select a valid images number")
            return

        croped_images = []
        if len(self.modifiedImages) > 0:
            for i in range(len(self.modifiedImages)):
                data = self.modifiedImages[i]
                liste = fonctions.crop(image=data,
                                       height=int(self.le1.text()),
                                       width=int(self.le2.text()),
                                       n=int(self.n.text()))
                for j in liste:
                    croped_images.append(j)
        else:
            for i in range(len(self.get_checked_items())):
                path = self.folder_path + '/' + self.get_checked_items()[i]
                # chargement de l'image
                img = load_img(path)
                # conversion en numpy array
                data = img_to_array(img)
                liste = fonctions.crop(image=data,
                                       height=int(self.le1.text()),
                                       width=int(self.le2.text()),
                                       n=int(self.n.text()))
                for j in liste:
                    croped_images.append(j)

        self.modifiedImages = croped_images
        self.name = "Crop"
        self.modified()

    def on_Contrast_clicked(self):
        if len(self.get_checked_items()) == 0:
            self.handle_error("No images selected.")
            return
        if self.n.text() is None or self.n.text().isdigit() is False:
            self.handle_error("Select a valid images number")
            return

        if self.le1.text() is None or self.le1.text().isdigit() is False or self.le2.text() is None or self.le2.text().isdigit() is False:
            self.handle_error("Select valid contrast values")
            return
        if int(self.le1.text()) < 0 or int(self.le2.text()) < int(self.le1.text()):
            self.handle_error("Select valid contrast values")
            return

        contrasted_images = []
        if len(self.modifiedImages) > 0:
            for i in range(len(self.modifiedImages)):
                data = self.modifiedImages[i]
                contrast = (int(self.le1.text()), int(self.le2.text()))
                liste = fonctions.contrast(image=data,
                                           contrast_range=contrast,
                                           n=int(self.n.text()))
                for j in liste:
                    contrasted_images.append(j)
        else:
            for i in range(len(self.get_checked_items())):
                path = self.folder_path + '/' + self.get_checked_items()[i]
                # chargement de l'image
                img = load_img(path)
                # conversion en numpy array
                data = img_to_array(img)
                contrast = (int(self.le1.text()), int(self.le2.text()))
                liste = fonctions.contrast(image=data,
                                           contrast_range=contrast,
                                           n=int(self.n.text()))
                for j in liste:
                    contrasted_images.append(j)

        self.modifiedImages = contrasted_images
        self.name = "Contrast"
        self.modified()

    def modified(self):
        if self.modifiedOnce:
            self.message_label.show()
            self.save_button.show()
            self.reset_button.show()

            qimg = QImage(self.modifiedImages[0].data, self.modifiedImages[0].shape[1], self.modifiedImages[0].shape[0],
                          self.modifiedImages[0].shape[1] * 3, QImage.Format_RGB888)
            qpixmap = QPixmap.fromImage(qimg)
            label = QLabel(self)
            label.setPixmap(qpixmap)
            self.scroll.setWidget(label)
            self.scroll.show()
            return

        # Ajouter un QLabel pour afficher le message
        self.message_label = QLabel("Images modifiées!", self)
        self.message_label.setGeometry(150, 520, 580, 30)
        self.message_label.show()

        # Ajouter un bouton "Enregistrer"
        self.save_button = QPushButton("Enregistrer", self)
        self.save_button.setGeometry(10, 520, 100, 30)
        self.save_button.clicked.connect(lambda: self.save_images())
        self.save_button.show()

        # Ajout du bouton "Reset"
        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setGeometry(490, 520, 100, 30)
        self.reset_button.clicked.connect(self.on_reset_button_clicked)
        self.reset_button.show()

        # Création du label pour stocker l'image
        qimg = QImage(self.modifiedImages[0].data, self.modifiedImages[0].shape[1], self.modifiedImages[0].shape[0],
                      self.modifiedImages[0].shape[1] * 3, QImage.Format_RGB888)
        qpixmap = QPixmap.fromImage(qimg)
        label = QLabel(self)
        label.setPixmap(qpixmap)

        # Création d'un QScrollArea et y placer le QLabel
        self.scroll = QScrollArea(self)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(label)
        self.scroll.setGeometry(650, 40, 520, 520)
        self.scroll.show()

        self.modifiedOnce = True

    # Modification du sélecteur de transformation

    def on_Zoom_index(self):

        if self.zoom:
            self.sl1.show()
            self.sl1.setValue((33, 66))
            self.sl2.show()
            self.sl2.setValue((33, 66))
            self.label1.show()
            self.value_label1.show()
            self.label2.show()
            self.value_label2.show()
            self.label3.show()
            self.n.show()
            self.label4.show()
            self.fm.show()
            return

        # HEIGHT RANGE SLIDER
        self.label1 = QLabel("Height_range :", self)
        self.label1.setGeometry(10, 400, 80, 30)

        self.sl1 = QRangeSlider(QtCore.Qt.Horizontal, self)
        self.sl1.setValue((33, 66))
        self.sl1.setGeometry(10, 450, 150, 30)

        # Ajouter un QLabel pour afficher la valeur actuelle du slider
        self.value_label1 = QLabel(f"{self.sl1.value()[0] * 2 - 99, self.sl1.value()[1] * 2 - 99}", self)
        self.value_label1.setGeometry(100, 400, 120, 30)
        self.value_label1.setStyleSheet("font-size: 14px;")

        # Connecter le signal valueChanged du slider avec la fonction update_value_label
        self.sl1.valueChanged.connect(lambda: self.update_value_label1(self.value_label1))

        # WIDTH RANGE SLIDER

        self.label2 = QLabel("Width_range :", self)
        self.label2.setGeometry(200, 400, 80, 30)

        self.sl2 = QRangeSlider(QtCore.Qt.Horizontal, self)
        self.sl2.setValue((33, 66))
        self.sl2.setGeometry(190, 450, 150, 30)

        # Ajouter un QLabel pour afficher la valeur actuelle du slider
        self.value_label2 = QLabel(f"{self.sl2.value()[0] * 2 - 99, self.sl2.value()[1] * 2 - 99}", self)
        self.value_label2.setGeometry(290, 400, 120, 30)
        self.value_label2.setStyleSheet("font-size: 14px;")

        # Connecter le signal valueChanged du slider avec la fonction update_value_label
        self.sl2.valueChanged.connect(lambda: self.update_value_label2(self.value_label2))

        # N QLINE EDIT

        self.label3 = QLabel("Number of \n  images :", self)
        self.label3.setGeometry(370, 390, 50, 60)

        self.n = QLineEdit(self)
        self.n.setMaxLength(2)
        self.n.setPlaceholderText("N")
        self.n.setGeometry(370, 450, 50, 30)

        # FILL MODE SELECTOR

        self.label4 = QLabel("Fill mode :", self)
        self.label4.setGeometry(470, 390, 50, 60)

        self.fm = QComboBox(self)
        self.fm.addItems(
            ['constant', 'nearest', 'reflect', 'wrap'])
        self.fm.setGeometry(450, 450, 100, 30)
        self.fm.setStyleSheet("background-color: white; border: 1px solid #DDDDDD;"
                              "font-size: 14px; padding-left: 5px;")
        self.zoom = True

    def update_value_label1(self, label):
        label.setText(f"{self.sl1.value()[0] * 2 - 99, self.sl1.value()[1] * 2 - 99}")

    def update_value_label2(self, label):
        label.setText(f"{self.sl2.value()[0] * 2 - 99, self.sl2.value()[1] * 2 - 99}")

    def on_Flip_index(self):
        if self.flip:
            self.cb1.show()
            self.cb2.show()
            self.n.clear()
            self.n.show()
            self.label3.show()
            return

        # HORIZONTAL FLIP

        self.cb1 = QCheckBox("Horizontal flip", self)
        self.cb1.setGeometry(30, 450, 150, 30)

        # VERTICAL FLIP

        self.cb2 = QCheckBox("Vertical flip", self)
        self.cb2.setGeometry(190, 450, 150, 30)

        self.cb1.show()
        self.cb2.show()
        self.label3.show()
        self.n.show()

    def on_Rotate_index(self):
        self.label1.setText("Angle range :")
        self.value_label1.show()
        self.label1.show()
        self.sl1.show()
        self.label3.show()
        self.label4.show()
        self.fm.show()
        self.n.show()

    def on_Brightness_index(self):
        self.label1.setText("Brightness range :")
        self.value_label1.show()
        self.label1.show()
        self.sl1.show()
        self.label3.show()
        self.n.show()

    def on_Shift_index(self):
        self.sl1.setValue((33, 66))
        self.sl1.show()
        self.sl2.setValue((33, 66))
        self.sl2.show()
        self.label1.setText("X range :")
        self.label1.show()
        self.value_label1.show()
        self.label2.setText("Y range :")
        self.label2.show()
        self.value_label2.show()
        self.label3.show()
        self.n.show()
        self.label4.show()
        self.fm.show()

    def on_Shear_index(self):
        if self.shear:
            self.label3.show()
            self.n.show()
            self.label5.setText("Value of the shear between 0 and 360")
            self.label5.show()
            self.le1.setGeometry(200, 450, 50, 30)
            self.le1.setPlaceholderText("sh")
            self.le1.show()
            return

        self.label5 = QLabel("Value of the shear between 0 and 360", self)
        self.label5.setGeometry(130, 400, 200, 30)

        self.le1 = QLineEdit(self)
        self.le1.setMaxLength(3)
        self.le1.setPlaceholderText("sh")
        self.le1.setGeometry(200, 450, 50, 30)

        self.label3.show()
        self.n.show()
        self.label5.show()
        self.le1.show()

        self.shear = True

    def on_Channel_shift_index(self):
        if self.channel_shift:
            self.label3.show()
            self.n.show()
            self.label6.setText("Value of the Channel shift between 0 and 200")
            self.label6.show()
            self.le1.setPlaceholderText("int")
            self.le1.setGeometry(200, 450, 50, 30)
            self.le1.show()
            return

        self.label6 = QLabel("Value of the intensity between 0 and 200", self)
        self.label6.setGeometry(110, 400, 250, 30)

        self.le1 = QLineEdit(self)
        self.le1.setMaxLength(3)
        self.le1.setPlaceholderText("int")
        self.le1.setGeometry(200, 450, 50, 30)

        self.label3.show()
        self.n.show()
        self.label6.show()
        self.le1.show()

        self.channel_shift = True

    def on_Resize_index(self):
        if self.resize:
            self.le3.show()
            self.le4.show()
            self.label1.show()
            self.label2.show()
            self.label3.show()
            self.n.show()
            return

        self.label1.setText("Width range :")
        self.label1.show()

        self.le3 = QLineEdit(self)
        self.le3.setMaxLength(3)
        self.le3.setPlaceholderText("min")
        self.le3.setGeometry(10, 450, 30, 30)
        self.le3.show()

        self.le4 = QLineEdit(self)
        self.le4.setMaxLength(3)
        self.le4.setPlaceholderText("max")
        self.le4.setGeometry(50, 450, 30, 30)
        self.le4.show()

        self.label2.setText("Height range :")
        self.label2.show()

        self.le5 = QLineEdit(self)
        self.le5.setMaxLength(3)
        self.le5.setPlaceholderText("min")
        self.le5.setGeometry(200, 450, 30, 30)
        self.le5.show()

        self.le6 = QLineEdit(self)
        self.le6.setMaxLength(3)
        self.le6.setPlaceholderText("max")
        self.le6.setGeometry(240, 450, 30, 30)
        self.le6.show()

        self.label3.show()
        self.n.show()

    def on_Crop_index(self):
        if self.crop:
            self.label7.show()
            self.label8.show()
            self.label3.show()
            self.n.show()
            self.le1.setPlaceholderText("H")
            self.le1.setGeometry(140, 450, 50, 30)
            self.le1.show()
            self.le2.show()
            return

        self.label7 = QLabel("Height of the crop", self)
        self.label7.setGeometry(130, 400, 200, 30)

        self.le1 = QLineEdit(self)
        self.le1.setMaxLength(3)
        self.le1.setPlaceholderText("H")
        self.le1.setGeometry(140, 450, 50, 30)

        self.label8 = QLabel("Width of the crop", self)
        self.label8.setGeometry(250, 400, 200, 30)

        self.le2 = QLineEdit(self)
        self.le2.setMaxLength(3)
        self.le2.setPlaceholderText("W")
        self.le2.setGeometry(260, 450, 50, 30)

        self.label7.show()
        self.label8.show()
        self.n.show()
        self.label3.show()
        self.le1.show()
        self.le2.show()

        self.crop = True

    def on_Contrast_index(self):
        if self.crop:
            self.label7.setText("Contrast min")
            self.label7.show()
            self.label8.setText("Contrast max")
            self.label8.show()
            self.label3.show()
            self.n.show()
            self.le1.setPlaceholderText("H")
            self.le1.setGeometry(140, 450, 50, 30)
            self.le1.show()
            self.le2.show()
            return

        self.label7 = QLabel("Contrast min", self)
        self.label7.setGeometry(130, 400, 200, 30)

        self.le1 = QLineEdit(self)
        self.le1.setMaxLength(3)
        self.le1.setPlaceholderText("min")
        self.le1.setGeometry(140, 450, 50, 30)

        self.label8 = QLabel("Contrast max", self)
        self.label8.setGeometry(250, 400, 200, 30)

        self.le2 = QLineEdit(self)
        self.le2.setMaxLength(3)
        self.le2.setPlaceholderText("max")
        self.le2.setGeometry(260, 450, 50, 30)

        self.label7.show()
        self.label8.show()
        self.n.show()
        self.label3.show()
        self.le1.show()
        self.le2.show()

        self.crop = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Interface()
    sys.exit(app.exec_())
