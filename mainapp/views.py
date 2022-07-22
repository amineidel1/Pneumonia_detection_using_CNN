import os
from django.shortcuts import render
from .forms import ImageForm
from keras.models import load_model
import matplotlib.pyplot as plt
from keras.preprocessing import image
# import pickle
# import joblib
import keras
import numpy as np
import os
from pathlib import Path


# Create your views here.
def home(request):
    return render(request,'index1.html')

def inputt(request):
    return render(request,'Frontend/InputImg.html')


def load_image(img_path, show=False):

    img = image.load_img(img_path, target_size=(224, 224))
    # print(type(img))
    img_tensor = image.img_to_array(img)                    # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.                                      # imshow expects values in the range [0, 1]

    if show:
        plt.imshow(img_tensor[0])                           
        plt.axis('off')
        plt.show()

    return img_tensor

def getOutput(image):
    # print(image)
    path = sorted(Path("V:/BEProject/detectPneumonia/media/images").iterdir(), key=os.path.getmtime , reverse=True)
    paths = sorted(os.listdir("V:/BEProject/detectPneumonia/media/images"))
    # print(path)
    tempp = str(path[0])[42:]
    print(tempp)
    # WindowsPath('V:/BEProject/detectPneumonia/media/images/person101_bacteria_486.jpeg')
    finalPath = "V:/BEProject/detectPneumonia/media/images/" + tempp
    print(finalPath)
    # print(path)
    model = load_model("model.h5")
    print("Came here")
    finalImage = load_image(finalPath)
    prediction = model.predict(finalImage)
    print(type(finalImage))


    print(prediction[0][1])   #prediction is two dimensional array where index 1 is accuracy. index 0 has image loss.
    if round(prediction[0][1],1) == 0:
        return "NORMAL"
    else:
        return "PNEUMONIA"
        # i = i + 1

    return prediction   

def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            output = getOutput(img_obj)
            print(output)
            return render(request, 'tempIndex.html', {'form': form, 'img_obj': img_obj, 'output':output})
    else:
        form = ImageForm()
    return render(request, 'tempIndex.html', {'form': form})

