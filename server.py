from nsfw_detect import NSFWDetector
from flask import Flask, request, render_template, send_from_directory, url_for

from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['NSFW_DETECTED_PHOTOS_DEST'] = 'images'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Sadece fotoğraf yükleyebilirsiniz'),
            FileRequired('Boş bırakılmamalı')
        ]
    )
    submit = SubmitField('Yükle')


@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    is_nsfw = False
    nsfw_url = None
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        nsfw_detector = NSFWDetector(f"uploads/{filename}")
        file_url = url_for('get_file', filename=filename)
        if nsfw_detector.get_is_nsfw():
            is_nsfw = True
            nsfw_url = nsfw_detector.get_censored_image(
                blur_only_detected_parts=True)
    else:
        file_url = None
    return render_template('index.html', form=form, file_url=file_url, nsfw_url=nsfw_url, is_nsfw=is_nsfw)


if __name__ == '__main__':
    app.run(debug=True)
