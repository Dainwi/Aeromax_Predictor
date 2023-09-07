import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential , load_model
from keras.layers import Dense, LSTM

class ECHO_ECHO:
    
    def __init__(self,dataset_path,model_path):
        self.dataset_path = dataset_path
        self.model_path = model_path
        self.dataframe = pd.read_csv(self.dataset_path)
        self.sc = MinMaxScaler(feature_range=(0,1))
        
        
    def data_preprocessing(self):
        self.dataframe["Timestamp"] = pd.to_datetime(self.dataframe["Timestamp"])
        self.dataframe['Date'] = self.dataframe["Timestamp"].dt.date
        self.dataframe_date = pd.DataFrame(self.dataframe.groupby('Date')['PM2.5'].mean())
        self.dataframe_year = self.dataframe.loc[:,['Year','PM2.5']]
        self.datafrane_day = self.dataframe.loc[:,['Day','PM2.5']]
        self.dataframe_hour = self.dataframe.loc[:,['Hour','PM2.5']]
        
    def visualize_for_exsisting(self,show_graph=False):
        self.new_dataframe_date = pd.DataFrame(self.dataframe.groupby('Date')['PM2.5'].mean())
        if show_graph==True:
            self.new_dataframe_date.plot(figsize=(25,4))
            
    def prepare_training_data(self):
        self.dataset = self.dataframe_date.values
        self.training_data_len = math.ceil(len(self.dataset)*0.8)
        self.scaled_data = self.sc.fit_transform(self.dataset)
        self.training_data = self.scaled_data[0:self.training_data_len,:]
        self.X_train = []
        self.y_train = []
        for i in range(60,len(self.training_data)):
            self.X_train.append(self.training_data[i-60:i,0])
            self.y_train.append(self.training_data[i,0])
        self.X_train, self.y_train = np.array(self.X_train), np.array(self.y_train)
        self.X_train = np.reshape(self.X_train,(self.X_train.shape[0],self.X_train.shape[1],1))
        
            
    def build_model(self):
        self.model = Sequential()
        self.model.add(LSTM(units=50, return_sequences=True, input_shape=(self.X_train.shape[1],1)))
        self.model.add(LSTM(units=50, return_sequences=False))
        self.model.add(Dense(units=25))
        self.model.add(Dense(units=1))
        
    def train_model(self):
        self.model.compile(optimizer='adam',loss='mean_squared_error')
        self.model.fit(self.X_train,self.y_train,batch_size=1,epochs=1)
        self.model.save(self.model_path)
    
    def train_or_load_model(self):
        try:
            self.model = load_model(self.model_path)
        except:
            self.build_model()
            self.train_model()
            
    def prepare_testing_data(self):
        self.testing_data = self.scaled_data[self.training_data_len-60:,:]
        self.X_test = []
        self.y_test = self.dataset[self.training_data_len:,:]
        for i in range(60,len(self.testing_data)):
            self.X_test.append(self.testing_data[i-60:i,0])
        self.X_test = np.array(self.X_test)
        self.X_test = np.reshape(self.X_test,(self.X_test.shape[0],self.X_test.shape[1],1))
        
    def make_prediction(self):
        self.predictions = self.model.predict(self.X_test)
        self.predictions = self.sc.inverse_transform(self.predictions)
        
    
    def visualize_prediction(self,save_graph=False):
        self.train = self.new_dataframe_date[:self.training_data_len]
        self.valid = self.new_dataframe_date[self.training_data_len:]
        self.valid['Predictions'] = self.predictions
        plt.figure(figsize=(10,4))
        plt.title('Model')
        plt.xlabel('Date',fontsize=8)
        plt.ylabel('PM2.5',fontsize=8)
        plt.plot(self.train['PM2.5'])
        plt.plot(self.valid[['PM2.5','Predictions']])
        plt.legend(['Train','Val','Predictions'])
        plt.show()
        if save_graph==True:
            plt.savefig('./graph/prediction.png')