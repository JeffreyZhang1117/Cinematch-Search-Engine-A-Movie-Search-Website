# TTDS Movie Search IR Project 2023
This is a group project for the course [TTDS](https://www.inf.ed.ac.uk/teaching/courses/tts/) (Text Technologies for Data Science) at the University of Edinburgh. 

The title of our project: **CineMatch(CNM)**
Now this websit run on google cloud platform (http://34.123.106.69:5000/)


## Summary

The project consists of 4 basic parts:

+ Data_Collection: crawl data from web page
+ ir_eval: IR indexing and ranking
+ GUI: built with Vue
+ API: built with Flask

## Setting up
```js
pip install -r requirements.txt
```
### Run the frontend
```js
cd client
npm install
npm run serve
npm run build   
```

### Run the backend
```js
python3 run.py
```
