from flask import request
from flask_restplus import Resource

from app.portal.api.util.decorator import token_required, admin_token_required
from .util.dto import StudentDto
from ..service.userService import save_new_user, get_all_users, get_student


api = StudentDto.api
student = StudentDto.student


@api.route('/')
class StudentList(Resource):

    @api.doc('list_of_students')
    @admin_token_required
    @api.marshal_list_with(student, envelope='data')
    def get(self):
        """List all available students"""
        return get_all_users()

    @api.response(201, 'Category successfully created.')
    @api.doc('create a new student')
    @api.expect(student)
    def post(self):
        """Creates a new Student ."""
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The Student identifier')
@api.response(404, 'User not found.')
class Student(Resource):

    @api.doc('get a student')
    @api.marshal_with(student)
    def get(self, public_id):
        """get a student given its identifier"""
        _student = get_student(public_id)
        if not _student:
            api.abort(404)
        else:
            return _student
