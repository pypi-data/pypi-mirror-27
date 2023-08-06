from setuptools import setup

setup(
    name='clitellum',
    version='3.0.3',
    packages=['clitellum', 'clitellum.core', 'clitellum.endpoints',
              'clitellum.endpoints.channels'],
    package_dir={'clitellum': 'clitellum'},
    url='https://gitlab.com/clitellum/clitellum/wikis/home',
    license='GPL',
    author='Sergio.Bermudez',
    author_email='sbermudezlozano@gmail.com',
    description='Clitellum Microservice Framework',
    extras_require={
    },
    install_requires=['pika', 'pymongo','zmq', 'pyyaml', 'fluidity-sm', 'python-dateutil']
)
