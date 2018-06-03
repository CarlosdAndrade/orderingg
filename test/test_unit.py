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
        #Creo la orden
        o = Order(id= 1)
        db.session.add(o)   

        #Creo el producto
        p = Product(id= 1, name= 'vaso', price= 500)
        db.session.add(p)

        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 1, product= p)
        db.session.add(orderProduct)
        db.session.commit()
        data = {
            'quantity': 10
        }
        self.client.put('order/1/product/1', data=json.dumps(data), content_type='application/json')
        arg = 1,1
        prod = OrderProduct.query.get(arg)

        self.assertTrue(prod.quantity == 10, "Fallo el metodo PUT")
        self.assert200(resp, "Fallo el funcionamiento del metodo PUT")

        # Verifica que la respuesta tenga el estado 200 (OK)
        self.assert200(resp, "Fallo el POST")
        p = Product.query.all()

        # Verifica que en la lista de productos haya un solo producto
        self.assertEqual(len(p), 1, "No hay productos")
     

     #--------------------ACTIVIDAD 3 - punto 1) c) ------------------------------------------------
    
    def test_OrderPrice(self): 
        
        #Creo la orden
        o = Order(id= 1)
        db.session.add(o)
        
        #Creo el producto
        p = Product(id= 1, name= 'vaso', price= 500)
        db.session.add(p)
        
        #Creo la relacion entre el producto y la orden
        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 10, product= p)
        db.session.add(orderProduct)
        db.session.commit()
        
        #Verifico que el primero y el segundo sean distintos 
        orden= Order.query.get(1)
        totalPrice = orden.orderPrice
        self.assertNotEqual(150, totalPrice, "El precio total no se calcula bien")   


        # ACTIVIDAD 3 - punto 2) a)  
    
    def test_orderProduct_neg (self):   #self tiene la referencia del objeto que llamo al metodo.        
        #correcion al no asignar un id al producto para posterior relacion y comparacion
        p = Product (id= 1, name='mantel', price=70)
        db.session.add(p)
                
        o = Order(id=1)
        db.session.add(o)   
        db.session.commit()

        #relacion con el order y agrego un quantity negativo
        orderP = OrderProduct(order_id=1, product_id=1,quantity=-5,product=p)      
        db.session.add(orderP)
        db.session.commit() 

        existe = OrderProduct.query.all()
        #voy a usar el assertEqual y no el assertTrue o False ya que me da un mejor msj de error, en caso de error
        #correcion sintaxis/ interpretacion, resolviendo con assert...
        #pruebo que los argumentos Si son iguales. Si los valores NO son iguales, la prueba falla
        self.assertEqual(len(existe),1,"No paso el test,se creo el producto")
        # db.session.rollback ()

    def test_Get_funcionamiento (self):
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
    	self.client.post('/order/1/product', data=json.dumps(op), content_type='application/json')
    	
    	#Realizo la solicitud GET que me transmita los datos del client
    	resp = self.client.get('/order/1/product/1')
    	self.assert200(resp, "No se cargo el producto")
    	#CORRECION VISTA EN CLASE, SE MODIFICO EL ENDPOINT, TENIA MAL EL CONCEPTO!!        


     #-------------------- ACTIVIDAD 3) - punto 3) a)------------------------------------------------------------
   
    def test_borrar(self):
      o = Order(id=1)
      db.session.add(o)

      p = Product(id=1, name='Cuchillo', price=20)
      db.session.add(p)

      orderProduct = OrderProduct(order_id=1, product_id=1, quantity=1, product=p)
      db.session.add(orderProduct)
      db.session.commit()

      resp = self.client.delete('order/1/product/1')

      self.assert200(resp, "Fallo el DELETE")

     
     #--------------------- ACTIVIDAD 3) - punto 3) c)-----------------------------------------------------------
     
    def test_name_vacio(self):
        data = {
            'name': '',
            'price': 30
        }

        resp = self.client.post('/product', data=json.dumps(data), content_type='application/json')

        #self.assert (resp != 200, 'Fallo el test, se creo un producto de nombre vacio')


# El  if __name__ == '__main__': sirve para que mi fichero test_unit.py se ejecuten, desde la terminal de forma automatica, todos los tests creados
if __name__ == '__main__':
    unittest.main()
