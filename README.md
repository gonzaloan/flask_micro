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
To upload a file to the server. This can be just .jpg, .png, .gif, or .zip
- Method: **POST**
- Path: /attach

Add a file in the body.

#### Responses:

- **201**: The content was uploaded OK. This will response the path of the file
```
{
    "path": [
        "uploaded/32x32_gffwqcloxmkhqmt.png",
        "uploaded/64x64_gffwqcloxmkhqmt.png",
        "uploaded/32x32_kpaqatoxdkjkzpr.png",
        "uploaded/64x64_kpaqatoxdkjkzpr.png",
        "uploaded/32x32_owzypzzbgbikeud.png",
        "uploaded/64x64_owzypzzbgbikeud.png"
    ],
    "response": "file(s) uploaded successfully.",
    "status": 201
}
```
The service, will create a thumbnail for 32x32 and 64x64 maintaining the aspect ratio of the image. If the image is smaller than 128x128, the 
Image will not be modified and will be saved as it is.
- **400**: The file is invalid, it can not be present or has invalid extension.
```
{
    "error": true,
    "message": {
        "response": "File is invalid or is not inside allowed extensions.",
        "status": 400
    }
}
```
- **500**: General error ocurred while uplodading file.
```
{
    "error": true,
    "message": {
        "response": "An error ocurred.",
        "status": 500
    }
}
```





