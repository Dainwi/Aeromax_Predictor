# Aeromax Predictor 🍃📈
> **Project Idea for Geeks-for-Geeks EcoTech Hack-A-Thon🚀**


## Table of Contents

- [Introduction](###Introduction)
- [Repository Structure](###Repository-Structure)
- [Requirements](###Requirements)
- [Installation](###Installation)
- [Usage](###Usage)
- [Benifits](###Benifits)
- [Future Scope](###Future-Scope)
- [Contributors](###Contributors)


### Introduction
A LSTM model which is integrated to a web-app built on django rest framework. The model is trained on [India's air quality dataset]() which can predict air quality index graph of the next year. The model is trained on the dataset from 2015 to 2021 and the model is tested on the dataset of 2022. And this LSTM model integrated to a web app so it can be used more easily. All you have to do is to upload the csv file and the predicted graph will be shown in result page.

#### Glimpse of the project

Here are some screenshots of the project. The first one is the homepage of the web app in which you can upload your csv file and the second one is the result page in which you can see the predicted graph of the next year.

| **`Home page`** | **`result page`** |
|:---:|:---:|
|![home page](./screenshots/aeromax_predictor_ss1.png)|![result page](./screenshots/aeromax_predictor_ss2.png)|

### Repository Structure
This is how the repository is structured. The repository contains the dataset, model, webapp, notebook, saved_model, media, docs and the manage.py file.


```bash
├───aeromax_predictor
│   ├───app
│   │   ├───migrations
│   │   ├───templates
│   │   │   └───app
│   │   │          index.html
│   │   │          result.html
│   │   |───static
│   │   │   └───styles.css
│   ├───dataset
│   │   └───dataset.csv
│   ├───docs
│   │   └───screenshots
│   │   |      └─── aeromax_predictor_ss1.png
│   │   |      └─── aeromax_predictor_ss2.png
|   |   └─── videos
|   |   └─── presentation
|   |   └─── index.html
|   |   └─── README.md
│   ├───media
│   │   └───uploads
│   │       └───dataset.csv
│   ├───model
│   │   └───model.py
│   ├───notebook
│   │   └───model.ipynb
│   ├───saved_model
│   │   └───model.h5
│   ├───webapp
│   │   └───settings.py
│   │   └───urls.py
│   │   └───wsgi.py
│   ├───.gitignore
│   ├───manage.py
```