from flask import Flask, render_template, redirect
from flask_restful import Resource, Api
from flask import request
import json
import os.path
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib as jb
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack, vstack

app = Flask(__name__)
api = Api(app)
json_db = 'db.json'

rf = jb.load("random_forest_m8.pkl.z")
dt = jb.load("decision_tree_m8.pkl.z")
nome_vec_validate = jb.load("nome_vectorizer_m8.pkl.z")

def get_records():
    try:    
        data = 1
        if os.path.exists(json_db):
            table = ''
            with open(json_db) as f:
                data = json.load(f)
                for d in data:
                    table += '<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(d['marca'], d['modelo'], d['cor'], d['cambio'], d['ano'], d['km'], d['portas'], d['precorf'])
                return table
        else:
            return "nao existe"
    except:
        return "erro 2"

def label_encode(data):
    label_encoder = LabelEncoder()
    cars_features_lbl_encd = ['km', 'cambio', 'portas', 'cor', 'ano']
    data = data[cars_features_lbl_encd]
    object_cols = ['cambio', 'cor', 'ano']
    for col in object_cols:
        data[col] = label_encoder.fit_transform(data[col])
    return data

def predict(data):
    vectorize_nome = nome_vec_validate.transform(data['nome'])
    data_label_encode = label_encode(data)
    data_hstack = hstack([data_label_encode, vectorize_nome])
    return rf.predict(data_hstack)[0], dt.predict(data_hstack)[0]


@app.route("/")
def index():
    dados = get_records()
    return """<head><h1>Previsão de Preços de Carros</h1></head>
            <body>
              <form action="/predict" method="post" style="padding-left: 15px; border: solid 1px #b9b9b9; margin-top: 0px; padding-top: 4px; padding-bottom: 15px;">
                  <h3>Formulario de teste:</h3>          
                  <table>
                <tr>
                  <td><label for="marca">Marca:</label></td>
                  <td><input type="text" id="marca" name="marca"></td>
                </tr>
                <tr>
                  <td><label for="modelo">Modelo:</label></td>
                  <td><input type="text" id="modelo" name="modelo"></td>
                </tr>
                <tr>
                  <td><label for="cor">Cor:</label></td>
                  <td><input type="text" id="cor" name="cor"></td>
                </tr>
                <tr>
                  <td><label for="cambio">Câmbio:</label></td>
                  <td><input type="text" id="cambio" name="cambio"></td>
                </tr>
                <tr>
                  <td><label for="ano">Ano:</label></td>
                  <td><input type="text" id="ano" name="ano"></td>
                </tr>
                <tr>
                  <td><label for="km">KM:</label></td>
                  <td><input type="text" id="km" name="km"></td>
                </tr>
                <tr>
                  <td><label for="portas">Portas:</label></td>
                  <td><input type="text" id="portas" name="portas"></td>
                </tr>
                <tr>
                  <td></td>
                  <td><input type="submit" value="Validar" style="width: 100px; margin-top: 10px;"></td>
                </tr>
            </table>
              </form>

              <div style="padding-top: 2px; padding-bottom: 1px;"><a href="https://github.com/AlexandreNeuk/curso-machine-learning" target="_blank"><h4>Link do projeto no github</h4></a></div>
              <div style="padding-top: 5px; padding-bottom: 1px;"><h3 style="margin-bottom: 5px;">Últimas Previsões:</h3></div>
              <table><tr><th style="width: 150; text-align: inherit;">Marca</th>
                       <th style="width: 150; text-align: inherit;">Modelo</th>
                       <th style="width: 80; text-align: inherit;">Cor</th>
                       <th style="width: 80; text-align: inherit;">Câmbio</th>
                       <th style="width: 60; text-align: inherit;">Ano</th>
                       <th style="width: 60; text-align: inherit;">KM</th>
                       <th style="width: 60; text-align: inherit;">Portas</th>
                       <th style="width: 60; text-align: inherit;">Preço Previsto</th></tr>
              {}
              </table>
            </body>""".format(dados)

@app.route('/predict', methods=['GET', 'POST'])
def handle_data():
    modelo = "{} {} {}".format(request.form['marca'], request.form['modelo'], request.form['ano'])
    km = int(request.form['km'])
    ano = int(request.form['ano'])
    portas = int(request.form['portas'])
    data = pd.DataFrame([[km, request.form['cambio'], ano, portas, request.form['cor'], modelo]], columns=['km','cambio', 'ano', 'portas', 'cor', 'nome'])
    preco_rf, preco_dt = predict(data)
    json_test = {
      "marca" : request.form['marca'],
      "modelo" : request.form['modelo'],
      "ano" : request.form['ano'],
      "km" : request.form['km'],
      "cambio" : request.form['cambio'],
      "cor" : request.form['cor'],
      "portas" : request.form['portas'],
      "precorf": preco_rf
    }
    json_tmp_data = []
    with open('db.json') as jsonfile:
        json_data = json.load(jsonfile)
        for d in json_data:
            json_tmp_data.append(d)

    json_tmp_data.append(json_test)

    with open('db.json', 'w+') as jsonfile:
        json.dump(json_tmp_data, jsonfile)
  
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')