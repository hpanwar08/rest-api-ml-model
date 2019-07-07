[![Build Status](https://travis-ci.org/hpanwar08/rest-api-ml-model.svg?branch=master)](https://travis-ci.org/hpanwar08/rest-api-ml-model
)

# Rest API for deploying ML models :zap:

A microservice built on Flask to deploy ML models as rest api.

## Steps to run
* Create virtual or conda environment and activate it  
  Windows  
  `virtualenv restenv`  
  `restenv\Scripts\activate`  
  Linux  
  `python3 -m venv restenv`  
  `source restenv/bin/activate`
* Install dependencies  
  Edit line 15-17 in requirements.txt according to your OS  
  `pip install -r requirements.txt`  
* Install spacy model  
  `python -m spacy download en_core_web_sm`
* To start the microservice  
  flask default server  
  `python manage.py run`  
  or Gevent production server  
  `python manage.py start`  
* To access swagger api, open http://localhost:5000/api/v1/
* To run tests  
  `python manage.py test`
* Code coverage  
  `python manage.py cov`



## Work in progress... 
### TODO
- [x] add sentiment analysis model
- [ ] update api
- [ ] add tests
- [ ] add load testing
- [ ] add database to store predictions
- [ ] add authentication
