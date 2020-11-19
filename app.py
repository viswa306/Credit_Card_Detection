#!/usr/bin/env python
# coding: utf-8
# ### Load test data into postgres for processing

# Import dependencied
from flask import Flask, render_template
from config import username, password, host, dbname
import pandas as pd
import requests
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

# connection_string = f'{username}:{passowrd}@localhost:5432/Creditcard_db'   
connection_string = f'{username}:{password}@{host}:5432/{dbname}'
engine = create_engine(f'postgresql://{connection_string}')



Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Assign the test data class to a variable called test_data
test_data = Base.classes.creditcard_test1
session = Session(engine)

# Create an instance of Flask
app = Flask(__name__)

# Basic Flask HTML Routes
@app.route("/gender")
def home():
    return render_template("gender.html")

def query_to_dictlist(keylist, obj):
    from datetime import date, datetime
    today = datetime.today()
    result_list = []
    for row in obj:
        mydict = {}
        for i in range(0,len(keylist)):
            if (keylist[i] == 'age'):
                birthdate = pd.to_datetime(row[i])
                age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day)) 
                mydict[keylist[i]] = age
            else:
                mydict[keylist[i]] = row[i]
        result_list.append(mydict)
    return result_list

# api route to extract the user's response in the form, pre-process it, plug it into the model, and spit out a prediction
@app.route('/makepredicitons')
def makepredicitons():
    session = Session(engine)
    data_test = session.query(test_data.cc_num, test_data.category, 
                test_data.amt, test_data.lat, test_data.long, 
                test_data.job, test_data.merch_lat, test_data.merch_long, 
                test_data.dob, test_data.trans_num, test_data.unix_time, test_data.is_fraud).all()
   
    columnlist = ['cc_num','category','amt','lat','long','job','merch_lat','merch_long','age','trans_num','unix_time','is_fraud']
    resultset = query_to_dictlist(columnlist, data_test)

    data_train = pd.DataFrame(resultset)
    print(data_train)


    # Encode the transaction number and convert into numeric
    from sklearn.preprocessing import LabelEncoder
    get_transnum = data_train['trans_num']
    label_encoder_t = LabelEncoder()
    label_encoder_t.fit(get_transnum)
    encoded_transnum = label_encoder_t.transform(get_transnum)
    data_train['trans_num'] = encoded_transnum

    # Encode the category and convert into numeric
    get_category = data_train['category']
    label_encoder_c = LabelEncoder()
    label_encoder_c.fit(get_category)
    encoded_category = label_encoder_c.transform(get_category)
    data_train['category'] = encoded_category

    # Encode the job and convert into numeric
    get_job = data_train['job']
    label_encoder_j = LabelEncoder()
    label_encoder_j.fit(get_job)
    encoded_job = label_encoder_j.transform(get_job)
    data_train['job'] = encoded_job


    ## Select all the records from the table
    # sql_stmt = "select * from creditcard_test"
    # result_set = engine.execute(sql_stmt)
    # results = []
    # for r in result_set:  
    #     results.append(r)
    #     print(r)    
    # result_set_df = pd.DataFrame(results, columns=["category", "cc_num", "amt", "lat","long", "job", "age", "trans_num", 
    #                          "unix_time", "merch_lat","merch_long", "is_fraud"])
    # result_set_df

    label_encoder_c.classes_

    # sets y to is_fraud
    target = data_train["is_fraud"].values.reshape(-1, 1)
    # Define the features
    selected_features = data_train.drop('is_fraud', axis=1)

    # Scale the train & test datasets
    from sklearn.preprocessing import StandardScaler
    # Create a standard scaler model and fit it to the training data
    X_scaler = StandardScaler().fit(selected_features)
    # Transform the scaled data
    X_test_scaled = X_scaler.transform(selected_features)

    import joblib
    filename = "logistic_balanced_model.sav"
    # load the model from disk
    loaded_model = joblib.load(filename)
    predictions = loaded_model.predict(X_test_scaled)

    # ## Display the output into a dataframe
    y_predictions = loaded_model.predict(X_test_scaled)

    actual_value = []
    predicted_value = []

    for i in range(len(target)):
        target_item = target[i][0]
        actual_value.append(target_item)
        
    for i in range(0, len(y_predictions)):
        pred_item = y_predictions[i]
        predicted_value.append(pred_item)


    label_encoder_c.inverse_transform(encoded_category)
    output_csv = pd.DataFrame()
    output_csv["category"] = label_encoder_c.inverse_transform(encoded_category)
    output_csv["cc_num"] = selected_features['cc_num']
    output_csv["trans_num"] = label_encoder_t.inverse_transform(encoded_transnum)
    output_csv["amount"] = selected_features['amt']
    # output_csv["unixtime"] = selected_features['unix_time']
    output_csv["actual_value"] = actual_value
    output_csv["predicted_value"] = predicted_value
    output_sliced = output_csv[4970:5000]
    # output_sliced = output_csv[-30:]
    output_dict = output_sliced.to_dict("records")
    # output_dict = output_csv.to_dict("records")
    return output_dict


#-------------------------------------------------------------------------------------
## Define the routes to render basic html pages
#-------------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')


# Render the analysis page
@app.route('/analysis')
def analysis():
    return render_template('tableauviz.html')

# Render the prediction html page
@app.route('/prediction')
def prediction():
    return render_template('prediction.html', output_html = makepredicitons())

# Render the about html page
@app.route('/about')
def about():
    return render_template('about.html')

#-------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)