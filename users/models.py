from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging
logger = logging.getLogger(__name__)

class LearningProgramCourse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class LearningProgram(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    learning_program = models.ForeignKey(LearningProgram, on_delete=models.SET_NULL, null=True)
    preference_text = models.TextField(null=True, blank=True, help_text="I'm a [year of study] year student interested in [major or areas of interest]. I prefer [specific subjects, skills, or topics] over [other subjects or topics]. My best time for learning is [preferred learning time, e.g., morning, afternoon, evening] because that's when I feel most [describe how you feel, e.g., focused, energetic]. For me, it's more important to be really [interested/focus solely on grades], and I [prefer working on projects/prefer taking exams] as a way to assess my understanding. I'm looking for courses that [describe what you want from your courses, e.g., challenge me, expand my knowledge, offer practical experience, include engaging projects, or prepare me for exams] as I plan out the rest of my academic journey.")

    def __str__(self):
        return self.user.username

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         UserProfile.objects.get_or_create(user=instance)
    #         if not created:
    #             logger.info(f"UserProfile already exists for user {instance.username}")
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.userprofile.save()

class Course(models.Model):
    TIME_CHOICES = (
        ('M', 'Morning'),
        ('N', 'Noon'),
        ('E', 'Evening'),
    )
    course_name = models.CharField(max_length=200)
    course_id = models.CharField(max_length=50, unique=True)
    # learning_program = models.ForeignKey(LearningProgramCourse, on_delete=models.CASCADE)
    course_informetion = models.TextField()
    # is_test= models.BooleanField(default=False)
    is_manadatory_ds= models.BooleanField(default=False)
    is_manadatory_ie= models.BooleanField(default=False)
    is_manadatory_se= models.BooleanField(default=False)
    lecture_hours = models.CharField(max_length=1, choices=TIME_CHOICES, default='M')
    syllabus = models.TextField()



    class Meta:
        ordering = ['course_name']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.course_name

class UserCourseRanking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    RANKING_CHOICES = (
        (0, '0 - Have not taken yet'),
        (1, '1 - Do not like at all'),
        (2, '2 - Do not like'),
        (3, '3 - Neutral'),
        (4, '4 - Like'),
        (5, '5 - Like a lot'),
    )
    ranking = models.IntegerField(choices=RANKING_CHOICES, default=0)  # 0 if not done yet, 1-5 for rankings

    class Meta:
        unique_together = (('user', 'course'),)
        ordering = ['user', '-ranking']

    def __str__(self):
        return f'{self.user.user.username} - {self.course.course_name}: {self.ranking}'

class UserRecommendation(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    recommended_course = models.OneToOneField(Course, null=True, on_delete=models.CASCADE)
    predicted_rank = models.FloatField(default=0.0)
    explanation = models.TextField(default='No explanation available')


    def __str__(self):
        return self.user.user.username


from django.db import models
from django.contrib.auth.models import User

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback by {self.user.username} on {self.created_at}'
