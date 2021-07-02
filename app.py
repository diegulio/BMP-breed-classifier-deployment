from typing import final
import numpy as np
from flask import Flask, request, jsonify, render_template, url_for, redirect, flash
from werkzeug.utils import secure_filename
import utils
import os
import json

# Carpeta donde se guardaran imagenes y resultados json
UPLOAD_FOLDER = 'static/uploads'
# Extensiones de archivos permitidos
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    '''
    función que verifica archivos válidos
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def final_result(pred):
    '''
    Función que entrega los parámetros con los cuales se renderizará el html
    que muestra los resultados
    '''
    if pred['top1'][0] == 'No detectado':
        disp_0r = 'inline-block'
        disp_1r = 'none'
        disp_3r = 'none'
        top1_breed = None
        top1_proba = None
        top2_breed = None
        top2_proba = None
        top3_breed = None
        top3_proba = None
        return disp_0r, disp_1r, disp_3r, top1_breed, top1_proba, top2_breed, top2_proba, top3_breed, top3_proba
    elif pred['top1'][1] - pred['top2'][1] >= 50:
        disp_0r = 'none'
        disp_1r = 'inline-block'
        disp_3r = 'none'
        top1_breed = pred['top1'][0]
        top1_proba = float(pred['top1'][1])
        top2_breed = None
        top2_proba = None
        top3_breed = None
        top3_proba = None
        return disp_0r, disp_1r, disp_3r, top1_breed, top1_proba, top2_breed, top2_proba, top3_breed, top3_proba
    else:
        disp_0r = 'none'
        disp_1r = 'none'
        disp_3r = 'inline-block'
        top1_breed = pred['top1'][0]
        top1_proba = float(pred['top1'][1])
        top2_breed = pred['top2'][0]
        top2_proba = float(pred['top2'][1])
        top3_breed = pred['top3'][0]
        top3_proba = float(pred['top3'][1])
        
        return disp_0r, disp_1r, disp_3r, top1_breed, top1_proba, top2_breed, top2_proba, top3_breed, top3_proba

def save_json(pred, path, name):
    '''
    Función que guarda un diccionario como json en una carpeta
    '''
    # convierto los valores a float para que json los acepte
    pred['top1'][1] = float(pred['top1'][1] )
    pred['top2'][1] = float(pred['top2'][1] )
    pred['top3'][1] = float(pred['top3'][1] )
    #creo un archivo json y los guardo junto con las imagenes
    with open(path + '/' + name + '.json', 'w') as f:
        json.dump(pred, f)


app = Flask(__name__, template_folder='template')

# Lugar donde se guardaran las imagenes y resultados json
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Pagina inicial
@app.route('/')
def home():    
    if request.method=="GET":
        return render_template("index.html",disp_img = 'none', disp_3r = 'none', disp_0r = 'none', disp_1r = 'none')


# Ruta donde se predice
@app.route('/predict', methods=['POST','GET'])
def predict_breed():     

    if request.method == 'POST':
       
        # check if the post request has the file part
        if 'file' not in request.files:
           
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
        
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            
            # Guardo la imagen
            filename = secure_filename(file.filename)
            path_to_save = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path_to_save)
            # Se hacen las predicciones
            pred = utils.get_prediction(path_to_save)
            #print(pred)
            #json_response = jsonify(top1_breed = pred['top1'][0], top1_proba = int(pred['top1'][1]), top2_breed = pred['top2'][0], top2_proba = int(pred['top2'][1]), top3_breed = pred['top3'][0], top3_proba = int(pred['top3'][1]))
            # Se guarda el resultado en json
            save_json(pred, app.config['UPLOAD_FOLDER'], os.path.splitext(filename)[0])
            # Se decodifican los resultados
            disp_0r, disp_1r, disp_3r, top1_breed, top1_proba, top2_breed, top2_proba, top3_breed, top3_proba = final_result(pred)
            # Se renderiza la pagina inicial con los parametros correspondientes al resultado
            return render_template("index.html", disp_img = 'inline-block', disp_0r = disp_0r, disp_1r = disp_1r, disp_3r = disp_3r, img_path = path_to_save, top1_breed = top1_breed, top1_proba = top1_proba, top2_breed = top2_breed, top2_proba = top2_proba, top3_breed = top3_breed, top3_proba = top3_proba)

    return render_template("index.html",disp_img = 'none',  disp_3r = 'none', disp_0r = 'none', disp_1r = 'none')

    



if __name__ == '__main__':

    #app.secret_key = 'super secret key'
    #app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug = True)





