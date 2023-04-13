# TTDS Movie Search IR Project 2023
This is a group project for the course [TTDS](https://www.inf.ed.ac.uk/teaching/courses/tts/) (Text Technologies for Data Science) at the University of Edinburgh.

This system is created by 6 member team: Xudong Zhang, Qiunan Wu, Tianrui Xiong, Huacheng Song, Richard Yuan and Hao Zhou

The title of our project: **CineMatch**
Now this websit run on google cloud platform ( http://35.239.129.169:5000/ )


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
