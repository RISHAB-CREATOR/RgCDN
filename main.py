import os
import requests
from flask import Flask, jsonify, request, render_template, redirect, flash
import random, time
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'apng', 'png', 'jpg', 'jpeg', 'webp', 'gif'}

def gen_id():
    res = requests.get("https://idgen.i-api.repl.co/uid?length=5").json()["id"]
    return(res)


def download(img_name, url):
    res = requests.get(url)
    u = url.lower()
    if u.endswith('.png'):
      f = open(f"static/uploads/{img_name}.png", "wb")
      f.write(res.content)
      f.close()
      return f"https://rishab-creator.github.io/RishabCDN/static/uploads/{img_name}.png"
    elif u.endswith('.jpg'):
      f = open(f"static/uploads/{img_name}.jpg", "wb")
      f.write(res.content)
      f.close()
      return f"https://rishab-creator.github.io/RishabCDN/static/uploads/{img_name}.jpg"
    elif u.endswith('.jpeg'):
      f = open(f"static/uploads/{img_name}.jpeg", "wb")
      f.write(res.content)
      f.close()
      return f"https://rishab-creator.github.io/RishabCDN/static/uploads/{img_name}.jpeg"
    elif u.endswith('.webp'):
      f = open(f"static/uploads/{img_name}.webp", "wb")
      f.write(res.content)
      f.close()
      return f"https://RishabCDN.intellectual-ga.repl.co/static/uploads/{img_name}.webp"
    elif u.endswith('.gif'):
      f = open(f"static/uploads/{img_name}.gif", "wb")
      f.write(res.content)
      f.close()
      return f"https://rishab-creator.github.io/RishabCDN/static/uploads/{img_name}.gif"
    elif u.endswith('.webm'):
      return f"WebM Not Supported"
    elif u.endswith('.mp4'):
      return f"mp4 Not Supported"
    elif u.endswith('.mp3'):
      return f"mp3 Not Supported"
    else:
      return "The Given File type is not supported!"
    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__, template_folder="html")
app.config['JSON_SORT_KEYS'] = False

uploads_dir = os.path.join(app.instance_path, 'static/uploads')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return render_template("index.html", image=f"Provide an Image")
        if file and allowed_file(file.filename):
            filename = gen_id()+"_"+file.filename.replace(" ", "-").replace("#", "").replace("<", "").replace(">","").replace("?","").replace("&", "")
            file.save(f"static/uploads/{filename}")
            f = open("html/gallery.html", "a")
            data = f"""
            <div class="card">
              <div class="card-body" style="text-align: center;">
                <img id="imgUrlRender" class="card-img-bottom" src="https://rishab-creator.github.io/RishabCDN/static/uploads/{filename}">
              </div>
            </div> \n
            """
            f.write(data)
            f.close()
            return render_template("index.html", image=f"https://rishab-creator.github.io/RishabCDN/static/uploads/{filename}")
        else:
          return render_template("index.html", image=f"File Type not supported!")
    return render_template("index.html")

@app.route('/upload')
def upload():
  url = request.args.get("url")
  pwd = request.args.get("pwd")
  if pwd == os.getenv("pwd"):
    uid = gen_id()
    image_url = download(uid, url)
    data = {
      "image_url": image_url
    }
    return jsonify(data)
  else:
    return redirect("https://rishab-creator.github.io/RishabCDN")

@app.route('/gallery')
def gallery():
  f = open("html/gallery.html", "r") # For Live updates
  data = f.read()
  f.close()
  return data

@app.route("/on")
def on():
  while True:
    res = requests.head("https://rishab-creator.github.io/RishabCDN").status_code
    if res == 200:
      print(res)
      return f"{res}"
    else:
      os.system("python main.py")
      return "Restarting repl"
    time.sleep(60)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=random.randint(2000, 9000))
