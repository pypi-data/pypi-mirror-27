from setuptools import setup

setup(name='openaero',
      version='0.1',
      description='Set of tools to project an aircraft',
      url='https://github.com/CeuAzul/OpenAero',
      author='Ceu Azul Aeronaves',
      author_email='rafael.lehmkuhl93@gmail.com',
      license='MIT',
      packages=['openaero'],
      install_requires=[
          'pytest'
      ],
      zip_safe=False)
