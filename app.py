from flask import Flask, request, render_template
import requests
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/receive_image', methods=['POST'])
def receive_image():
    image_url = request.form.get('image_url')

    response = requests.get(image_url)

    if response.status_code == 200:
        try:
            image = Image.open(BytesIO(response.content))

            # Convierte la imagen al modo RGB
            image = image.convert('RGB')

            # Convierte la imagen a formato base64
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            image_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            return render_template('index.html', image=image_base64)
        except Exception as e:
            return "Error al abrir y procesar la imagen: " + str(e)
    else:
        return "No se pudo obtener la imagen de la URL proporcionada."

if __name__ == '__main__':
    app.run(debug=True)
