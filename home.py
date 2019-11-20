import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
file = open('model.pkl', 'rb')
model = pickle.load(file)


@app.route('/', methods=['get', 'post'])
def index():
    return render_template('index.html')


@app.route('/index', methods=['get', 'post'])
def home():
    return render_template('index.html')


@app.route('/sal', methods=['get', 'post'])
def salary():
    return render_template('home.html')


@app.route('/result', methods=['get', 'post'])
def result():
    if request.method == 'POST':
        '''CRIM = float(request.form.get('r1'))
        ZN = float(request.form.get('r2'))
        INDUS = float(request.form.get('r3'))
        CHAS = float(request.form.get('r4'))
        NOX = float(request.form.get('r5'))
        RM = float(request.form.get('r6'))
        AGE = float(request.form.get('r7'))
        DIS = float(request.form.get('r8'))
        RAD = float(request.form.get('r9'))
        TAX = float(request.form.get('r10'))
        PTRATIO = float(request.form.get('r11'))
        BR = float(request.form.get('r12'))
        LSTAT = float(request.form.get('r13'))
        #MEDV = request.form.get('r14')
        features = np.array([[CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRATIO, BR, LSTAT]])'''
        input_features = [float(x) for x in request.form.values()]
        features = [np.array(input_features)]
        result = model.predict(features)
        output = round(result[0], 2)
    return render_template('home.html', param='Predicted Salary is Rs. {}'.format(output))


@app.route('/bolly', methods=['get', 'post'])
def bollywood():
    mess = "Enter a movie name."
    return render_template('bolly_movie.html', message=mess)


@app.route('/movie_result', methods=['get', 'post'])
def movies():
    data = pd.read_csv('bolly_movie.csv')
    data['title'] = data['title'].str.lower()
    movie_name = request.form.get('mov_name')
    movie_name.lower()
    mess = "'"+movie_name+"'"+' '+'is a great choice, below are 10 movies that you might like to watch.'
    file1 = open('sim.pkl', 'rb')
    model1 = pickle.load(file1)
    if movie_name in data['title'].unique():
        i = data.loc[data['title'] == movie_name].index[0]
        list_bolly = []
        movie_list = list(enumerate(model1[i]))
        print(movie_list)
        movie_list = sorted(movie_list, key=lambda x: x[1], reverse=True)
        print(movie_list)
        movie_list = movie_list[1:11]
        print(movie_list)
        for j in range(len(movie_list)):
            a = movie_list[j][0]
            list_bolly.append(data['title'][a] + ' (' + data['actors'][a] + ')')
        for k in range(len(list_bolly)):
            print(list_bolly[k])
        return render_template('bolly_movie.html', movies_list=list_bolly, message=mess)
    else:
        mess="sorry we dont have the movie that you selected in our database, kindly try another movie."
        return render_template('bolly_movie.html', movie_list="", message=mess)


if __name__ == '__main__':
    app.run(debug=True)
