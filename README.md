[![Build Status](https://travis-ci.org/hpanwar08/rest-api-ml-model.svg?branch=master)](https://travis-ci.org/hpanwar08/rest-api-ml-model
)
[![codecov](https://codecov.io/gh/hpanwar08/rest-api-ml-model/branch/master/graph/badge.svg)](https://codecov.io/gh/hpanwar08/rest-api-ml-model)

# Rest API for deploying ML models :zap:

A microservice built on Flask to deploy ML models as rest api.  
This code can be used as a boilerplate for your next machine learning project deployment

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
  ```python -m spacy download en_core_web_sm```
* To start the microservice in dev environment  
  ```python manage.py start --env=dev```  
* To start the microservice in production environment  
  ```python manage.py start```
* To access swagger api, open http://localhost:5000/api/v1/
* To run tests  
  ```python manage.py test```
* Code coverage  
  ```python manage.py cov```

## Input JSON and output JSON

### Sample input json body

URL: http://localhost:5000/api/v1/sentiment  

```json
{
	"text": "i am so happy"
}
```

### Sample output json body

```json
{
    "status": "success",
    "message": {
        "text": "i am so happy",
        "sentiment": "positive",
        "confidence": 0.9986
    }
}
```

### Input json body (bulk predict)

URL: http://localhost:5000/api/v1/sentiments  

```json
{
    "texts": [
        {
            "text": "i am so happy"
        },
        {
            "text": "I am so SAD"
        },
        {
            "text": "today is a Good day"
        }
    ]
}
```

### Output json body

```json
{
    "status": "success",
    "message": [
        {
            "status": "success",
            "text": "i am so happy",
            "sentiment": "positive",
            "confidence": 0.9986
        },
        {
            "status": "success",
            "text": "I am so SAD",
            "sentiment": "negative",
            "confidence": 0.9993
        },
        {
            "status": "success",
            "text": "today is a Good day",
            "sentiment": "positive",
            "confidence": 0.9989
        }
    ]
}
```


## Swagger API

URL: http://localhost:5000/api/v1/  

![Swagger API](/imgs/swagger1.JPG "Swagger API")

### Sentiment Prediction using ```/sentiment``` endpoint

![Sentiment](/imgs/senti1.JPG "Sentiment predict")


## Work in progress... 
<details><summary>TODOs ⏰</summary><p>

- [x] add sentiment analysis model  
- [x] update api  
- [x] add tests  
- [x] add logging
- [ ] add load testing  
- [ ] add database to store predictions  
- [ ] dockerize the app  
- [ ] add authentication  

</p></details>

---
