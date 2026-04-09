from flask import request,g, make_response
from flask_restful import Resource
from ....utils.auth import login_required, admin_required, can_edit_record
from ... import Record
from ....config import db
from werkzeug.exceptions import Forbidden
from ....services.email_service import send_status_update_email

class RecordResource(Resource):
    @login_required
    def patch(self,id):
        record=db.session.get(Record,id)
        if not record:
            return {'message':'Record not found!'},404
        if not can_edit_record(record,g.current_user):
            return {'message':'Not allowed to edit this record'},403
        
        for field,value in request.json.items():
            if hasattr(record,field):
                if field =='status':
                    raise Forbidden('Admin privileges required')
                setattr(record,field,value)
        
        try:
            db.session.commit()
            return make_response({'data':record.to_dict()},200)
        except Exception as e:
            db.session.rollback()
            return {'message':[str(e)]}
    
    @login_required
    def delete(self,id):
        record=db.session.get(Record,id)
        if not record:
            return {'message':'Record not found!'},404
        if not can_edit_record(record,g.current_user):
            return {'message':'Not allowed to edit this record'},403
        
        db.session.delete(record)
        db.session.commit()
        
        return make_response({},204)

class RecordCreateResource(Resource):
    @login_required
    def post(self):
        data=request.get_json()
        record=Record(
            user_id=g.current_user.id,
            title=data.get('title'),
            description=data.get('description'),
            type=data.get('type'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            status='pending'
        )
        try:
            db.session.add(record)
            db.session.commit()
            return make_response({'data':record.to_dict()},201)
        except Exception as e:
            db.session.rollback()
            return {'message':str(e)},400

class AdminRecordResource(Resource):
    @admin_required 
    def patch(self, id):
        record = db.session.get(Record, id)
        if not record:
            return {'message': 'Record not found!'}, 404
        
        data = request.get_json()
        if 'status' not in data:
            return {'message': 'Only status field can be updated'}, 400
        new_status = data['status']

        try:
            setattr(record, 'status', new_status)
            db.session.commit()
            
            try:
                send_status_update_email(
                    recipient_email=record.user.email,
                    recipient_name=record.user.username,
                    record_title=record.title,
                    new_status=new_status
                )
            except Exception as e:
                # Log the message but don't break the response
                print(f"Email failed: {e}")
            
            return make_response({'data': record.to_dict()}, 200)
        except ValueError as e:
            
            return {'message': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': [str(e)]}, 400
