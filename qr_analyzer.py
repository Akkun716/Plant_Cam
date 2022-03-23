
from pyzbar.pyzbar import decode
from PIL import Image
from PIL import UnidentifiedImageError

class DataPair:

    ### 
    # A class representing a data pair of an image and, should there be a QR code in it,
    # the data within it. This way the program that this will pass both things to 

    def __init__(self, image, id):
        ### Parameters:
        # 
        #   image - str
        #   The recallable image handle for the processed image.
        #
        #   id - int
        #   The plot number that, in optimal circumstances, would be retrieved
        #   from a QR code in that image.
        self.image = image 
        self.id = id

def qr_decode(imgname):
     ### Analyzes an image using PZYBAR and PILLOW to determine that a QR code is 
    # here, and if there is, adds the image and the data within to a 

    # Parameters: 
    #
    # imgname - str
    # The filename for the image to be checked.

    try: 
         # Checks that the image is ACTUALLY an image
        img = Image.open(imgname)
        result = decode(img)[0].data.decode('ascii')
        block = DataPair(img, result)
        return block
        # If result has a length of 0, it means no result came about from the image.
    except(IndexError, FileNotFoundError, UnidentifiedImageError):
        return None
        # Because there was no data, it shouldn't be passed into the database.

#Test Code
#imagetest = "IMG_0198.JPG"

#try:
#   print(qr_decode(imagetest).id)
#except(AttributeError):
#    print("\nQR Code could not be retrieved from filename '",imagetest,"'.")