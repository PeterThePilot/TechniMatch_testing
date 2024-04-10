from django import forms

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, LearningProgram, UserCourseRanking, Course

class UserRegistrationForm(UserCreationForm):
    # username = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # Set the initial value for the preference_text field
        self.fields[
            'preference_text'].initial = "Example text : I'm a [year of study] year student interested in [major or areas of interest]. I prefer [specific subjects, skills, or topics] over [other subjects or topics]. My best time for learning is [preferred learning time, e.g., morning, afternoon, evening] because that's when I feel most [describe how you feel, e.g., focused, energetic]. For me, it's more important to be really [interested/focus solely on grades], and I [prefer working on projects/prefer taking exams] as a way to assess my understanding. I'm looking for courses that [describe what you want from your courses, e.g., challenge me, expand my knowledge, offer practical experience, include engaging projects, or prepare me for exams] as I plan out the rest of my academic journey."

    email = forms.EmailField(required=True)
    learning_program = forms.ModelChoiceField(queryset=LearningProgram.objects.all(), empty_label="Select Program")
    preference_text = forms.CharField(widget=forms.Textarea, required=False)#help_text="I'm a [year of study] year student interested in [major or areas of interest]. I prefer [specific subjects, skills, or topics] over [other subjects or topics]. My best time for learning is [preferred learning time, e.g., morning, afternoon, evening] because that's when I feel most [describe how you feel, e.g., focused, energetic]. For me, it's more important to be really [interested/focus solely on grades], and I [prefer working on projects/prefer taking exams] as a way to assess my understanding. I'm looking for courses that [describe what you want from your courses, e.g., challenge me, expand my knowledge, offer practical experience, include engaging projects, or prepare me for exams] as I plan out the rest of my academic journey.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #         # Check if UserProfile exists and get or create accordingly
    #         profile, created = UserProfile.objects.get_or_create(user=user)
    #         profile.learning_program = self.cleaned_data['learning_program']
    #         profile.preference_text = self.cleaned_data['preference_text']
    #         profile.save()
    #     return user
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                learning_program=self.cleaned_data['learning_program'],
                preference_text=self.cleaned_data['preference_text'],
            )
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['learning_program', 'preference_text']

class UserCourseRankingForm(forms.ModelForm):
    class Meta:
        model = UserCourseRanking
        fields = ['course', 'ranking']

    def __init__(self, *args, **kwargs):
        super(UserCourseRankingForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text']


#
# class UserPreferenceForm(forms.ModelForm):
#     class Meta:
#         model = UserPreference
#         fields = ['name', 'year_of_study', 'degree', 'preferences']
#
#
# class UserRankingForm(forms.Form):
#     introduction_to_python = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Introduction to Python")
#     advanced_python = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Advanced Python")
#     data_structures = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Data Structures")
#     algorithms = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Algorithms")
#     web_development = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Web Development")
#     database_systems = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Database Systems")
#     operating_systems = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Operating Systems")
#     computer_networks = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Computer Networks")
#     machine_learning = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Machine Learning")
#     artificial_intelligence = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Artificial Intelligence")
#     software_engineering = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Software Engineering")
#     cybersecurity = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Cybersecurity")
#     Interaction = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Human-Computer Interaction")
#     cloud_development = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Cloud Development")
#     mobile_app_development = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Mobile App Development")
#     data_mining = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Data Mining")
#     natural_language_processing = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)],
#                                                     label="Natural Language Processing")
#     parrallel_computing = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Parrallel Computing")
#     blockchain_technology = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], label="Blockchain Technology")
#
#     def set_labels(self, courses):
#         for field, course in zip(self.fields.values(), courses):
#             field.label = course
#
#
#
# class UserLoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)