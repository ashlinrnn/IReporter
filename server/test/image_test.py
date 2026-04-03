import pytest
from server.models.image.image import Image
from server.models.record.record import Record
from server.config import db




def test_image_instance():
    image = Image()
    assert isinstance(image, Image)


def test_image_creation():
    image = Image(
        image_url="img.png",
        record_id=1
    )

    assert image.image_url == "img.png"
    assert image.record_id == 1



def test_image_save(app):

    record = Record(
        title="Test",
        description="Test description",
        type="red flag"
    )
    db.session.add(record)
    db.session.commit()

    
    image = Image(
        image_url="img.png",
        record_id=record.id
    )
    db.session.add(image)
    db.session.commit()

   
    assert image.id is not None



def test_image_requires_url():
    with pytest.raises(ValueError):
        Image(
            image_url=None,
            record_id=1
        )



def test_image_belongs_to_record(app):
    record = Record(
        title="Test",
        description="Test description",
        type="red flag"
    )
    db.session.add(record)
    db.session.commit()

    image = Image(
        image_url="img.png",
        record_id=record.id
    )
    db.session.add(image)
    db.session.commit()

    assert image.record == record



def test_create_image(client):
    
    client.post('/records', json={
        "title": "Test",
        "description": "Test description",
        "type": "red flag"
    })

    response = client.post('/images', json={
        "image_url": "img.png",
        "record_id": 1
    })

    assert response.status_code == 201


def test_get_images(client):
    response = client.get('/images')
    assert response.status_code == 200


def test_delete_image(client):
    
    client.post('/records', json={
        "title": "Test",
        "description": "Test description",
        "type": "red flag"
    })

    
    client.post('/images', json={
        "image_url": "img.png",
        "record_id": 1
    })

    response = client.delete('/images/1')

    assert response.status_code == 200