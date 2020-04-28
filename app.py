from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
import json
import pandas as pd
import csv

app = Flask(__name__)

#conexión mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'almacen'
mysql = MySQL(app)


#llave secreta
app.secret_key = 'mysecretkey'

#funciones
@app.route('/', methods=['GET', 'POST'])
def index():
    #Inicializar cursor
    global data
    cur = mysql.connection.cursor()
    #inicio de query
    cur.execute('SELECT * FROM orden_compra')
    #guardar la data en una variable global
    data = cur.fetchall()
    return render_template('index.html')

@app.route('/altaAlmacen')
#redirecciona al formulario de almacen
def altaAlmacen():
    return render_template('altaAlmacen.html')    

@app.route('/altaCompras')
#redirecciona al formulario OC
def altaCompras():
    return render_template('altaCompras.html')    

@app.route('/altaProducto')
#redirecciona al formulario de alta producto
def altaProducto():
    return render_template('altaProducto.html')    

@app.route('/add_almacen', methods = ['GET', 'POST'])
#función que valida la información introducida para el alta de almacen
def almacen():   
    if request.method == 'POST':
        nombre_almacen = request.form['nombre_almacen']
        sub_inventario = request.form['sub_inventario']
        cur = mysql.connection.cursor()
        if len(nombre_almacen) > 0 and len(sub_inventario) > 0:
            for x in data:
                almacenDB = x[5]
                iventarioDB = x[4]
                if nombre_almacen != x[5] and sub_inventario != x[4]:
                    cur.execute('INSERT INTO orden_compra (nombre_almacen, sub_inventario) VALUES(%s, %s)',
                    (nombre_almacen, sub_inventario)) 
                    mysql.connection.commit()
                    flash('Almacen agregado correctamente')
                    return redirect(url_for('altaCompras'))
                else:
                    flash('El almacen ya existe en sistema')
        else:
            flash('Debes introducir datos de almacen')
            return redirect(url_for('altaAlmacen'))
        

@app.route('/data', methods=['GET','POST'])
#función para subir el xls y validaciones pertinentes
def data():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM productos')
        productData = cur.fetchall()
        print('productData', productData)
    
        dataLength = []
        newData = []
        lengthData = 141
        skuData = 2
        f = request.form['csvfile']
        data = pd.read_excel(f)
        #información que carga del xlsx
        finalData = data.to_dict()
        dataToOC = data.to_html()
        for k in dataToOC:
            # newData.appen(k)
            print(k)

        #se recorre para conocer la longitud
        for x in finalData:
           dataLength.append(x)
        #validación de longitud
        if len(dataLength) != lengthData:
            flash('Error!, la longitud es incorrecta')
            print('no son iguales')
        else:
            print('entra al else')
            # for p in range(skuData, len(dataLength) - skuData):
            #     for skuDB in productData:
            #         print('skuDB[2]',skuDB[2])
            #         if dataLength[p] != skuDB[2]:    
            #     cur.execute('INSERT INTO productos1 (sku, cantidad) VALUES(%s, %s)', (dataLength[p], '1')) 
            #     mysql.connection.commit()
        flash('La información se guardó en la base de datos')            
        return render_template('data.html')

if __name__ == '__main__':
    app.run(port=4000, debug = True)
