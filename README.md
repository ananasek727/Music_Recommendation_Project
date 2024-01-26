
# Project of a music recommending application based on emotion recognition

This project aims to develop a web application that recommends music based on emotion recognition from images. The emotion recognition part was implemented with the use of models of deep learning and the dataset, which consists of images from FER2013, KDEF and AffectNet. Models were trained to recognise seven different emotions: anger, disgust, fear, happiness, sadness, surprise and neutrality. The music recommendation part involved integrating the application with the Spotify streaming service and developing a music recommendation algorithm. The application was implemented using the React framework and Python Django framework.
## Table of content
- [Requirement](#Requirement)
- [Installation](#Installation)
- [Manual](#Manual)
- [Credits](#Credits)
## Requirement

Python 3.9, Node.js 20.10.0, Spotify Premium account, \
Requirement for backend are written in file backend/requirement.txt \
Requirement for frontend are written in file frontend/package.json

## Installation

#### Install the dependencies:
```sh
cd  ./front-end
npm install

cd ./backend
pip3 install -r requirements.txt
```
#### Starting application:
For the application to work, the frontend and backend must operate simultaneously.
```sh
frontend:
cd  ./front-end
npm start

backend:
cd ./backend
py manage.py makemigrations
py manage.py migrate
py manage.py runserver
```

Additionally, in order for the user to be able to use the part of the application
related to music recommendation, it is necessary to add the user once to the application
user database on the Spotify API development website. This is a requirement imposed
by Spotify. After completing these steps, the application should be fully functional.

#### Testing:
Frontend:\
In order to
perform all tests, it is also necessary to run the backend server. Backend tests are run by
```sh
cd ./front-end
npm run test
```
Backend:
```sh
cd ./backend
py manage.py test
```
Additionally, it is necessary to manually enter the data used to interact with
Spotify API in the ”test data.yml” file where detailed instructions are located in the
”/backend/spotify” folder.

## Manual
The user manual ia locamen in the PDF file "bachelor_thesis" in seccion 4.14

## Credits
[Błażej Misiura](https://github.com/blazej-misiura)\
[Piotr Możeluk](https://github.com/ananasek727)\
[Justyna Pokora](https://github.com/justynapokora)
