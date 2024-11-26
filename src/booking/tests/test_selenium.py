# from selenium.webdriver.edge.options import Options
# from selenium import webdriver
# from django.test import TestCase
# import os
# import time
# import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.local')
# django.setup()


# class TestMainFunctional(TestCase):

#     def test_get_index_page(self):
#         options = Options()
#         options.add_experimental_option('detach', True)
#         self.browser = webdriver.Edge()
#         time.sleep(2)
        
#         self.browser.get('http://127.0.0.1:8030/trainers')
#         time.sleep(2)

#         self.assertEqual(self.browser.title, 'Наші тренери - Fitness First')
#         self.browser.quit()
