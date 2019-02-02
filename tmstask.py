from io import BytesIO
import numpy as np
import pandas as pd
import psycopg2
from flask import Flask, render_template,request,send_file, make_response,json
from flask_bootstrap import Bootstrap
from pandas.io.json import json_normalize
from flask_cors import  CORS,cross_origin
app = Flask(__name__)
CORS(app, support_credentials=True)
Bootstrap(app)
import xgboost as xgb
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LogisticRegression
con = psycopg2.connect("dbname=daabi6mhbsu5fm user=ewyivrzjhyxxyy password=dc37c6729bd76a50666bfc9ffad4fa11b6e3a1974834b3b5ab6933f23a25254d host=ec2-54-83-17-151.compute-1.amazonaws.com")
@app.route('/app1',methods=['GET', 'POST'])
@cross_origin(supports_credentials=True)
def index():
  if request.method=='GET':
    try:
      if (isinstance(int(request.args.get('cid')),int) and isinstance(int(request.args.get('tid')),int) and isinstance(int(request.args.get('eid')),int)) == True:
        num1 = request.args.get('cid')
        num2 = request.args.get('tid')
        num3 = request.args.get('eid')
        sq = """SELECT *FROM public.tms3"""
        trn = pd.io.sql.read_sql(sq,con)
        #trn=pd.read_csv("tmsbhav.csv")
        cid=trn['cid']
        tid=trn['tid']
        eid=trn['eid']
        rc=trn['roc']
        class_names = ['tid', 'cid', 'eid']
        print(class_names)
        X=np.array([cid,tid,eid]).T
        #X=X[:,1:3]
        #print(X)
        Y=np.array(rc)
        #print(Y)
        reg=LogisticRegression()
        reg.fit(X,Y)
        z = np.array([num1,num2,num3]).reshape(1, -1)
        # Predict the response for test dataset
        y_pred = reg.predict(z)
        y_pred=int(y_pred)
        pythonDictionary = {'a':num1, 'b':num2, 'c':num3,'e':y_pred}
        return  json.dumps(pythonDictionary)
    except ValueError:
      return 'enter valid parameters'
