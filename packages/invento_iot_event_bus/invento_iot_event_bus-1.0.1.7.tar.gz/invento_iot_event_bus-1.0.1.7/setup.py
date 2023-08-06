from setuptools import setup, find_packages

setup(name='invento_iot_event_bus',
      version='1.0.1.7',
      description='Iot invento mqtt event bus',
      url='https://github.com/jakekutsel/invento-event-bus',
      author='Jake Kutsel',
      author_email='e.kutel@invento.by',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'pika',
      ],
      include_package_data=True,
      zip_safe=False)
