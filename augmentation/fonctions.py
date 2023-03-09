from random import random, randint

import keras
import tensorflow as tf
import numpy
from keras import layers
from keras.backend import squeeze
from keras.layers import GaussianNoise, Conv2D
from keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot as plt
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

def shift(image : numpy.ndarray, width_shift_range : float, height_shift_range : float, n : int) -> list[numpy.ndarray] :
    """
    Shift the image
    :param image: numpy array of the image
    :param width_shift_range: range of the shift in x direction, must be between -2 and 2
    :param height_shift_range: range of the shift in y direction, must be between -2 and 2
    :param n: number of images to generate
    :return: list of numpy arrays of the images
    """
    assert isinstance(width_shift_range, float) or isinstance(width_shift_range, int)
    assert isinstance(height_shift_range, float) or isinstance(height_shift_range, int)
    assert width_shift_range < 2 and width_shift_range > -2 # Lower bound chosen arbitrarily
    assert height_shift_range < 2 and height_shift_range > -2 # Lower bound chosen arbitrarily

    datagen = ImageDataGenerator(width_shift_range=width_shift_range, height_shift_range=height_shift_range)

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

def shear(image : numpy.ndarray, shear_value : float, n : int) -> list[numpy.ndarray] :
    """
    Change the perspective of the image by providing a distortion along the x-axis and y-axis
    :param image: numpy array of the image
    :param shear_value: value of the shear, must be between 0 and 360
    :param n: number of images to generate
    :return: list of numpy arrays of the images
    """
    assert isinstance(shear_value, float) or isinstance(shear_value, int)
    assert shear_value < 360 and shear_value > 0

    datagen = ImageDataGenerator(shear_range=shear_value)

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

def channel_shift(image : numpy.ndarray, intensity : float, n : int) -> list[numpy.ndarray] :
    """
    Shift the channels of the image, each channel of an image (red, green, blue) is shifted by a random value between range [-intensity;+intensity]. The shift value is added to each pixel value in the channel, which can result in a new color tone and brightness for the image.
    :param image: numpy array of the image
    :param intensity: intensity of the shift ; must be between 0 and 200
    :param n: number of images to generate
    :return: list of numpy arrays of the images
    """
    assert isinstance(intensity, float) or isinstance(intensity, int)
    assert intensity < 200 and intensity > 0

    datagen = ImageDataGenerator(channel_shift_range=intensity)

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

def custom_resize(image, width_range, height_range) -> numpy.ndarray :
    """
    Utility function to resize the image using a custom function
    :param image: numpy array of the image
    :param width_range: range of the width
    :param height_range: range of the height
    :return: numpy array of the image
    """
    func = keras.Sequential([
        layers.Resizing(randint(width_range[0], width_range[1]), randint(height_range[0], height_range[1])),
        layers.Rescaling(1. / 255)
    ])
    #The colormap is determined by two rules. If the image values are integers, they use a scale from [0, 255]. If the type is a float, it is mapped from [0.0, 1.0].
    # When scaling, resize will covert integers to floats, but does not rescale the values. This can result in values from [0.0, 255.0] which throws the colormap out of whack.
    # To remedy, you can either cast the values back to int or scale the values from [0.0, 1.0] using tf.keras.layers.experimental.preprocessing.Rescaling(1./255).

    return func(image)
def resize(image : numpy.ndarray, width_range : tuple, height_range : tuple, n : int) -> numpy.ndarray :
    """
    Randomly resize the image according to the width and height range provided
    :param image: numpy array of the image
    :param width_range: range of the width
    :param height_range: range of the height
    :param n: number of images to generate
    :return: list of numpy arrays of the images
    """
    assert isinstance(width_range, tuple)
    assert isinstance(height_range, tuple)
    assert len(width_range) == 2
    assert len(height_range) == 2

    augmented_images = []
    for i in range(n):
        augmented_images.append(custom_resize(image, width_range, height_range))

    return augmented_images

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