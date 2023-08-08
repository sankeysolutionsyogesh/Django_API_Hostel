import json
from django.http import JsonResponse, HttpResponse
from .models import Student
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
import re
import datetime


@csrf_exempt
# Main Route
def student_api(request):
    if request.method == 'GET':
        # Check if the request is for 'getall' or 'getbyid'
        data = request.GET

        if 'id' in data or 'name' in data or 'roomno' in data or 'is_paid' in data:
            return get_student_byValue(request)
        else:
            return student_list(request)

    elif request.method == 'POST':
        return create_student(request)

    elif request.method == 'PUT':
        return update_student(request)

    elif request.method == 'DELETE':
        return delete_student(request)

    else:
        return HttpResponse('Method not allowed', status=405)

# Get all api


def student_list(request):
    data = json.loads(request.body)
    # print("paginat",data)
    pageno = data.get('page_no', 1)
    page_size = data.get('page_size', 10)

    student_list = []

    start = (pageno - 1) * page_size
    end = start + page_size

    total_items = Student.objects.count()

    total_pages = (total_items + page_size - 1) // page_size
    has_next = pageno < total_pages
    has_previous = pageno > 1

    students = Student.objects.all()[start:end]
    students_list_of_dicts = list(students.values())

    result = [{
        "page_no": pageno,
        "page_size": page_size,
        "total_pages": total_pages,
        "total_size": total_items,
        "has_next": has_next,
        "has_previous": has_previous,
        "data": students_list_of_dicts,
    }]

    if len(students_list_of_dicts) == 0:
        result[0]["message"] = "No records found"
    else:
        result[0]["message"] = "Success"

    return JsonResponse(result, safe=False)

# Get data by value


def get_student_byValue(request):
    data_id = request.GET.get('id')
    data_name = request.GET.get('name')
    data_roomno = request.GET.get('roomno')
    data_is_paid = request.GET.get('is_paid')
    try:
        student = {}
        if data_id is not None:
            student = Student.objects.filter(student_id=data_id)
            pass

        if data_name is not None:
            student = Student.objects.filter(student_name=data_name)
            pass

        if data_roomno is not None:
            student = Student.objects.filter(room_number=data_roomno)
            pass

        if data_is_paid is not None:
            student = Student.objects.filter(is_paid=data_is_paid)
            pass
        student_list = []
        if len(student) > 0:
            for stud in student:
                student_info = {
                    'student_id': stud.student_id,
                    'student_name': stud.student_name,
                    'gender': stud.gender,
                    'date_of_birth': stud.date_of_birth,
                    'room_number': stud.room_number,
                    'guardian_contact': stud.guardian_contact,
                    'is_paid': stud.is_paid,
                    'fees_paid': stud.fees_paid,
                    'roll_no': stud.roll_no
                }

                student_list.append(student_info)
            return JsonResponse({"total_size": len(student), "data": student_list, "message": "Successfully retrive data"})

        return JsonResponse({"total_size": len(student), "data": [], "message": "No records found"})
    except Student.DoesNotExist:
        return JsonResponse({'message': 'Student not found'}, status=404)

# Create new student


@csrf_exempt
def create_student(request):
    GENDER_CHOICES = ('M', 'F', 'O')
    data = json.loads(request.body)

    errors = {}
    try:

        if 'student_name' not in data:
            errors['student_name'] = "student_name key-value is reuired"
        elif not data['student_name'].replace(' ', '').isalpha():
            errors['student_name'] = "Student name must contain only alphabetic characters and spaces."

        if 'gender' not in data or data['gender'] not in GENDER_CHOICES:
            errors['gender'] = "Invalid gender choice."

        if 'date_of_birth' in data:
            try:
                datetime.datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
            except ValueError:
                errors['date_of_birth'] = "Invalid date format. Use 'YYYY-MM-DD'."

        if 'room_number' not in data or len(str(data['room_number'])) > 6:
            errors['room_number'] = "Room number cannot be more than 6 characters."

        if 'guardian_contact' not in data or not str(data['guardian_contact']).isdigit() or len(str(data['guardian_contact'])) != 10:
            errors['guardian_contact'] = "Guardian contact should be 10-digit number."

        if not isinstance(data['fees_paid'], int):
            errors['fees_paid'] = "Fee paid should be an integer."

        if 'is_paid' not in data or not isinstance(data['is_paid'], bool):
            errors['is_paid'] = "is_paid should be a boolean value."

        if 'is_paid' not in data or str(data['is_paid']).lower() not in ['true', 'false']:
            errors['is_paid'] = "Invalid value for is_paid. Use 'true' or 'false'."

        if not isinstance(data['roll_no'], int):
            errors['roll_no'] = "Roll number should be an integer."
        elif len(str(data['roll_no'])) > 5:
            errors['roll_no'] = "Roll number should be lesser than 5-digit integer."
        else:
            student_roll_no = data['roll_no']
            student = Student.objects.filter(roll_no=student_roll_no)
            student_count = student.count()
            if student_count > 0:
                errors['roll_no'] = "Student Roll No is already taken"

        required_fields = [
            'student_name', 'gender', 'date_of_birth', 'room_number',
            'guardian_contact', 'fees_paid', 'is_paid', 'roll_no'
        ]

        for field in required_fields:
            if not data.get(field):
                errors[field] = f"{field} is required."

        student_name = data['student_name']
        gender = data['gender']
        date_of_birth = data['date_of_birth']
        room_number = data['room_number']
        guardian_contact = data['guardian_contact']
        fees_paid = data['fees_paid']
        is_paid = data['is_paid']
        roll_no = data['roll_no']

        student = Student(
            student_name=student_name,
            gender=gender,
            date_of_birth=date_of_birth,
            room_number=room_number,
            guardian_contact=guardian_contact,
            fees_paid=fees_paid,
            is_paid=is_paid,
            roll_no=roll_no
        )
    except Exception as e:
        errors['database_error'] = str(e)

    if errors:
        return JsonResponse({'errors': errors}, status=400)
    else:
        student.save()
        return JsonResponse({'Message': "Successfully created a new student account"}, status=201)


