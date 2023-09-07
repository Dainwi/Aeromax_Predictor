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
            model.visualize_for_exsisting(show_graph=False)
            model.prepare_training_data()
            model.train_or_load_model()
            model.prepare_testing_data()
            model.make_prediction()
            train , valid = model.preprare_prediction_data()
            
            plt.figure(figsize=(16,8))
            plt.title('Model')
            plt.xlabel('Date', fontsize=8)
            plt.ylabel('PM2.5', fontsize=8)
            plt.plot(train['PM2.5'])
            plt.plot(valid[['PM2.5','Predictions']])
            plt.legend(['Train','Val','Predictions'])

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
