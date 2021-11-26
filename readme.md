# Django Gramm.
## Overview.
This program is an Instagram clone with basic functionality,  

such as: creating posts, commenting on posts, liking posts,  

subscribing to other users and much more.

## Requirements
All necessary requirements are specified in the file requirements.txt  

Additionally, you must have Node.js installed 

## Installation.
All you have to do is clone the git repository.  

At the cli just type:  
`git clone https://git.foxminded.com.ua/Fan4ik/task12_create_basic_application.git`

## After installation.
1. Python Modules.
    1. Installing all python modules via command `pip install -r requirements.txt`

2. Webpack.
    1. Go to the webpack_dir directory and install all necessary node packages:  
    `cd webpack_dir`  
    `npm install` 
    2. Build the main js file - bundle.js
    `npm run build` or `npx webpack`  
    
2. Database
    1. You must set your own database settings.

3. Env Variables
    1. You must determine all Env variables that uses in settings.py

## Running.
After small project settings you can start the server with the command from the root dir  
`python manage.py runserver`

## Links.
https://django-gramm.herokuapp.com

## License.
MIT