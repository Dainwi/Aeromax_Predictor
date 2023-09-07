# myapp/views.py
from io import BytesIO
from model.model import AeroMax
import matplotlib.pyplot as plt
from .forms import UploadFileForm
from django.shortcuts import render
import base64

params = [
    'dataset/air-quality-india.csv',
    'saved_model/aeromax_predictor_model.h5'
]

aeromax = AeroMax(params[0],params[1])
aeromax.data_preprocessing()  
aeromax.visualize_for_exsisting(show_graph=False)
aeromax.prepare_training_data()
aeromax.train_or_load_model()
aeromax.prepare_testing_data()
aeromax.make_prediction()

def upload_file(request):
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            train , valid = aeromax.preprare_prediction_data()
            plt.figure(figsize=(25,8))
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
            return render(request, 'app/show_predicted_graph.html', {'image_data': image_base64})
    else:
        form = UploadFileForm()
    return render(request, 'app/index.html', {'form': form})
