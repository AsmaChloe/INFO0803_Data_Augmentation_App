from random import randint
import numpy
from keras import layers
from keras.layers import RandomCrop, RandomContrast, RandomTranslation, RandomBrightness, RandomRotation, RandomFlip, RandomZoom
from keras.preprocessing.image import ImageDataGenerator
from numpy import expand_dims

def zoom(image : numpy.ndarray, height_range : tuple, width_range : tuple, n : int, fill_mode : str = 'nearest') -> list[numpy.ndarray] :
    """
    Zoom in and out of the image by a random amount in the range specified by height_range and width_range
    :param image: numpy array of the image
    :param height_range: range of the zoom height, must be a tuple, between -1 and 1
    :param width_range: range of the zoom width, must be a tuple, between -1 and 1
    :param n: number of images to generate ; must be greater than 0
    :param fill_mode: fill mode for the zoom ; must be one of the following: 'constant', 'nearest', 'reflect', 'wrap' ; default is 'nearest'
    :return: list of numpy arrays of the images
    """
    assert isinstance(height_range, tuple) and len(height_range) == 2 and height_range[0] <= height_range[1] and -1 <= height_range[0] <= 1 and -1 <= height_range[1] <= 1
    assert isinstance(width_range, tuple) and len(width_range) == 2 and width_range[0] <= width_range[1] and -1 <= width_range[0] <= 1 and -1 <= width_range[1] <= 1
    assert isinstance(n, int) and n > 0

    zoom_function = RandomZoom(height_range, width_range, fill_mode=fill_mode)

    augmented_images = []
    for i in range(n):
        augmented_images.append(zoom_function(image).numpy().astype('uint8'))

    return augmented_images

def flip(image : numpy.ndarray, horizontal : bool, vertical : bool, n : int) -> list[numpy.ndarray] :
    """
    Flip the image horizontally and/or vertically
    :param image: numpy array of the image
    :param horizontal: boolean, if True, flip horizontally
    :param vertical: boolean, if True, flip vertically
    :param n: number of images to generate ; must be greater than 0
    :return: list of numpy arrays of the images
    """
    assert isinstance(n, int) and n > 0
    flip_function = RandomFlip(mode='horizontal_and_vertical' if horizontal and vertical else 'horizontal' if horizontal else 'vertical')

    augmented_images = []
    for i in range(n):
        augmented_images.append(flip_function(image).numpy().astype('uint8'))

    return augmented_images

def rotate( image : numpy.ndarray, angle_range : tuple,  n : int, fill_mode : str = 'nearest') -> list[numpy.ndarray] :
    """
    Rotate the image by a random angle in the range specified by angle_range
    :param image: numpy array of the image
    :param angle_range: range of the rotation angle, must be a tuple, between -1 and 1, represent percentage of 360 degrees
    :param n: number of images to generate ; must be greater than 0
    :param fill_mode: fill mode for the rotation ; must be one of the following: 'constant', 'nearest', 'reflect', 'wrap' ; default is 'nearest'
    :return: list of numpy arrays of the images
    """
    assert isinstance(angle_range, tuple) and len(angle_range) == 2 and angle_range[0] <= angle_range[1] and -1 <= angle_range[0] <= 1 and -1 <= angle_range[1] <= 1
    assert isinstance(n, int) and n > 0

    rotation_function = RandomRotation(angle_range, fill_mode=fill_mode)

    augmented_images = []
    for i in range(n):
        augmented_images.append(rotation_function(image).numpy().astype('uint8'))

    return augmented_images

def brightness(image : numpy.ndarray, brightness_range : tuple, n : int) -> list[numpy.ndarray] :
    """
    Change the brightness of the image by a random amount in the range specified by brightness_range
    :param image: numpy array of the image
    :param brightness_range: range of the brightness change, must be a tuple, between -1 and 1
    :param n: number of images to generate ; must be greater than 0
    :return: list of numpy arrays of the images
    """
    assert isinstance(brightness_range, tuple) and len(brightness_range) == 2 and brightness_range[0] <= brightness_range[1] and -1 <= brightness_range[0] <= 1 and -1 <= brightness_range[1] <= 1
    assert isinstance(n, int) and n > 0

    brightness_function = RandomBrightness(brightness_range)

    augmented_images = []
    for i in range(n):
        augmented_images.append(brightness_function(image).numpy().astype('uint8'))

    return augmented_images

