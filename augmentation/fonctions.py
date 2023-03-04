import numpy
from keras.preprocessing.image import ImageDataGenerator
from numpy import expand_dims

def zoom(image : numpy.ndarray, zoom_range : list, n : int) -> list[numpy.ndarray] :
    """
    Zoom in and out of the image
    :param image: numpy array of the image
    :param zoom_range: list containing the zoom range, zoom_range[0] is lower bound, zoom_range[1] is upper bound
    :param n: number of images to generate
    :return: list of numpy arrays of the images
    """
    if(len(zoom_range) != 2):
        raise ValueError("Zoom range must contain 2 values")
    if(zoom_range[0] < 0) :
        raise ValueError("Zoom range lower bound mist be positive")

    datagen = ImageDataGenerator(zoom_range=zoom_range)

    image = expand_dims(image, 0)
    it = datagen.flow(image, batch_size=1)

    augmented_images = []
    for i in range(n):
        # generate batch of images
        batch = it.next()
        # convert to unsigned integers for viewing
        image = batch[0].astype('uint8')
        augmented_images.append(image)

    return augmented_images

def translate(image, tx : float, ty : float, n : int) -> list[numpy.ndarray] :
    """
    Translate the image
    :param image: numpy array of the image
    :param tx: translation in x direction
    :param ty: translation in y direction
    :param n: number of images to generate
    :return: list of numpy arrays of the images
    """
    datagen = ImageDataGenerator(width_shift_range=tx, height_shift_range=ty)

    image = expand_dims(image, 0)
    it = datagen.flow(image, batch_size=1)

    augmented_images = []
    for i in range(n):
        # generate batch of images
        batch = it.next()
        # convert to unsigned integers for viewing
        image = batch[0].astype('uint8')
        augmented_images.append(image)

    return augmented_images

def flip(image : numpy.ndarray, horizontal : bool, vertical : bool, n : int) -> list[numpy.ndarray] :
    """
    Flip the image
    :param image: numpy array of the image
    :param horizontal: flip horizontally
    :param vertical: flip vertically
    :param n: number of images to generate
    :return: list of numpy arrays of the images
    """
    datagen = ImageDataGenerator(horizontal_flip=horizontal, vertical_flip=vertical)

    image = expand_dims(image, 0)
    it = datagen.flow(image, batch_size=1)

    augmented_images = []
    for i in range(n):
        # generate batch of images
        batch = it.next()
        # convert to unsigned integers for viewing
        image = batch[0].astype('uint8')
        augmented_images.append(image)

    return augmented_images

def rotate(image, angle : int, n : int) -> list[numpy.ndarray] :
    """
    Rotate the image
    :param image: numpy array of the image
    :param angle: angle of rotation
    :param n: number of images to generate
    :return: list of numpy arrays of the images
    """
    datagen = ImageDataGenerator(rotation_range=angle)

    image = expand_dims(image, 0)
    it = datagen.flow(image, batch_size=1)

    augmented_images = []
    for i in range(n):
        # generate batch of images
        batch = it.next()
        # convert to unsigned integers for viewing
        image = batch[0].astype('uint8')
        augmented_images.append(image)

    return augmented_images

def brightness(image, brightness_range : list, n : int) -> list[numpy.ndarray] :
    """
    Change the brightness of the image
    :param image: numpy array of the image
    :param brightness_percentage: percentage of brightness change
    :param n: number of images to generate
    :return: list of numpy arrays of the images
    """
    datagen = ImageDataGenerator(brightness_range=brightness_range)

    image = expand_dims(image, 0)
    it = datagen.flow(image, batch_size=1)

    augmented_images = []
    for i in range(n):
        # generate batch of images
        batch = it.next()
        # convert to unsigned integers for viewing
        image = batch[0].astype('uint8')
        augmented_images.append(image)

    return augmented_images

def resize(image : numpy.ndarray, width : int, height : int) -> numpy.ndarray :
    pass

def scale(image):
    pass

def blur(image):
    pass

def noise(image):
    pass

def contrast(image):
    pass

def crop(image : numpy.ndarray):
    pass

def shift(image : numpy.ndarray, ):
    pass