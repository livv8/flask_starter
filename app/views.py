"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from werkzeug.utils import secure_filename
from app import app
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory
from .form import addPropertyform, FormPhoto



###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/property', methods=['POST'])
def property():
    form=addPropertyform()
    if request.method == 'POST':
         if form.validate_on_submit():
             title=form.title.data
             numofbedrooms= form. numofbedrooms.data
             numofbath= form.numofbath.data 
             location= form.location.data
             price= form.price.data
             housetype=form.housetype.data
             descript=form.descript.data 
             
             flash('Form Completed', 'success')
             return redirect("/properties")
             return render_template('property.html', title=title, numofbedrooms=numofbedrooms, numofbath=numofbath, location=location, price=price, housetype=housetype, descript=descript)
         
         flash_errors(form)
    return render_template('property.html', form=form)



@app.route('/process-file', methods=['POST', 'GET'])
def process_file():
    photoform= FormPhoto()
    
    if request.method =='POST' and photoform.validate_on_submit():
        db = connect_db()
            cur = db.cursor()
            cur.execute('insert into property (name, email)
            values (%s, %s)', (request.form['name'],
            request.form['email']))
            db.commit()
            flash('New user was successfully added')
            return redirect(url_for('property'))
            return render_template('properties.html')
        file=request.files['file']
        filename= secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('property.html', filename=filename)
    
    flash_errors(photoform)
    return render_template('property.html', form=photoform)

@app.route("/uploads/<filename>")
def get_uploaded_file(filename):
    root_dir = os.getcwd()

    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)
      


@app.route('/properties')
def properties():
    return render_template('properties.html')

@app.route('/property/<propertyid>')
def propertyid():
    return render_template('property.html')


###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
