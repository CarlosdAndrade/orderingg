import os 
import unittest

import os
import unittest 

        #modulo de unittest, me permite realizar los test de nuestra aplicacion
from flask import json
from flask_testing import TestCase

from app import create_app, db
from app.models import Product, Order, OrderProduct

basedir = os.path.abspath(os.path.dirname(__file__))

class OrderingTestCase(TestCase): # Creacion de una clase que contiene todos nuestros tests
        
    def create_app(self):
        config_name = 'testing'
        app = create_app()
        app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True
        )
        return app

    # Creamos la base de datos de test
    def setUp(self):
        db.session.commit()
        db.drop_all()
        db.create_all()

    # Destruimos la base de datos de test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_iniciar_sin_productos(self):
        resp = self.client.get('/product')
        data = json.loads(resp.data)

        assert len(data) == 0, "La base de datos tiene productos"
    
    def test_crear_producto(self):
        data = {
            'name': 'Tenedor',
            'price': 50
        }

        resp = self.client.post('/product', data=json.dumps(data), content_type='application/json')
    
        # Verifica que la respuesta tenga el estado 200 (OK)
        self.assert200(resp, "Fallo el POST")
        p = Product.query.all()

        # Verifica que en la lista de productos haya un solo producto
        self.assertEqual(len(p), 1, "No hay productos")
    

#             ACTIVIDAD 3 - punto 2) a)       
    def test_orderProduct_neg (self): #self tiene la referencia del objeto que llamo al metodo.
        
        p = Product (name='mantel', price=70)
        db.session.add(p)
        db.session.commit()
        
        o = Order(id=1)
        db.session.add(o)   
        db.session.commit()

        orderP = OrderProduct(order_id=1, product_id=1,quantity=-5,product=p)      
        o.products.append(orderP)
        db.session.add(o)
        db.session.commit()
        op = OrderProduct.query.all()

        if len(op) == 0: 
            print ("No se creo el producto") 
        else:
            print ("Se creo el producto")

#             ACTIVIDAD 3 - punto 2) b)
    
    def test_GET_funcionamiento (self):
        #creo un producto nuevo
        p= {
        'id':1,
        'name': 'mantel',
        'price': 70
          }
        
        self.client.post('/product', data=json.dumps(p), content_type='application/json')
        
        #creo, guardo la order de este producto nuevo y lo cargo
        o = Order(id=1)
        db.session.add(o)
        db.session.commit()        
        
        #voy a usar client de prueba POST y GET
        op = {"quantity" :10,"order_id":1,"product":p,"product":{"id":1}}
        #Me creo el OrderProduct usando POST como solicitud para agregar el nuevo producto
        self.client.post('/o/1/product', data=json.dumps(op), content_type='application/json')
        
        #Realizo la solicitud GET que me transmita los datos del client
        resp = self.client.get('/o/1/product/1')
        self.assert200(resp, "No se cargo el producto")
        #REVISAR SINTAXIS , CONSULTAR!!        

   
    
# El  if __name__ == '__main__': sirve para que mi fichero test_unit.py se ejecuten, desde la terminal de forma automatica, todos los tests creados
if __name__ == '__main__':  
    unittest.main()

