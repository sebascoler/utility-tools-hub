from flask import Flask, render_template, request, send_file, jsonify
import qrcode
from io import BytesIO
import base64
import requests
from PIL import Image
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get API key from environment variable
REMOVEBG_API_KEY = os.getenv('REMOVEBG_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-qr', methods=['POST'])
def generate_qr():
    data = request.json.get('data')
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return jsonify({'qr_code': f'data:image/png;base64,{img_str}'})

@app.route('/generate-whatsapp-link', methods=['POST'])
def generate_whatsapp_link():
    phone = request.json.get('phone')
    message = request.json.get('message', '')
    
    # Clean phone number
    phone = ''.join(filter(str.isdigit, phone))
    
    # Create WhatsApp link
    base_url = "https://wa.me/"
    link = f"{base_url}{phone}"
    if message:
        link += f"?text={message}"
    
    return jsonify({'link': link})

@app.route('/remove-background', methods=['POST'])
def remove_background():
    if not REMOVEBG_API_KEY:
        return jsonify({'error': 'API key not configured. Please set the REMOVEBG_API_KEY environment variable.'}), 500
        
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    
    try:
        # Read the file into memory
        img_data = file.read()
        
        # Call remove.bg API
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': img_data},
            data={'size': 'auto'},
            headers={'X-Api-Key': REMOVEBG_API_KEY},
        )
        
        if response.status_code != 200:
            return jsonify({'error': 'Error processing image with remove.bg API'}), 500
            
        # Convert the response content to base64
        img_str = base64.b64encode(response.content).decode()
        return jsonify({'processed_image': f'data:image/png;base64,{img_str}'})
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return jsonify({'error': 'Error processing image. Please try again.'}), 500

if __name__ == '__main__':
    if not REMOVEBG_API_KEY:
        print("Warning: REMOVEBG_API_KEY environment variable not set. Background removal will not work.")
    port = int(os.getenv('PORT', 5003))
    app.run(host='0.0.0.0', port=port)
