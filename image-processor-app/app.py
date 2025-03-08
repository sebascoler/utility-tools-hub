from flask import Flask, render_template, request, send_file
from PIL import Image, ImageEnhance
import requests
import io
import os
from config import REMOVEBG_API_KEY

app = Flask(__name__)

# Ensure uploads directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def enhance_image(image):
    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.5)
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.2)
    
    # Enhance brightness
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.1)
    
    # Enhance color
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.2)
    
    return image

def remove_background(image_data):
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': image_data},
        data={'size': 'auto'},
        headers={'X-Api-Key': REMOVEBG_API_KEY},
    )
    if response.status_code == requests.codes.ok:
        return response.content
    else:
        raise Exception(f"Error removing background: {response.status_code} {response.text}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return 'No image uploaded', 400
    
    file = request.files['image']
    if file.filename == '':
        return 'No selected file', 400

    try:
        # Read the image
        img_data = file.read()
        
        if not REMOVEBG_API_KEY or REMOVEBG_API_KEY == "YOUR-API-KEY":
            return 'Please set up your remove.bg API key in config.py', 400
        
        # Remove background
        try:
            output_data = remove_background(img_data)
        except Exception as e:
            return str(e), 400
        
        # Convert to PIL Image for enhancement
        img = Image.open(io.BytesIO(output_data))
        
        # Enhance image
        enhanced_img = enhance_image(img)
        
        # Save to bytes
        img_byte_arr = io.BytesIO()
        enhanced_img.save(img_byte_arr, format='PNG', quality=95)
        img_byte_arr.seek(0)
        
        return send_file(
            img_byte_arr,
            mimetype='image/png',
            as_attachment=True,
            download_name='processed_image.png'
        )
    
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
