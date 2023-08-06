from setuptools import setup, find_packages


setup(
    name='gpiosvr',
    version='0.0.1',
    license='MIT',
    author='Brian Hines',
    author_email='brian@projectweekend.net',
    description='RESTful interfaces for Raspberry Pi GPIO',
    url='https://github.com/projectweekend/gpiosvr',
    packages=find_packages(),
    python_requires='>=3',
    install_requires=[
        'falcon',
        'gpiozero',
        'gunicorn',
        'python-mimeparse',
        'six',
    ],
)
