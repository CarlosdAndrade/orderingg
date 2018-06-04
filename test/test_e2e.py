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

        # ACTIVIDAD OPCIONAL ASIGNADA 2)b)

    def test_Notificacion_Aparece(self):

          # Genero producto
          p = Product(id=1, name='Vaso', price=500)
          db.session.add(p)
          # Genero una order
          o = Order(id=1)
          db.session.add(o)

          # Asigno la orden al producto creado
          op = OrderProduct(order_id=1, product_id=1, product=p, quantity=1)
          db.session.add(op)
          db.session.commit()

          # Me traigo la base
          driver = self.driver
          driver.get(self.baseURL)
          time.sleep(4)

          # Tomo la ruta del boton agregar producto copiando su xpath
          agregar = driver.find_element_by_xpath("/html/body/main/div[1]/div/button").click()

          # Busco el elemento seleccionar producto
          selecproducto = driver.find_element_by_id('select-prod')
          selecproducto.click()

          # Abro la lista desplegable y elijo el producto Vaso que se encuentra en la opción 2
          selecc_prod_opc = driver.find_element_by_xpath('//*[@id="select-prod"]/option[2]')
          selecc_prod_opc.click()

          # Busco el elemento cantidad
          cantidad = driver.find_element_by_xpath('//*[@id="quantity"]')

          # Edito la cantidad
          cant_val = 3
          cantidad.send_keys(str(cant_val))

          #Busco el elemento guardar y le hago un click
          guardar = driver.find_element_by_xpath('//*[@id="save-button"]')
          guardar.click()

          # busco el elemento notificacion
          notificacion = driver.find_element_by_xpath('//*[@id="select"]/p')

          # verifico que aparesca la notificacion
          self.assertEqual(notificacion.is_displayed(),True,"No pararece la notifacion de producto duplicado")




    def tearDown(self):
        self.driver.get('http://localhost:5000/shutdown')
        db.session.remove()
        db.drop_all()
        self.driver.close()
        self.app_context.pop()


if __name__ == "__main__":
    unittest.main()