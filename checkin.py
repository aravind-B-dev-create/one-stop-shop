from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
from bson.objectid import ObjectId
from passlib.hash import sha256_crypt

truepass = "hello world"
pass1 = sha256_crypt.hash(truepass)
print(sha256_crypt.verify("hello world", pass1))
