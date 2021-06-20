import io
import json
import zipfile

from utils.constants import ERROR_ZIP_FILE_RESPONSE


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
    assert json_data['response'] == 'file(s) uploaded successfully.'


def test_attach_image_without_attachment(test_client):
    data = {}
    response = test_client.post('/attach', data=data)
    assert response.status_code == 400


def test_attach_image_with_pdf_invalid_file(test_client):
    file_name = 'test.pdf'
    print('weás: ', (io.BytesIO(b"asdsdsbcdef"), file_name))
    data = {
        'file': (io.BytesIO(b"asdsdsbcdef"), file_name)
    }
    response = test_client.post('/attach', data=data)
    assert response.status_code == 400


def test_attach_zip_file_ok(test_client):
    zip_name = 'test.zip'
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, data in [('1.png', io.BytesIO(b'111')), ('2.png', io.BytesIO(b'222'))]:
            zip_file.writestr(file_name, data.getvalue())
    data = {
        'file': (io.BytesIO(zip_buffer.getvalue()), zip_name)
    }
    response = test_client.post('/attach', data=data)
    json_data = json.loads(response.data)
    assert response.status_code == 201
    assert len(json_data['path']) == 2
    assert json_data['response'] == 'file(s) uploaded successfully.'


def test_attach_zip_file_has_no_valid_files_inside(test_client):
    zip_name = 'test2.zip'
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, data in [('1.pdf', io.BytesIO(b'111')), ('2.exe', io.BytesIO(b'222'))]:
            zip_file.writestr(file_name, data.getvalue())
    data = {
        'file': (io.BytesIO(zip_buffer.getvalue()), zip_name)
    }
    response = test_client.post('/attach', data=data)
    assert response.status_code == 400


def test_attach_zip_file_is_empty(test_client):
    zip_name = 'test2.zip'
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        pass
    data = {
        'file': (io.BytesIO(zip_buffer.getvalue()), zip_name)
    }
    response = test_client.post('/attach', data=data)
    json_data = json.loads(response.data)
    assert response.status_code == 400
    assert json_data['message']['response'] == ERROR_ZIP_FILE_RESPONSE['response']





