import pandas as pd
from .models import Course
import os
import django

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
# django.setup()

# Load your DataFrame (this should be where your DataFrame is stored)
# df = pd.read_csv('transfored_courses_data.csv')
df = pd.read_csv("C:\\Users\\micha\\Desktop\\Technimatch\\myproject\\users\\transfored_courses_data.csv")
# Iterate through each row of the DataFrame and create Course instances
for index, row in df.iterrows():
    # c= Course.objects.create(
    #     course_name=row['course_name'],
    #     course_id=row['course_id'],
    #     course_informetion=row['course_basic_information'] if pd.notnull(row['course_basic_information']) else 'No information available',
    #     is_manadatory_ds=row['is_manadatory_ds'],
    #     is_manadatory_ie=row['is_manadatory_ie'],
    #     is_manadatory_se=row['is_manadatory_se'],
    #     lecture_hours=row['time_category'],  # Assuming this matches 'M', 'N', or 'E'
    #     syllabus=row['semesterial_data']  # Or wherever the syllabus information is stored
    # )
    # c.save()

    course, created = Course.objects.get_or_create(
        course_id=row['course_id'],
        defaults={
            'course_name': row['course_name'],
            'course_informetion': row['semesterial_data'] if pd.notnull(
                row['course_basic_information']) else 'No information available',
            'is_manadatory_ds': row['is_manadatory_ds'],
            'is_manadatory_ie': row['is_manadatory_ie'],
            'is_manadatory_se': row['is_manadatory_se'],
            'lecture_hours': row['time_category'],  # Assumes this matches 'M', 'N', or 'E'
            'syllabus': row['course_basic_information']  # Or wherever the syllabus information is stored
        }
    )
    if created:
        print(f'Created new course: {course.course_name}')
    else:
        print(f'Course already exists: {course.course_name}')