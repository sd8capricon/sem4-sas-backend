import hashlib, os

from api.serializers import AttendanceSerializer, StatSerializer, TeacherViewSerializer
from api.models import Attendance, Course, Lec_Stat, Student, Teacher


# View all Teachers
def teachers_details(req):
    if req.method == 'GET':
        teacher = Teacher.objects.all()
        serializer = TeacherViewSerializer(teacher, many=True)
        return serializer.data

def teacher(req, teacher_id):
    if req.method == 'GET':
        try:
            teacher = Teacher.objects.get(pk=teacher_id)
            serializer = TeacherViewSerializer(teacher)
            return serializer.data
        except Exception as e:
            error = {'error': str(e)}
            return error
    elif req.method == 'POST':
        try:
            data = req.data
            password = (os.environ.get('PASS_SALT')+data['password']).encode('utf-8')
            h = hashlib.sha256(password).hexdigest()
            t = Teacher(username=data['username'], password=h, f_name=data['f_name'], l_name=data['l_name'])
            t.save()
            serializer = TeacherViewSerializer(t)
            return serializer.data
        except Exception as e:
            error = {'error': str(e)}
            return error