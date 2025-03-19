from setuptools import setup
import os

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = f"{lib_folder}/requirements.txt"
install_requires = [] # Here we'll add: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirement_path):
      with open(requirement_path) as f:
            install_requires = f.read().splitlines()

setup(name='inventario',
      version='0.0.1+devel',
      description='Servicios REST para el inventario de aplicaciones de la GSS',
      url='https://servicios.jcyl.es/gitlab/gerencia-de-servicios-sociales/direcci-n-general-de-familias-infancia-y-atenci-n-a-la-diversidad/familias/si-familias/reports-microservice.git',
      author='Ángel de Jesús Vizcaíno',
      author_email='jesvizan@jcyl.es',
      license='MIT',
      packages=['inventario-backend'],
      install_requires=install_requires,
      zip_safe=False)