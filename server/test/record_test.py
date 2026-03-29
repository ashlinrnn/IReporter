from server.app import create_app
from server.config import db
from server.models.record.record import Record
from sqlalchemy_serializer import SerializerMixin
class TestRecords:
    
    def test_can_be_intantiated(self):
        record=Record()
        assert record
        assert isinstance(record, Record)
    
    def test_has_attri(self):
        record=Record(user_id=1, 
                    type='red flag', 
                    title='IEBC corruption case to be looked at by the People in charge', 
                    description='any description here will work', 
                    status='pending')
        assert record.id is None
        assert record.user_id==1
        assert record.type=='red flag'
        assert record.status=='pending'
        assert record.title=='IEBC corruption case to be looked at by the People in charge'
        assert record.description=='any description here will work'
    
    def test_inherit_dbModel_SerializerMixin(self):
        record=Record()
        assert isinstance(record,db.Model)
        assert isinstance(record, SerializerMixin)
    
    def test_to_dict(self):
        record=Record(user_id=1, 
                    type='red flag', 
                    title='IEBC corruption case to be looked at by the People in charge', 
                    description='any description here will work', 
                    status='pending')
        assert isinstance(record.to_dict(), dict)