# Update exisitng student data
@csrf_exempt
def update_student(request):
    GENDER_CHOICES = ('M', 'F', 'O')
    data = json.loads(request.body)
    student_id = data.get('student_id')

    errors = {}
    try:
        if 'student_name' not in data:
            errors['student_name'] = "student_name key-value is reuired"
        elif not data['student_name'].replace(' ', '').isalpha():
            errors['student_name'] = "Student name must contain only alphabetic characters and spaces."

        if 'gender' not in data or data['gender'] not in GENDER_CHOICES:
            errors['gender'] = "Invalid gender choice."

        if 'date_of_birth' in data:
            try:
                datetime.datetime.strptime(data['date_of_birth'], '%Y-%m-%d')
            except ValueError:
                errors['date_of_birth'] = "Invalid date format. Use 'YYYY-MM-DD'."

        if 'room_number' not in data or len(str(data['room_number'])) > 6:
            errors['room_number'] = "Room number cannot be more than 6 characters."

        if 'guardian_contact' not in data or not str(data['guardian_contact']).isdigit() or len(str(data['guardian_contact'])) != 10:
            errors['guardian_contact'] = "Guardian contact should be 10-digit number."

        if not isinstance(data['fees_paid'], float):
            errors['fees_paid'] = "Fee paid should be an float value."

        if 'is_paid' not in data or not isinstance(data['is_paid'], bool):
            errors['is_paid'] = "is_paid should be a boolean value."

        if 'is_paid' not in data or str(data['is_paid']).lower() not in ['true', 'false']:
            errors['is_paid'] = "Invalid value for is_paid. Use 'true' or 'false'."

        if not isinstance(data['roll_no'], int):
            errors['roll_no'] = "Roll number should be an integer."
        elif len(str(data['roll_no'])) > 5:
            errors['roll_no'] = "Roll number should lesser than 5-digit integer."
       

        required_fields = [
            'student_name', 'gender', 'date_of_birth', 'room_number',
            'guardian_contact', 'fees_paid', 'is_paid', 'roll_no'
        ]

        for field in required_fields:
            if not data.get(field):
                errors[field] = f"{field} is required."

        student = Student.objects.get(pk=student_id)

        student_data = {
            'student_name': data.get('student_name', student.student_name),
            'gender': data.get('gender', student.gender),
            'date_of_birth': data.get('date_of_birth', student.date_of_birth),
            'room_number': data.get('room_number', student.room_number),
            'guardian_contact': data.get('guardian_contact', student.guardian_contact),
            'fees_paid': data.get('fees_paid', student.fees_paid),
            'is_paid': data.get('is_paid', student.is_paid),
            'roll_no': data.get('roll_no', student.is_paid),
        }

        
    except Student.DoesNotExist:
        errors['database_error'] = 'Student not found'

    if errors:
        return JsonResponse({'errors': errors}, status=400)
    else:
        Student.objects.filter(pk=student_id).update(**student_data)
        return JsonResponse({'message': 'Student updated successfully'}, status=201)


    

@csrf_exempt
def delete_student(request):

    data = json.loads(request.body)
    student_id = data.get('id')
    try:
        student = Student.objects.get(pk=student_id)
        student.delete()
        return JsonResponse({'message': 'Student deleted successfully of ID '+str(student_id)}, status=201)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
