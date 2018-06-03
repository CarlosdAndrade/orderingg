import unittest
import os
import time
import threading

from selenium import webdriver

from app import create_app, db
from app.models import Product, Order, OrderProduct

basedir = os.path.abspath(os.path.dirname(__file__))

from werkzeug.serving import make_server

class Ordering(unittest.TestCase):
    # Creamos la base de datos de test
    def setUp(self):
        self.app = create_app()
        self.app.config.update(
            SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'test.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            TESTING=True
        )

        self.app_context = self.app.app_context()
        self.app_context.push()

        self.baseURL = 'http://localhost:5000'

        db.session.commit()
        db.drop_all()
        db.create_all()

        self.t = threading.Thread(target=self.app.run)
        self.t.start()

        time.sleep(1)

        self.driver = webdriver.Firefox()

    def test_title(self):
        driver = self.driver
        driver.get(self.baseURL)
        add_product_button = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
        add_product_button.click()
        modal = driver.find_element_by_id('modal')
        assert modal.is_displayed(), "El modal no esta visible"

     

     #-------------ACTIVIDAD 3 - punto 1)  b) -------------------------------------------------------
    
    def test_InfoModalEditar(self):
        #Para que este test  funcione debe haber productos cargados sino fallara ya que sin productos 
        #no se puede editar
        #Genero una orden
        o = Order(id= 1)
        db.session.add(o)
        #Genero un producto
        p = Product(id= 1, name= 'vaso', price= 500)
        db.session.add(p)
        #Relaciono orden y producto
        orderProduct = OrderProduct(order_id= 1, product_id= 1, quantity= 1, product= p)
        db.session.add(orderProduct)
        db.session.commit()
        #Me traigo la base
        driver = self.driver
        driver.get(self.baseURL)
        #tiempo de espera de 4 segundos
        time.sleep(4)
        #busco el boton de edicion que esta en la fila de productos junto al boton de eliminar y lo clickeo
        boton_editar = driver.find_element_by_xpath('/html/body/main/div[2]/div/table/tbody/tr[1]/td[6]/button[1]')
        boton_editar.click()
        #busco las referencias que tiene el producto tanto selecion como la cantidad 
        producto = driver.find_element_by_xpath('//*[@id="select-prod"]')
        cantidad = driver.find_element_by_xpath('//*[@id="quantity"]')
        #tomo el atributo nombre
        value_prod = producto.get_attribute("value")
        #tomo el atributo de su cantidad
        value_cant = cantidad.get_attribute("value")
        #identifico el boton que cierra el modal y lo clickeo
        boton_cerrar_modal = driver.find_element_by_xpath('//*[@id="modal"]/div[2]/footer/button[3]')
        time.sleep(5)
        boton_cerrar_modal.click()
        #finalmente evaluo si es verdero que tanto el valor como la cantidad sean distintas de vacio o 
        # devuelve que no tienen informacion cargada
        self.assertTrue(value_prod != "", "No tiene informacion")
        self.assertTrue(value_cant != "", "No tiene informacion")

    
    #ACTIVIDAD OPCIONAL ASIGNADA 2)b)

    def test_Notificacion_Aparece(self):
        
        #Genero producto
        p = Product(id=1, name = 'Mesa', price = 500)
        db.session.add(p)
        
        #Genero una order
        o = Order(id=1)
        db.session.add(o)
        
        #Asigno la orden al producto creado
        op = OrderProduct(product=p, quantity=1)
        db.session.add(op)
        db.session.commit()

        #Me traigo la base
        driver = self.driver
        driver.get(self.baseURL)
        #Tomo la ruta del boton agregar producto copiando su xpath
        agregar = driver.find_element_by_xpath("/html/body/main/div[1]/div/button").click()
        #Busco el elemento seleccionar producto 
        producto = driver.find_element_by_id("select-prod")
        #Selecciono el elemento visible Mesa en este caso ya q es el que quiero repetir guardar
        #la mesa para que me salte la notificacion
        producto.select_by_visible_text('Mesa')
        #Busco el elemento cantidad
        cantidad = driver.find_element_by_id("quantity")
        #Edito la cantidad 
        cantidad.SendKeys('1')
        #Busco el elemento boton guardar y clickeo
        guardar = driver.find_element_by_id("save-button").click()
        #busco el elemento notificacion y lo muestro
        noti = driver.find_element_by_id('noti').is_displayed()
        #verifico que aparesca la notificacion
        self.assertEqual(noti, True,"No pararece la notifacion")
        #LAS SIGUIENTES SON OPCIONES QUE SE ME OCURRIERON PARA QUE NO ME FALLE EL TEST:
        #self.assertEqual(noti, False,"No pararece la notifacion")
        #self.assertEqual(len(noti),"No se pueden agregar productos con nombre repetido", "No hay productos")
        #self.assertTrue(noti=="No se pueden agregar productos con nombre repetido","No hay productos")



        
    def tearDown(self):
        self.driver.get('http://localhost:5000/shutdown')
        db.session.remove()
        db.drop_all()
        self.driver.close()
        self.app_context.pop()

  
if __name__ == "__main__":
    unittest.main() 

