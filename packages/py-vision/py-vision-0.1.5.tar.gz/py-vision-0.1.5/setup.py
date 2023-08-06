from distutils.core import setup

setup(
    name='py-vision',
    version='0.1.5',
    packages=['pyvision', 'pyvision.filters'],
    url='https://github.com/saivarunk/py-vision',
    license='Apache License 2.0',
    author='Varun Kruthiventi, Shiva Katepally',
    author_email='saivarunk@gmail.com, shiva.analytics@gmail.com',
    description='Image Processing Library for Python',
    install_requires=[
        'scipy',
    ]
)
