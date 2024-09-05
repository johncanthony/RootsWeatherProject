from setuptools import setup, find_packages

setup(
    name='RootsWeatherProject',
    version='1.0.30',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['pytest', 'fastapi', 'pydantic', 'uvicorn', 'httpx', 'redis', 'requests',
                      'beautifulsoup4', 'bs4', 'setuptools', 'ffmpeg-python', 'google_auth_oauthlib',
                      'google-api-python-client'],
    author='John Anthony',
    description='A package holding microservices to create video from compiled weather image data',
    url='https://github.com/johncanthony/RootsWeatherProject',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.12'
    ],
    entry_points={
        'console_scripts': [
            'managerAPI = ManagerAPI.server:launch',
            'imageResolver = ImageResolver.imageResolver.resolver:launch',
            'imageGrabber = ImageGrabber.imageGrabber.grabber:launch',
            'videoMaker = VideoMaker.videoMaker.videomaker:launch',
            'videoUploader = VideoUploader.videoUploader.uploader:launch'
        ]
    }
)
