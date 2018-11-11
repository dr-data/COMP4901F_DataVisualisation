from flask import Flask, render_template
import os

IMAGE_FOLDER = os.path.join('static', 'image')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
 
@app.route("/")
def overview_home():
    imagename = os.path.join(app.config['UPLOAD_FOLDER'], 'paul-smith-193761-unsplash.jpg')
    return render_template('page1.html', user_image = imagename)

@app.route("/page1.html")
def page1():
	imagename = os.path.join(app.config['UPLOAD_FOLDER'], 'paul-smith-193761-unsplash.jpg')
	return render_template('page1.html', user_image = imagename)

@app.route("/page2.html")
def page2():
	imagename = os.path.join(app.config['UPLOAD_FOLDER'], 'paul-smith-193761-unsplash.jpg')
	return render_template('page2.html', user_image = imagename)


## testing

@app.route("/paracoords")
def paracoords_viz():
    return render_template('paracoords.html')
 
if __name__ == "__main__":
	app.static_folder = 'static'
	app.run(debug=True)