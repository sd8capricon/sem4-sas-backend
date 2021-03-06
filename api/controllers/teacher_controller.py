import hashlib
import os

from api.serializers import TeacherViewSerializer
from api.models import Teacher


# View all Teachers
def teachers_details(req):
    if req.method == 'GET':
        course_taught = []
        teachers = Teacher.objects.all()
        for teacher in teachers:
            try:
                temp = teacher.course.course_name
            except:
                temp = None
            course_taught.append(temp)
        serializer = TeacherViewSerializer(teachers, many=True)
        scpy = serializer.data
        for index, teacher in enumerate(scpy):
            teacher['course_taught'] = course_taught[index]
        sortedTeachers = sorted(scpy, key = lambda d:d['teacher_id'])
        return sortedTeachers

def teacher(req, teacher_id):
    if req.method == 'GET':
        try:
            teacher = Teacher.objects.get(pk=teacher_id)
            serializer = TeacherViewSerializer(teacher)
            scpy = serializer.data
            try:
                scpy['course_taught'] = teacher.course.course_name
            except:
                scpy['course_taught'] = None
            return scpy
        except Exception as e:
            error = {'error': str(e)}
            return error
    elif req.method == 'POST':
        try:
            data = req.data
            password = (os.environ.get('PASS_SALT') +
                        data['password']).encode('utf-8')
            h = hashlib.sha256(password).hexdigest()
            t = Teacher(username=data['username'], password=h,
                        f_name=data['f_name'], l_name=data['l_name'])
            if 'type' in data:
                t.type = data['type']
            t.save()
            serializer = TeacherViewSerializer(t)
            return serializer.data
        except Exception as e:
            error = {'error': str(e)}
            return error
    elif req.method == 'PATCH':
        try:
            data = req.data
            Teacher.objects.filter(teacher_id=teacher_id).update(username=data['username'], f_name=data['f_name'], l_name=data['l_name'])
            t = Teacher.objects.get(pk=teacher_id)
            if 'password' in data:
                password = (os.environ.get('PASS_SALT') +
                        data['password']).encode('utf-8')
                h = hashlib.sha256(password).hexdigest()
                t.password = h
                t.save()
            serializer = TeacherViewSerializer(t)
            return serializer.data
        except Exception as e:
            error = {'error': str(e)}
            return error
    elif req.method == 'DELETE':
        try:
            t = Teacher.objects.get(pk=teacher_id)
            t.delete()
            return {"message": "Teacher Removed"}
        except Exception as e:
            error = {'error': str(e)}
            return error
