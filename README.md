# CreditCard-Fraud-Detector
## Summary:
Credit card fraud happens when someone — a fraudster or a thief — uses your stolen credit card or the information from that card to make unauthorized purchases in your name or take out cash advances using your account.
Our team decided how machine learning will predict the fraud Transactions. We searched the data in Kaggle we got the simulated credit card fraud transactions as csv files. We brainstormed and came up with some solution. Please visit our application to see what we have predicted using supervised learning.

## Overview of development steps:
* Original fraudtrain.csv has 1297868 rows and 23 columns. 
* Used one hot encoding to convert the string to numeric data in the selected columns.
* By using Random Forest Classifier, we selected the feature importance to narrow down our features to the model and split the data.
* Scaled the data, then logistic regression model with the trained data. Once the model is fitted then we predicted outcome using test data.

## Data source:
[Kaggle] https://www.kaggle.com/kartik2112/fraud-detection?select=fraudTrain.csv
         https://www.kaggle.com/kartik2112/fraud-detection?select=fraudTest.csv


## Requirements to run the app on the local machine
* Download the data files from Kaggle and save in the resources folder.
* Provide the Heroku Postgres user credentials in the config.py
* Initialize the database by running the jupyter notebook database_setup.ipynb

## Visualizations:
* The cleaned csv file was uploaded into the Tableau Public.
* The Tableau visualizations were made based on the factors affecting the amount, category, transactions, age and locations.
* Used matplotlib to create confusion matrix and correlation diagrams.

## Machine learning models used:
* Random Forest Classifier
* XGBoost Classifier
* Logistic Regression
* Gradient Boosting Regressor
* Gaussian Naive Bayes
* K-Nearest Neighbors(KNN)
* Support Vector Machine(SVM)

## Tools used in this project:
* Python: Pandas, Flask, SKlearn
* Webpage Design: HTML, CSS , Bootstrap
* Tableau
* PostgreSQL 

## Local
* Make sure all the requirements from requirements.txt are up to date
* Run app.py
* Access at local host: http://127.0.0.1:5000/

### Remote Access
* [Heroku] https://credit-card-detect.herokuapp.com/



        


