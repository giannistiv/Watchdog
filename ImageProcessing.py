import os
import io
import Image
from array import array

image = Image.open(io.BytesIO(bytes))
image.save(savepath)