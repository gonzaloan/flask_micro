# Flash Micro-Web-Framework Challenge

This repo is for the flask micro web framework challenge for **Service Rocket** application.
My name is Gonzalo Muñoz (gonzaloan.munoz@gmail.com)


## Build and deploy in local environment
This project use Docker to simplify the usage of the application 

### Build
To build the docker image:

```
$ docker build -t images_micro:latest . 
```

### Run the image

To run the image:

```
$ docker run -d -p 5000:5000 images_micro 
```

### Run Test

To run test, the application uses *Pytest*.
You can run all suites:
```
$ pytest
```

## Endpoints
This API has the following endpoints to be accessed without authorization.

### Upload Simple File.
To upload a file to the server. This can be just .jpg, .png, .gif
- Method: **POST**
- Path: /attach

Add a file in the body.

#### Responses:

- **201**: The content was uploaded OK. This will response the path of the file
- **400**: The file is invalid, it can not be present or has invalid extension.
- **500**: General error ocurred while uplodading file.

### Upload Simple File.
To upload a file to the server. This can be just .jpg, .png, .gif
- Method: **POST**
- Path: /attach



