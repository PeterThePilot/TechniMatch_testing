import pandas as pd

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
course_categories = {'mathematics': [94594,
  96262,
  94345,
  94481,
  97950,
  95140,
  97317,
  94139,
  94142,
  95296,
  96327,
  96200,
  94411,
  94412,
  96351,
  96226,
  97510,
  94312,
  94313,
  94314,
  104042,
  94700,
  104044,
  97139,
  96122,
  94333,
  94591],
 'programming_and_cs': [97280,
  97920,
  234114,
  94210,
  97921,
  97922,
  97414,
  96265,
  94219,
  94224,
  96411,
  96412,
  94241,
  96250,
  96291,
  95140,
  97447,
  95280,
  96311,
  94395,
  97215,
  95296,
  96578,
  97222,
  96327,
  97225,
  96208,
  96336,
  96210,
  96211,
  96212,
  96215,
  94170,
  97244,
  96222,
  96351,
  96224,
  97246,
  96226,
  96231,
  94312,
  94313,
  94314,
  96235,
  94700,
  234221,
  94704,
  95219,
  97139,
  96244,
  94202,
  94333],
 'statistics_and_probability': [97280,
  97414,
  96262,
  97800,
  94224,
  94481,
  96275,
  96411,
  96414,
  95140,
  96425,
  97449,
  96693,
  97209,
  96570,
  94139,
  96576,
  96450,
  96578,
  96200,
  97225,
  94411,
  94412,
  96336,
  96212,
  94423,
  94424,
  94170,
  96475,
  96222,
  97246,
  94564,
  95334,
  96617,
  94314,
  94700,
  96620,
  97135,
  95605,
  96120,
  96122],
 'machine_learning': [97921,
  97922,
  95622,
  96275,
  96411,
  96292,
  95280,
  96311,
  97209,
  97215,
  97222,
  97225,
  94288,
  96336,
  96212,
  94295,
  94170,
  96222,
  97247,
  97248,
  96622,
  97135,
  97400],
 'data_science': [94210,
  97414,
  94219,
  94224,
  96275,
  97950,
  94241,
  95140,
  94139,
  97215,
  95296,
  96327,
  96200,
  94295,
  94424,
  94170,
  97246,
  96222,
  97248,
  96226,
  94700,
  97135,
  94202],
 'classical_ai_and_robots': [96235, 96208, 96210, 97622, 97244],
 'optimization': [96224,
  97280,
  96226,
  95140,
  96327,
  96200,
  97225,
  96235,
  96336,
  96311,
  96122],
 'game_theory': [96576,
  97921,
  96226,
  97317,
  96690,
  96211,
  96570,
  97980,
  97950]}

import random
from django.contrib.auth.models import User
from users.models import UserProfile, LearningProgram, Course, UserCourseRanking

# First, define the preference text and course categories
preferences = {
    'mathematics': "I really enjoy mathematics and problem solving.",
    'programming_and_cs': "I am passionate about programming and computer science.",
    'statistics_and_probability': "Statistics and probability fascinate me.",
    'machine_learning': "Machine learning is my area of interest.",
    'data_science': "Data science models and data visualization are what I like to study.",
    'classical_ai_and_robots': "Classical artificial intelligence and robots are my main focus.",
    'optimization': "Optimization problems are what I like to solve.",
    'game_theory': "Game theory is incredibly intriguing to me.",
}

# Learning programs to choose from
learning_programs = list(LearningProgram.objects.all())


# This function creates a user profile
def create_user_profile(username, preference_category, learning_program):
    user = User.objects.create(username=username)
    user_password = "31102002m"  # You should generate or obtain a password securely
    user.set_password(user_password)
    user.save()

    profile = UserProfile.objects.create(
        user=user,
        preference_text=preferences[preference_category],
        learning_program=random.choice(learning_programs)
    )
    return profile

# This function creates course rankings for a given user profile
def create_course_rankings(user_profile, category):
    high_rank_courses = course_categories[category]
    all_courses = list(Course.objects.all())
    for course in all_courses:
        # print(high_rank_courses)
        # print(int(course.course_id))
        rank = random.choice([4, 5]) if int(course.course_id) in high_rank_courses else random.choice([1, 2, 3])
        UserCourseRanking.objects.create(
            user=user_profile,
            course=course,
            ranking=rank
        )

# Create 10 user profiles and rankings for each category
for category in preferences.keys():
    for i in range(10):
        username = f'user_simple_a_{category}_{i}'
        user_profile = create_user_profile(username, category, random.choice(learning_programs))
        create_course_rankings(user_profile, category)

print("Users and their course rankings created successfully!")
