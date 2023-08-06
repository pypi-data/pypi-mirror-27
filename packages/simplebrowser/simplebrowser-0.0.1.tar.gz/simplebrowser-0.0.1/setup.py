from setuptools import setup

setup(
    name='simplebrowser',
    version='0.0.1',
    description='Low-level HTTP browser for easier website interaction',
    license='MIT',
    author='Lukasz Salitra',
    author_email='lukasz.salitra@gmail.com',
    url='https://github.com/estilen/simplebrowser',
    packages=[
        'simplebrowser',
    ],
    install_requires=[
        'requests',
        'bs4',
    ]
)
