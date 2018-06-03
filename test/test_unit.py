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




     #--------------------ACTIVIDAD 3 - punto 1) a) ----------------------------------------------------------

    def test_put(self):
        
        #Creo el producto
        p = Product(id= 1, name= 'vaso', price= 500)
        db.session.add(p)

        #Creo la orden
        o = Order(id= 1)
        db.session.add(o)   
        
        #Relaciono la orden al producto creado
        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 1, product= p)
        db.session.add(orderProduct)
        db.session.commit()
        #Este sera el dato que voy a modificar con canidad 10 en el producto que acabo de cargar
        data = {
            'quantity': 5
        }
        #Invoco el metodo put en el documento de prueba json en el argumento orden 1 con producto 1
        self.client.put('order/1/product/1', data=json.dumps(data), content_type='application/json')
        arg = 1,1
        #Me traigo este argumento
        prod = OrderProduct.query.get(arg)
        #Verifico q la cantidad del producto es la modificada en este caso 5
        self.assertTrue(prod.quantity == 5, "Fallo el metodo PUT")
        #Me traigo todos los productos y verifico que haya un solo producto en lista
        p = Product.query.all()
        self.assertEqual(len(p), 1, "No hay productos")
     

     #--------------------ACTIVIDAD 3 - punto 1) c) ------------------------------------------------
    
    def test_OrderPrice(self): 
        
        #Creo el producto
        p = Product(id= 1, name= 'vaso', price= 500)
        db.session.add(p)
        
        #Creo la orden
        o = Order(id= 1)
        db.session.add(o)
        
        #Creo la relacion entre el producto y la orden
        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 4, product= p)
        db.session.add(orderProduct)
        db.session.commit()
        
        #me traigo la order creada y verifico que el precio se haya calculado bien
        orden= Order.query.get(1)
        totalPrice = orden.orderPrice
        self.assertEqual(2000, totalPrice, "El precio total no se calcula bien")
        #En este caso me pasa porque el vaso de 500 mangos y la cantidad 4 me da 2000 p   


 # El  if __name__ == '__main__': sirve para que mi fichero test_unit.py se ejecuten, desde la terminal de forma automatica, todos los tests creados
if __name__ == '__main__':
    unittest.main()




