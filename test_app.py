import unittest
import app 
from io import BytesIO

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)

    def test_process_image_no_image(self):
        response = self.app.post('/process-image')
        self.assertEqual(response.status_code, 400)
        self.assertIn('application/json', response.content_type)
        self.assertIn('No image part', response.json['error'])

    def test_process_image_with_image(self):
        with open('image.jpg', 'rb') as img:
            imgBytes = BytesIO(img.read())
        
        data = {
            'image': (imgBytes, 'test.jpg')
        }
        
        response = self.app.post('/process-image', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
