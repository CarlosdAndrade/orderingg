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

    
#         ACTIVIDAD 3 punto 2, incsiso c
    
    def test_selenium_cant_negativa(self):
        driver = self.driver
        driver.get(self.baseURL)

        boton_agregar = driver.find_element_by_xpath('/html/body/main/div[1]/div/button')
        boton_agregar.click()

        cant =  driver.find_element_by_xpath('//*[@id="quantity"]')
        cerrar_modal = driver.find_element_by_xpath('//*[@id="modal"]/div[2]/footer/button[3]')

        time.sleep(4)
        cerrar_modal.click()

        self.assertTrue(cant >= 1 , "valor negativo")

        
    def tearDown(self):
        self.driver.get('http://localhost:5000/shutdown')

        db.session.remove()
        db.drop_all()
        self.driver.close()
        self.app_context.pop()

# Actividad 3 Inciso 3b

    def test_de_selenium_eliminar(self):
        o = Order(id=1)
        db.session.add(o)

        p = Product(id=1, name='Cuchillo', price=20)
        db.session.add(p)

        orderProduct = OrderProduct(order_id=1, product_id=1, quantity=1, product=p)
        db.session.add(orderProduct)
        db.session.commit()

        driver = self.driver
        driver.get(self.baseURL)
        time.sleep(4)
        delete_product_button = driver.find_element_by_xpath(
            '/html/body/main/div[2]/div/table/tbody/tr[1]/td[6]/button[2]')
        delete_product_button.click()
        time.sleep(4)
        self.assertRaises(NoSuchElementException, driver.find_element_by_xpath, "xpath")
if __name__ == "__main__":
    unittest.main()
