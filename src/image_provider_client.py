import requests

class ImageProviderClient:
    def __init__(self, host: str):
        self.host = host

    def get_image(self, id):
        try:
            res = requests.get(
            f'{self.host}/images/{id}', timeout=5
            )
        except requests.Timeout:
            return {'error': 'Timeout exceeded'}, 504
        except requests.RequestException as e:
            return {"error": str(e)}, 500
        if res.status_code != 200:
            return {'error': 'image not found'}, res.status_code
        return {'image': res.content}, res.status_code
    