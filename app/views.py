# myapp/views.py
from django.shortcuts import render
from .forms import UploadFileForm
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from model.model import ECHO_ECHO  # Import your model class

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            data = pd.read_csv(uploaded_file.csv_file)


            model = ECHO_ECHO('dataset/air-quality-india.csv', 'saved_model/echo_echo.h5')
            model.data_preprocessing()  
            model.prepare_testing_data()
            model.make_prediction()
            
            plt.plot(data['x'], model.predictions)
            plt.xlabel('X-axis')
            plt.ylabel('Predicted Y-axis')
            plt.title('Predicted Graph')

            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            image_data = buffer.getvalue()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            return render(request, 'app/index.html', {'image_data': image_base64})
    else:
        form = UploadFileForm()
    return render(request, 'app/upload.html', {'form': form})
