from replit import db
from flask import Flask, render_template, redirect, request, make_response
from functions import *
from languages import *
import os
from verify import is_human

app = Flask("app")

@app.route("/")
def index():
  username = request.cookies.get("username")
  if loggedIn():
    if checkUser():
      recent = list(db[username]["files"].keys())
      recent.reverse()
      recentlength = len(recent)
      if recentlength >= 3:
        recent = [recent[0], recent[1], recent[2]]
      return render_template("home.html", username=username, recent=recent, recentlength=recentlength)
    else:
      return redirect("/logout")
  else:
    return render_template("notloggedin.html")

@app.route("/login")
def login():
  if loggedIn():
    return redirect("/")
  return render_template("login.html")

@app.route("/signup")
def signup():
  if loggedIn():
    return redirect("/")
  return render_template("signup.html")

@app.route("/loginsubmit", methods=["GET", "POST"])
def loginsubmit():
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    loggedIn = request.cookies.get("loggedIn")
    if username in db.keys():
      if password == db[username]["password"]:
        resp = make_response(render_template('readcookie.html'))
        resp.set_cookie("loggedIn", "true", httponly=True)
        resp.set_cookie("username", username, httponly=True)
        resp.set_cookie("password", password, httponly=True)
        return resp
      else:
        return render_template("message.html", message="Incorrect password.", loggedIn=loggedIn)
    else:
      return render_template("message.html", message="Account not found.", loggedIn=loggedIn)

@app.route("/createaccount", methods=["GET", "POST"])
def createaccount():
  if request.method == "POST":
    if loggedIn():
      return redirect("/")
    newusername = request.form.get("newusername")
    newpassword = request.form.get("newpassword")
    captcha_response = request.form.get("g-recaptcha-response")
    isLoggedIn = request.cookies.get("loggedIn")
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    cap_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    allchars = letters + cap_letters + numbers + ['_']
    print(newusername)
    for i in newusername:
      if i not in allchars:
        return render_template("message.html", message="Username can only contain alphanumeric characters and underscores.", loggedIn=isLoggedIn)
    if newusername in db.keys():
      return render_template("message.html", message="Username taken.", loggedIn=isLoggedIn)
    if newusername == "":
      return render_template("message.html", message="Please enter a username.", loggedIn=isLoggedIn)
    if newpassword == "":
      return render_template("message.html", message="Please enter a password.", loggedIn=isLoggedIn)
    if is_human(captcha_response):
      db[newusername] = {"password":newpassword, "files":{}}
      print("new account created")
      resp = make_response(render_template('readcookie.html'))
      resp.set_cookie("loggedIn", "true", httponly=True)
      resp.set_cookie("username", newusername, httponly=True)
      resp.set_cookie("password", newpassword, httponly=True)
      return resp
    else:
      print("not verified")
      return render_template("message.html", message="No bots allowed!")

@app.route("/logout")
def logout():
  resp = make_response(render_template('readcookie.html'))
  resp.set_cookie("loggedIn", "false", httponly=True)
  resp.set_cookie("username", "None", httponly=True)
  resp.set_cookie("password", "None", httponly=True)
  return resp

@app.route("/files")
def files():
  username = request.cookies.get("username")
  if loggedIn():
    if checkUser():
      files = list(db[username]["files"].keys())
      order = request.args.get("sort")
      if order == "old":
        sort = "Oldest first"
        pass
      elif order == "a-to-z":
        files.sort()
        sort = "A to Z"
      elif order == "z-to-a":
        files.sort()
        files.reverse()
        sort = "Z to A"
      else:
        files.reverse()
        sort = "Newest first"
      files = " ".join(files)
      return render_template("files.html", files=files, username=username, sort=sort)
    else:
      return redirect("/logout")
  else:
    return redirect("/login")
  
@app.route("/<user>/<name>.<filetype>/edit")
def edit(user, name, filetype):
  username = request.cookies.get("username")
  if loggedIn():
    if checkUser():
      if user in db.keys():
        total = f"{name}.{filetype}"
        if total in db[user]["files"].keys():
          mode = modes[filetype]
          contents = db[user]["files"][total]
          return render_template("editor.html", username=username, contents=contents, filename=total, mode=mode)
      return redirect("/")
    else:
      return redirect("/logout")
  else:
    return redirect("/")

