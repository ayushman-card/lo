from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import subprocess
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ENHANCED_FOLDER = 'enhanced'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ENHANCED_FOLDER'] = ENHANCED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENHANCED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def enhance_video(input_path, output_path):
    # Simulated enhancement using FFmpeg scaling (e.g., 720p to 1080p)
    command = [
        'ffmpeg', '-i', input_path,
        '-vf', 'scale=1920:1080',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '22',
        '-c:a', 'copy',
        output_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return redirect(request.url)
    file = request.files['video']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_path = os.path.join(app.config['ENHANCED_FOLDER'], f"enhanced_{filename}")
        file.save(input_path)
        enhance_video(input_path, output_path)
        return render_template('result.html', filename=f"enhanced_{filename}")
    return "Invalid file format"

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['ENHANCED_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
