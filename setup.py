from setuptools import setup, find_packages

setup(
    name='RootsWeatherProject',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['pytest', 'fastapi', 'uvicorn'],
    author='John Anthony',
    description='A package holding microservices to create video from compiled weather image data',
    url='https://github.com/your_username/RootsWeatherProject',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
