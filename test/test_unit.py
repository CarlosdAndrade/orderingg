import os
import unittest

from flask import json
from flask_testing import TestCase
from app import create_app, db
from app.models import Product, Order, OrderProduct

basedir = os.path.abspath(os.path.dirname(__file__))

class OrderingTestCase(TestCase):
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

#---------------------------ACTIVIDAD 3 - punto 1)  a) ---------------------------------------------
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
        #self.assertTrue(prod.quantity == 10, "Fallo el metodo PUT")
        #self.assert200(resp, "Fallo el funcionamiento del metodo PUT")

#--------------------------ACTIVIDAD 3 - punto 1)  c) ------------------------------------------------
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

#-----------------------ACTIVIDAD 3 - punto 3)   a)--------------------------------------------------- 
    def test_delete(self):
        #Creo la orden
        o = Order(id= 1)
        db.session.add(o)
        #Creo el producto
        p = Product(id= 1, name= 'cuchara', price= 230)
        db.session.add(p)
        #Creo la relacion entre el producto y la orden
        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 1, product= p)
        db.session.add(orderProduct)
        db.session.commit()
        
        resp = self.client.delete('order/1/product/1')

     #   self.assert200(resp, "Fallo el DELETE")


if __name__ == '__main__':
    unittest.main()