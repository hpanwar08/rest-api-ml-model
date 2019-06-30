[![Build Status](https://travis-ci.org/hpanwar08/rest-api-ml-model.svg?branch=master)](https://travis-ci.org/hpanwar08/rest-api-ml-model
)

# Rest API for deploying ML models

A microservice built on Flask to deploy ML models as api.

## Steps to run
* Create virtual or conda environment and activate it  
  `virtualenv restenv`  
  `restenv\Scripts\activate`  
* Install dependencies  
  `pip install -r requirements.txt`  
* To start the microservice  
  `python manage.py run`  
* To access swagger api, open http://localhost:5000/api/v1/
* To run tests  
  `python manage.py test`

  `python -m spacy download en_core_web_sm`


### Work in progress... 
