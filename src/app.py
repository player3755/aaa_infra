from flask import Flask, request
import logging
import io
from image_provider_client import ImageProviderClient
from models.plate_reader import PlateReader, InvalidImage

logger = logging.getLogger('Logger')
app = Flask(__name__)
image_provider = ImageProviderClient(host='http://89.169.157.72:8080')
plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')

@app.route('/')
def hello():
    return '<h1><center>Сервис поможет заосиарить номер!</center></h1>'

@app.route('/single_plate', methods=['POST'])
def single_plate():
    if 'id' not in request.json:
        logging.error('ids field not found')
        return {'error': 'id field not found'}, 400
    
    id = request.json['id']
    return read_plate(id)
    
@app.route('/multiple_plates', methods=['POST'])
def multiple_plates():
    if 'ids' not in request.json:
        logging.error('ids field not found')
        return {'error': 'ids field not found'}, 400
    
    response = []
    for id in request.json['ids']:
        msg, code = read_plate(id)
        if code == 200:
            response.append({'id': id, 'plate': msg})
        else:
            logging.error(f'image {id} error')
            response.append({'id': id, 'error': code})
    return response, 200

def read_plate(id: int):
    logging.info(id)
    if not id: 
        logging.error('invalid id')
        return {'error': 'invalid id'}, 400
    
    msg, code = image_provider.get_image(id=id)
    
    if code != 200:
        logging.error('image error')
        return msg, code
    im = io.BytesIO(msg['image'])
    
    try:
        res = plate_reader.read_text(im)
    except InvalidImage:
        logging.error('invalid image')
        return {'error': 'invalid image'}, 400

    return {
        'plate_number': res,
    }, 200


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.json.ensure_ascii = False
    app.run(host='0.0.0.0', port=8080, debug=True)
