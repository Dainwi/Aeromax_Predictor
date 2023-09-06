import datetime
import math
import os
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras.layers import LSTM, Dense
from keras.models import Sequential, load_model
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm

warnings.filterwarnings("ignore")

class ECHO_ECHO:
    
    def __init__(self,dataset,saved_model_path):
        self.dataset = dataset
        self.dataframe = pd.read_csv(dataset)
        self.dataframe_info = self.dataframe.info()
        self.dataframe['Timestamp'] = pd.to_datetime(self.dataframe['Timestamp'])
        self.dataframe_head = self.dataframe.head()
        self.dataframe['Date'] = self.dataframe['Timestamp'].dt.date
        self.scaler = MinMaxScaler(feature_range=(0,1))
        self.saved_model_path = saved_model_path
        
    def visualize(self,show_plot=False):
        self.dataframe.plot(x='Timestamp',y='PM2.5',figsize=(10,4))
        plt.xticks(rotation=45)
        if show_plot==True:
            plt.show()
        
    def process_data(self,num=60):
        self.dataframe_date = pd.DataFrame(self.dataframe.groupby('Date')['PM2.5'].mean())
        self.datasets = self.dataframe_date.values
        self.training_data_len = math.ceil(len(self.datasets)*0.8)
        self.scaled_data = self.scaler.fit_transform(self.datasets)
        
        train_data = self.scaled_data[0:self.training_data_len,:]
        self.x_train = []
        self.y_train = []
        for i in range(num,len(train_data)):
            self.x_train.append(train_data[i-num:i , 0])
            self.y_train.append(train_data[i,0])
        self.x_train, self.y_train = np.array(self.x_train), np.array(self.y_train)
        self.x_train = np.reshape(self.x_train, (self.x_train.shape[0],self.x_train.shape[1],1))
        
        # return self.x_train,self.y_train
    
    def build_model(self):
        self.model = Sequential()
        self.model.add(LSTM(50, return_sequences=True, input_shape=(self.x_train.shape[1],1)))
        self.model.add(LSTM(50,return_sequences=False))
        self.model.add(Dense(25))
        self.model.add(Dense(5))
    
    
    def train_or_load_model(self):
        if os.path.isfile(self.saved_model_path):
            self.model = load_model(self.saved_model_path)
        else:
            self.model.compile(optimizer='adam',loss='mean_squared_error')
            self.model.fit(self.x_train,self.y_train,epochs=25,batch_size=8)
            self.model.save(self.saved_model_path)
        
    def make_prediction(self,num=60):
        test_data = self.scaled_data[self.training_data_len-60:,:]
        self.x_test = []
        self.y_test = self.datasets[self.training_data_len:,:]
        for i in range(num,len(test_data)):
            self.x_test.append(test_data[i-num:i,0])
        self.x_test = np.array(self.x_test)
        self.x_test = np.reshape(self.x_test, (self.x_test.shape[0], self.x_test.shape[1], 1))
        predictions = self.model.predict(self.x_test)
        predictions = self.scaler.inverse_transform(predictions)  
        
        return predictions
    
    def show_predicted_graph(self,prediction):
        rmse = np.sqrt(np.mean(prediction-self.y_test)**2)
        train = self.dataframe[:self.training_data_len]
        validate = self.dataframe[self.training_data_len:]
        validate['Predictions'] = prediction
        
        plt.title("Model for PM2.5")
        plt.xlabel("Date", fontsize = 15)
        plt.ylabel("PM2.5",fontsize=15)
        plt.plot(train[self.dataframe_date.columns])
        plt.plot(validate['PM2.5'])
        plt.plot(validate["Predictions"])
        plt.legend(["Train","Val","Predictions"])
            
        
        
if __name__=='__main__':
    
    dataset = 'model/dataset/air-quality-india.csv'
    saved_model = 'ECHO_ECHO.h5'
    
    echo_echo = ECHO_ECHO(dataset,saved_model)
    echo_echo.visualize(show_plot=False)
    echo_echo.process_data()
    echo_echo.build_model()
    echo_echo.train_or_load_model()
    prediction = echo_echo.make_prediction(num=60)
    echo_echo.show_predicted_graph(prediction=prediction)