from flask import Flask,render_template,request
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn .model_selection import cross_val_score
from sklearn.metrics import accuracy_score,precision_score,recall_score,classification_report
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb
import pickle
app = Flask(__name__)
app.config['upload folder']= r'C:\Users\YMTS0356\PycharmProjects\floods\upload'
@app.route('/')
def home():
    return render_template('index.html')

def cleaning(file):
    data = file[['Mar-May','Jun-Sep','10days_june','increased Rainfall','flood']]
    return data
def spliting(file):
    global X,y
    X = file.drop(['flood'],axis = 1)
    y = file.flood
    x_train,x_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state = 9)
    return x_train,x_test,y_train,y_test

@app.route('/upload',methods = ['POST',"GET"])
def upload():
    if request.method =="POST":
        file = request.files['file']
        global df
        print(file)
        filetype =os.path.splitext(file.filename)[1]
        print(filetype)
        if filetype == '.csv':
            path = os.path.join(app.config['upload folder'],file.filename)
            file.save(path)
            df = pd.read_csv(path)
            df.drop(['Unnamed: 0'],axis = 1,inplace = True)
            return render_template('view.html',col_name = df.columns,row_val = list(df.values.tolist()))
        else:
            return render_template('upload.html')
    return render_template('upload.html')
@app.route('/model',methods= ['POST',"GET"])
def model():
    if request.method == 'POST':
        clean_data = cleaning(df)
        x_train,x_test,y_train,y_test = spliting(clean_data)
        model = int(request.form['model'])
        if model == 1:
            knn = KNeighborsClassifier()
            score =cross_val_score(knn,X,y,cv = 5)
            print(score)
            print(score.mean())
            kn = knn.fit(x_train,y_train)
            pre = kn.predict(x_test)
            file = 'models/knn.h5'
            pickle.dump(kn,open(file,'wb'))
            scores = accuracy_score(y_test,pre)
            print(scores)
            return render_template('model.html',msg = 'success',score = scores,Selected = 'KNN')
        if model == 2:
            dt = DecisionTreeClassifier()
            score =cross_val_score(dt,X,y,cv = 5)
            print(score)
            print(score.mean())
            d =dt.fit(x_train,y_train)
            file = 'models/dt.h5'
            pickle.dump(d, open(file, 'wb'))
            pre = d.predict(x_test)
            scores = accuracy_score(y_test,pre)
            print(scores)
            return render_template('model.html',msg = 'success',score = scores,Selected = 'Decision Tree Classifier')
        if model == 3:
            lr = LogisticRegression()
            score =cross_val_score(lr,X,y,cv = 5)
            print(score)
            print(score.mean())
            l = lr.fit(x_train,y_train)
            pre = l.predict(x_test)
            file = 'models/lr.h5'
            pickle.dump(l, open(file, 'wb'))
            scores = accuracy_score(y_test,pre)
            print(scores)
            return render_template('model.html',msg = 'success',score = scores,Selected = 'Logistic Regression')
        if model == 4:
            xg = xgb.XGBClassifier()
            score =cross_val_score(xg,X,y,cv = 5)
            print(score)
            print(score.mean())
            x = xg.fit(x_train,y_train)
            pre = x.predict(x_test)
            file = 'models/xgb.h5'
            pickle.dump(x, open(file, 'wb'))
            scores = accuracy_score(y_test,pre)
            print(scores)
            return render_template('model.html',msg = 'success',score = scores,Selected = 'XGBoost')

    return render_template('model.html')


@app.route('/prediction',methods = ["POST","GET"])

def prediction():
    if request.method == "POST":
        a = float(request.form['f1'])
        b = float(request.form['f2'])
        c = float(request.form['f3'])
        d = float(request.form['f4'])
        values = [[float(a),float(b),float(c),float(d)]]
        filenam = r'models/xgb.h5'
        model = pickle.load(open(filenam,'rb'))
        ex = pd.DataFrame(values,columns=X.columns)
        pred = model.predict(ex)
        print(pred)
        return render_template('prediction.html',res = pred)
    return render_template('prediction.html')

if __name__ == '__main__':
    app.run(debug=True)