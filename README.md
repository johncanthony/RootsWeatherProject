# Roots Weather Project v2

![Build Workflow](https://github.com/johncanthony/RootsWeatherProject/actions/workflows/python-package.yml/badge.svg) [![PyPI](https://img.shields.io/pypi/v/rootsweatherproject)](https://img.shields.io/pypi/v/rootsweatherproject)


`RootsWeatherProjectv2` is a Python package that contains pipeline microservices designed to create and upload videos (h.264) from compiled NOAA GOES image data. 

Project Youtube Link : [https://www.youtube.com/@rweather](https://www.youtube.com/@rWeather)

## Services

- **Manager API**: Uvicorn wrapped FastAPI server for managing video creation jobs state. [ Supported state backend: Redis ]
- **Image Resolver**: Resolves NOAA GOES image urls for a provided region and image resolution
- **Image Grabber**: Fetches the resolved image urls and stores in the shared file storage. 
- **Video Maker**: FFMpeg runner to encode the images into video (h.264 + AAC). [ Encoding Resolutions - 1920x1080, 1080x1920]
- **Video Uploader**: Uploads encoded video to the host service (Youtube is currently the only supported hosting service)

## Installation

The project can be installed using pip:

```bash
$ pip install RootsWeatherProject
```

## Example Architecture (K3S)
![Architecture Diagram](https://raw.githubusercontent.com/johncanthony/RootsWeatherProject/main/docs/images/RWDArchitecture.png)







