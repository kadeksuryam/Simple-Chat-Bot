# Hayacaka Bot
Simple task deadline remainder chatbot

## Table of contents
* [General info](#general-info)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [Status](#status)
* [Contact](#contact)

## General info
This project is a project that is obligatory in IF2211-Algorithm Strategies Course class of 2021. We're expected to build a simple chatbot that help user to remember their task deadline.

## Screenshots
![Example screenshot](./img/screenshot.png)

## Technologies
* Flask 
* ReactJS
* Bootstrap
* Kendo React UI

## Setup
- Firstly, you need to install NodeJS and Python3 in your machine. You can grab the installer at [NodeJS](https://nodejs.org/en/download/) and [Python3](https://www.python.org/downloads/)
- After you've intalled those, next, you need to intall `yarn` via npm using command `npm install --global yarn`
- After that, go to `src/api` directory and create virtual environment for the app using command `pip install virtualenv && virtualenv venv`. Note : you may use pip3 instead of pip on Ubuntu/Linux.
- Activate the virtual environment using `venv\Scripts\activate` for Windows and `source venv/bin/activate` for Linux
- Then, go back to `src` directory and install all required libraries using `pip install -r requirements.txt`
- Start the application using `yarn start-api-windows` if you're using windows and `yarn start-api-unix` for Linux
- Now, you can view the webpage on `localhost:5000` via web browser


## Features
List of features ready and TODOs for future development
* Add task
* View task 
* View task deadline
* Update task

To-do list:
* Better text processing
* Better interface

## Status
Project is: _finished_

## Contact
Created by
- Zaidan Naufal Sudrajat - 13518021 (13518021@std.stei.itb.ac.id)
- Kadek Surya Mahardika  - 13519165 (13519165@std.stei.itb.ac.id)
- Akeyla Pradia Naufal   - 13519178 (13519178@std.stei.itb.ac.id)
