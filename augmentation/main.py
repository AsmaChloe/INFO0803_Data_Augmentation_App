from keras_preprocessing.image import load_img, img_to_array
from matplotlib import pyplot as plt

from fonctions import *

# path to image
path = "C:/Users/user/Pictures/gerber-and-rose-2-1544099.jpg"
# load the image
img = load_img(path)
# convert to numpy array
data = img_to_array(img)

n = 2
augmented_images = resize(data,(100,500), (200,300), n)

# display the images
for i in range(n):
    plt.subplot(1,2, i+1)
    plt.imshow(augmented_images[i])
plt.subplots_adjust(wspace=0.5)
plt.show()