def shift(image : numpy.ndarray, x_range : tuple, y_range : tuple, n : int, fill_mode : str = 'nearest') -> list[numpy.ndarray] :
    """
    Shift the image in x and y direction. The shift is random and in the range specified by x_range and y_range.
    :param image: numpy array of the image
    :param x_range: range of the shift in x direction, must be between -1 and 1
    :param y_range: range of the shift in y direction, must be between -1 and 1
    :param n: number of images to generate ; must be greater than 0
    :param fill_mode: Points outside the boundaries of the input are filled according to the given mode (one of {"constant", "reflect", "wrap", "nearest"}). Default is 'nearest'.
    :return:
    """
    assert isinstance(x_range, tuple) and len(x_range)==2 and -1 <= x_range[0] <= 1 and -1 <= x_range[1] <= 1 and x_range[0] <= x_range[1]
    assert isinstance(y_range, tuple) and len(y_range)==2 and -1 <= y_range[0] <= 1 and -1 <= y_range[1] <= 1 and y_range[0] <= y_range[1]
    assert isinstance(n, int) and n > 0

    translation = RandomTranslation(height_factor=y_range, width_factor=x_range, fill_mode=fill_mode)

    augmented_images = []
    for i in range(n):
        augmented_images.append(translation(image).numpy().astype('uint8'))

    return augmented_images

def shear(image : numpy.ndarray, shear_value : float, n : int) -> list[numpy.ndarray] :
    """
    Change the perspective of the image by providing a distortion along the x-axis and y-axis between [-shear_value, shear_value]
    :param image: numpy array of the image
    :param shear_value: value of the shear, must be between 0 and 360
    :param n: number of images to generate ; must be greater than 0
    :return: list of numpy arrays of the images
    """
    assert isinstance(shear_value, int) and 360 > shear_value > 0
    assert isinstance(n, int) and n > 0

    datagen = ImageDataGenerator(shear_range=shear_value)

    if len(image.shape) == 3:
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

def channel_shift(image : numpy.ndarray, intensity : int, n : int) -> list[numpy.ndarray] :
    """
    Shift the channels of the image, each channel of an image (red, green, blue) is shifted by a random value between range [-intensity;+intensity]. The shift value is added to each pixel value in the channel, which can result in a new color tone and brightness for the image.
    :param image: numpy array of the image
    :param intensity: intensity of the shift ; must be between 0 and 200
    :param n: number of images to generate ; must be greater than 0
    :return: list of numpy arrays of the images
    """
    assert isinstance(intensity, int) and 200 > intensity > 0
    assert isinstance(n, int) and n > 0

    datagen = ImageDataGenerator(channel_shift_range=intensity)

    if len(image.shape) == 3:
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

def resize(image : numpy.ndarray, width_range : tuple, height_range : tuple, n : int) -> numpy.ndarray :
    """
    Randomly resize the image according to the width and height range provided
    :param image: numpy array of the image
    :param width_range: range of the width ; must be a tuple of 2 integers and width_range[1] >= width_range[0] > 0
    :param height_range: range of the height ; must be a tuple of 2 integers and height_range[1] >= height_range[0] > 0
    :param n: number of images to generate ; must be greater than 0 and an integer
    :return: list of numpy arrays of the images
    """
    assert isinstance(width_range, tuple) and len(width_range) == 2 and width_range[1] >= width_range[0] > 0
    assert isinstance(height_range, tuple) and len(height_range) == 2 and height_range[1] >= height_range[0] > 0
    assert isinstance(n, int) and n > 0

    augmented_images = []
    for i in range(n):
        resize_function = layers.Resizing(randint(width_range[0], width_range[1]),
                                          randint(height_range[0], height_range[1]))
        augmented_images.append(resize_function(image).numpy().astype('uint8'))

    return augmented_images

def crop(image : numpy.ndarray, height : int, width : int, n : int) -> numpy.ndarray :
    """
    Randomly crop the image according to the width and height range provided
    :param image: numpy array of the image
    :param height: height of the crop ; must be greater than 0 and an integer
    :param width: width of the crop ; must be greater than 0 and an integer
    :param n: number of images to generate ; must be greater than 0 and an integer
    :return: list of numpy arrays of the images
    """
    assert height > 0 and width > 0 and isinstance(height, int) and isinstance(width, int)
    assert isinstance(n, int) and n > 0

    crop_function = RandomCrop(height, width)

    augmented_images = []
    for i in range(n):
        augmented_images.append(crop_function(image).numpy().astype('uint8'))

    return augmented_images

def contrast(image : numpy.ndarray, contrast_range : tuple, n : int) -> numpy.ndarray :
    """
    Randomly change the contrast of the image
    :param image: numpy array of the image
    :param contrast_range: range of the contrast, a tuple of two floats, lower bound must be greater or equal to 0
    :param n: number of images to generate ; must be greater than 0 and an integer
    :return: list of numpy arrays of the images
    """
    assert isinstance(contrast_range, tuple) and len(contrast_range) == 2 and contrast_range[0] >= 0
    assert isinstance(n, int) and n > 0

    contrast_function = RandomContrast(factor=(contrast_range[0], contrast_range[1]))
    augmented_images = []
    for i in range(n):
        augmented_images.append(contrast_function(image).numpy().astype('uint8'))

    return augmented_images