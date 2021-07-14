from flask import request
from replit import db

def loggedIn():
  cookie = request.cookies.get("loggedIn")
  if cookie == "true":
    return True
  return False

def checkUser():
  username = request.cookies.get("username")
  password = request.cookies.get("password")
  loggedIn = request.cookies.get("loggedIn")
  if loggedIn != "true":
    return True
  if username != None and username in db.keys():
    if password == db[username]["password"]:
      return True
  return False