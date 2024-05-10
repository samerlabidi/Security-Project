"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from hackathone_draft2 import app
from flask import request
import random
import os
from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory
from flask import send_file


def encrypt(file):
    fo = open(file, "rb")
    image=fo.read()
    fo.close()
    image=bytearray(image)
    key=random.randint(0,256)
    for index , value in enumerate(image):
	    image[index] = value^key
    fo=open("enc.jpg","wb")
    imageRes="enc.jpg"
    fo.write(image)
    fo.close()
    return (key,imageRes)

def decrypt(key,file):
    fo = open(file, "rb")
    image=fo.read()
    fo.close()
    image=bytearray(image)
    for index , value in enumerate(image):
	    image[index] = value^key
    fo=open("dec.jpg","wb")
    imageRes="dec.jpg"
    fo.write(image)
    fo.close()
    return imageRes



@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Decrypt',
        year=datetime.now().year,
        message='Upload your encrypted image along with the key'
    )
@app.route('/team')
def team():
    """Renders the team page."""
    return render_template(
        'team.html',
        title='Team',
        year=datetime.now().year,
        message='.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='Encrypt',
        year=datetime.now().year,
        message='Upload the image here'
    )

@app.route('/contact1', methods = ['POST'])  
def contact1():  
    if request.method == 'POST':  
        global f
        f = request.files['file']  
        f.save(f.filename)  
        text = request.form['key']
        key=int(text)
        image=decrypt(key,f.filename)
        return render_template('contact1.html',
        title='Decrypted',
        year=datetime.now().year,
        message='This is your Decrypted image', name = f.filename) 

@app.route('/about1', methods = ['POST'])  
def about1():  
    if request.method == 'POST':  
        global f
        f = request.files['file']  
        f.save(f.filename)  
        key,image=encrypt(f.filename)
        return render_template('about1.html',
        title='Encrypted',
        year=datetime.now().year,
        message='This is your encrypted image', name = f.filename,keys=key,images=image)

@app.route('/return-file')
def return_file():
    return send_file("../enc.jpg",attachment_filename="enc.jpg")

@app.route('/return-file1')
def return_file1():
    return send_file("../dec.jpg",attachment_filename="dec.jpg")