@app.route("/<user>/<name>.<filetype>")
def view(user, name, filetype):
  if user in db.keys():
    total = f"{name}.{filetype}"
    if total in db[user]["files"].keys():
      contents = db[user]["files"][total]
      response = make_response(contents)
      response.mimetype = filetypes[filetype]
      return response
  return redirect("/")

@app.route("/<user>/<name>.py/run")
def runpython(user, name):
  if user in db.keys():
    total = f"{name}.py"
    if total in db[user]["files"].keys():
      contents = db[user]["files"][total]
      return render_template("runpython.html", code=contents)
  return redirect("/")

@app.route("/<user>/<name>.<filetype>/download")
def download(user, name, filetype):
  username = request.cookies.get("username")
  if loggedIn():
    if checkUser():
      if user in db.keys():
        total = f"{name}.{filetype}"
        if total in db[user]["files"].keys():
          contents = db[user]["files"][total]
          response = make_response(contents)
          response.headers['Content-Disposition'] = "attachment; filename=" + total;
          response.mimetype = filetypes[filetype]
          return response
    else:
      return redirect("/logout")
  else:
    return redirect("/")

@app.route("/<user>/<name>/save", methods=["GET", "POST"])
def save(user, name):
  if request.method == "POST":
    username = request.cookies.get("username")
    if loggedIn():
      if checkUser():
        if user in db.keys():
          if user == username:
            if name in db[user]["files"].keys():
              contents = request.json["contents"]
              db[user]["files"][name] = contents
              return "Saved"
        return redirect("/")
      else:
        return redirect("/logout")
    else:
      return redirect("/")

@app.route("/<user>/<name>/rename", methods=["GET", "POST"])
def rename(user, name):
  if request.method == "POST":
    username = request.cookies.get("username")
    if loggedIn():
      if checkUser():
        if user in db.keys():
          if user == username:
            if name in db[user]["files"].keys():
              newname = request.json["newname"]
              if newname not in db[user]["files"].keys():
                contents = db[user]["files"][name]
                del db[user]["files"][name]
                db[user]["files"][newname] = contents
                return "Renamed"
        return redirect("/")
      else:
        return redirect("/logout")
    else:
      return redirect("/")

@app.route("/<user>/<name>/delete", methods=["GET", "POST"])
def delete(user, name):
  if request.method == "POST":
    username = request.cookies.get("username")
    if loggedIn():
      if checkUser():
        if user in db.keys():
          if user == username:
            if name in db[user]["files"].keys():
              del db[user]["files"][name]
              return "Deleted"
        return redirect("/")
      else:
        return redirect("/logout")
    else:
      return redirect("/")

@app.route("/create")
def create():
  username = request.cookies.get("username")
  if loggedIn():
    if checkUser():
      files = list(db[username]["files"].keys())
      files = " ".join(files)
      return render_template("create.html", files=files, username=username)
    else:
      return redirect("logout")
  return redirect("/")

@app.route("/createnewfile", methods=["GET", "POST"])
def newfile():
  if request.method == "POST":
    username = request.cookies.get("username")
    user = request.json["user"]
    newfilename = request.json["newfilename"]
    newfiletype = request.json["newfiletype"]
    total = f"{newfilename}.{newfiletype}"
    if loggedIn():
      if checkUser():
        if user == username:
          if total not in db[user]["files"].keys():
            start = filestarts[newfiletype]
            if newfiletype == "java":
              start = start.replace("FILENAME", newfilename)
            db[user]["files"][total] = start
            return "Saved"
          return redirect("/")
      else:
        return redirect("logout")
    else:
      return redirect("/")

@app.route("/help")
def help():
  if checkUser():
    return render_template("help.html", loggedIn=request.cookies.get("loggedIn"))
  return redirect("/logout")

@app.route(os.getenv("path"))
def path():
  resp = make_response(str(dict(db)))
  resp.mimetype = "application/json"
  return resp

@app.errorhandler(404)
def page_not_found(e):
  if checkUser():
    return render_template("404.html", loggedIn=request.cookies.get("loggedIn")), 404
  return redirect("/logout")

app.run(host="0.0.0.0", port=8080)