import io
import json


def test_attach_image_ok(test_client):
    file_name = 'test.jpg'
    data = {
        'file': (io.BytesIO(b"abcdef"), file_name)
    }
    response = test_client.post('/attach', data=data)
    json_data = json.loads(response.data)
    assert response.status_code == 201
    assert json_data['path'] != ''
    assert json_data['path'] != file_name # It should be another random name
    assert json_data['response'] == 'file uploaded successfully.'


def test_attach_image_without_attachment(test_client):
    data = {}
    response = test_client.post('/attach', data=data)
    assert response.status_code == 400


def test_attach_image_with_pdf_invalid_file(test_client):
    file_name = 'test.pdf'
    data = {
        'file': (io.BytesIO(b"asdsdsbcdef"), file_name)
    }
    response = test_client.post('/attach', data=data)
    assert response.status_code == 400


