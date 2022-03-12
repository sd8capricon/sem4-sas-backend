from django.db.models import Sum

from api.serializers import CourseSerializer, CourseViewSerializer, StatSerializer
from api.models import Course, Lec_Stat, Student, Teacher


# View all courses
def courses_detail(req):
    if req.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return serializer.data

# View a course or Create a Course
def course(req, course_id):
    if req.method == 'GET':
        try:
            course = Course.objects.get(pk=course_id)
            serialzer = CourseViewSerializer(course)
            course = serialzer.data
            for student in course['enrolled_students']:
                student.pop('total_attendance_percentage')
            return course
        except Exception as e:
            error = {'error': str(e)}
            return error
    elif req.method == 'POST':
        try:
            course_name = req.data['course_name']
            course = Course(course_name=course_name)
            course.save()
            # Check if teacher is assigned to course
            if 'taught_by' in req.data:
                taught_by_id = req.data['taught_by']
                taught_by = Teacher.objects.get(pk=taught_by_id)
                course.taught_by = taught_by
            # Check if enrolled students list is passed
            if 'enrolled_students' in req.data:
                enrolled_students = req.data['enrolled_students']
                for student in enrolled_students:
                    s = Student.objects.get(pk=student)
                    course.enrolled_students.add(s)
            course.save()
            serialzer = CourseViewSerializer(course)
            return serialzer.data
        except Exception as e:
            error = {'error': str(e)}
            return error
    elif req.method == 'PATCH':
        # To edit a existing course
        pass
    elif req.method == 'DELETE':
        try:
            course = Course.objects.get(pk=course_id)
            course.delete()
            return {"message": "Course Deleted"}
        except Exception as e:
            error = {'error': str(e)}
            return error

# Get avg Course Attendance Percentage and stats
def course_lec_stats(req, course_id):
    if req.method == 'GET':
        try:
            c = Course.objects.get(pk=course_id)
            lecs = Lec_Stat.objects.filter(course=c)
            lecCount = lecs.count()
            if lecCount!=0:
                atten_sum = Lec_Stat.objects.all().aggregate(sum=Sum('attendance_percentage'))
                avg_percentage_attendace = atten_sum['sum']/lecCount
                statSerializer = StatSerializer(lecs, many=True)
                statcpy = statSerializer.data
                for stat in statcpy:
                    stat.pop('course')
                res = {
                    'course_stats': statcpy,
                    'avg_course_attendance': avg_percentage_attendace
                }
                return res
            else:
                return {'error': 'No lectures found'}
        except Exception as e:
            error = {'error': str(e)}
            return error