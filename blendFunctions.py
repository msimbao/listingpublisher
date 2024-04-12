from PIL import Image
import numpy
from blend_modes import difference
from blend_modes import multiply
from blend_modes import normal

def Multiply(background_img_raw,foreground_img_raw):
    '''
    Function to apply a multiply blend mode to background and foreground image
    :param background_img_raw: Any PIL Image in RGBA format, same size as foreground
    :param foreground_img_raw: Any PIL Image in RGBA format, same size as background
    :return: blended_img_raw PIL image in RGBA format
    '''
    # Import background image
    background_img = numpy.array(background_img_raw)  # Inputs to blend_modes need to be numpy arrays.
    background_img_float = background_img.astype(float)  # Inputs to blend_modes need to be floats.

    # Import foreground image
    foreground_img = numpy.array(foreground_img_raw)  # Inputs to blend_modes need to be numpy arrays.
    foreground_img_float = foreground_img.astype(float)  # Inputs to blend_modes need to be floats.

    # Blend images
    opacity = 0.99  # The opacity of the foreground that is blended onto the background is 70 %.
    blended_img_float = multiply(background_img_float, foreground_img_float, opacity)

    # Convert blended image back into PIL image
    blended_img = numpy.uint8(blended_img_float)  # Image needs to be converted back to uint8 type for PIL handling.
    blended_img_raw = Image.fromarray(blended_img)  # Note that alpha channels are displayed in black by PIL by default.
                                                    # This behavior is difficult to change (although possible).
                                                    # If you have alpha channels in your images, then you should give
                                                    # OpenCV a try.
    return blended_img_raw
    # Display blended image

def Normal(background_img_raw,foreground_img_raw):
    '''
    Function to apply a normal blend mode to background and foreground image
    :param background_img_raw: Any PIL Image in RGBA format, same size as foreground
    :param foreground_img_raw: Any PIL Image in RGBA format, same size as background
    :return: blended_img_raw PIL image in RGBA format
    '''
    # Import background image
    background_img = numpy.array(background_img_raw)  # Inputs to blend_modes need to be numpy arrays.
    background_img_float = background_img.astype(float)  # Inputs to blend_modes need to be floats.

    # Import foreground image
    foreground_img = numpy.array(foreground_img_raw)  # Inputs to blend_modes need to be numpy arrays.
    foreground_img_float = foreground_img.astype(float)  # Inputs to blend_modes need to be floats.

    # Blend images
    opacity = 0.8  # The opacity of the foreground that is blended onto the background is 70 %.
    blended_img_float = normal(background_img_float, foreground_img_float, opacity)

    # Convert blended image back into PIL image
    blended_img = numpy.uint8(blended_img_float)  # Image needs to be converted back to uint8 type for PIL handling.
    blended_img_raw = Image.fromarray(blended_img)  # Note that alpha channels are displayed in black by PIL by default.
                                                    # This behavior is difficult to change (although possible).
                                                    # If you have alpha channels in your images, then you should give
                                                    # OpenCV a try.
    return blended_img_raw
    # Display blended image

def Difference(background_img_raw,foreground_img_raw):
    '''
    Function to apply a normal blend mode to background and foreground image
    :param background_img_raw: Any PIL Image in RGBA format, same size as foreground
    :param foreground_img_raw: Any PIL Image in RGBA format, same size as background
    :return: blended_img_raw PIL image in RGBA format
    '''
    # Import background image
    background_img = numpy.array(background_img_raw)  # Inputs to blend_modes need to be numpy arrays.
    background_img_float = background_img.astype(float)  # Inputs to blend_modes need to be floats.

    # Import foreground image
    foreground_img = numpy.array(foreground_img_raw)  # Inputs to blend_modes need to be numpy arrays.
    foreground_img_float = foreground_img.astype(float)  # Inputs to blend_modes need to be floats.

    # Blend images
    opacity = 0.8  # The opacity of the foreground that is blended onto the background is 70 %.
    blended_img_float = difference(background_img_float, foreground_img_float, opacity)

    # Convert blended image back into PIL image
    blended_img = numpy.uint8(blended_img_float)  # Image needs to be converted back to uint8 type for PIL handling.
    blended_img_raw = Image.fromarray(blended_img)  # Note that alpha channels are displayed in black by PIL by default.
                                                    # This behavior is difficult to change (although possible).
                                                    # If you have alpha channels in your images, then you should give
                                                    # OpenCV a try.
    return blended_img_raw
    # Display blended image
