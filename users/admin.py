from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import LearningProgram,Course,UserProfile,UserCourseRanking, LearningProgramCourse,UserRecommendation,Feedback

admin.site.register(LearningProgram)
admin.site.register(Course)
admin.site.register(UserProfile)
admin.site.register(UserCourseRanking)
admin.site.register(LearningProgramCourse)
admin.site.register(UserRecommendation)
admin.site.register(Feedback)