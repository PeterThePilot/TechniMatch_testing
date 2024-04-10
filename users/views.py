import random
import numpy as np
import os
from django.contrib.auth import logout
from django.shortcuts import redirect
from tqdm import tqdm
from .models import UserProfile, Course, UserCourseRanking, UserRecommendation, LearningProgram, Feedback
from django.contrib.auth.models import User
from .env import GOOGLE_API_KEY

# if "GOOGLE_API_KEY" not in os.environ:
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


from dotenv import load_dotenv, dotenv_values

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator

load_dotenv()
def custom_logout(request):
    logout(request)
    return redirect('home')


from django.db import transaction
def register(request):
    # try:
    #     profile = request.user.userprofile
    # except UserProfile.DoesNotExist:
    #     profile = UserProfile(user=request.user)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Adjust the redirect to your login page's name
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})

def some_error_view(request):
    return render(request, 'users/some_error.html')


def submit_course_rankings(request):
    if request.method == 'POST':
        user_profile = UserProfile.objects.get(user=request.user)
        # Assuming your POST data contains 'ranking_<course_id>' as keys
        for key, value in request.POST.items():
            if key.startswith('ranking_'):
                course_id = key.split('_')[1]
                course = Course.objects.get(id=course_id)
                UserCourseRanking.objects.update_or_create(
                    user=user_profile,
                    course=course,
                    defaults={'ranking': value}
                )
        return redirect('system')
    else:
        user_profile = UserProfile.objects.get(user=request.user)
        learning_program = str(user_profile.learning_program)
        if learning_program=="Data Science and Engineering":
            mandatory_courses = Course.objects.filter( is_manadatory_ds=True)
            other_courses = Course.objects.filter( is_manadatory_ds=False)
        elif learning_program=="Industrial Engineering and Management":
            mandatory_courses = Course.objects.filter( is_manadatory_ie=True)
            other_courses = Course.objects.filter( is_manadatory_ie=False)
        else:
            #learning_program=="Informetion System Engineering":
            mandatory_courses = Course.objects.filter( is_manadatory_se=True)
            other_courses = Course.objects.filter( is_manadatory_se=False)

        return render(request, 'users/courses_rank.html', {
            'mandatory_courses': mandatory_courses,
            'other_courses': other_courses,
            'RANKING_CHOICES': UserCourseRanking.RANKING_CHOICES
        })


from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import UserProfile

def success(request):
    return render(request, 'users/success.html')


# def success(request):
#     return render(request, 'success.html')


def success2(request, username):
    return render(request, 'success.html', {'username': username})
    # context = {'username': username}
    # return render(request, 'users/success.html', context)

#
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # return redirect(request.GET.get('next', reverse('system')))
                return redirect('system')
            else:
                messages.error(request, 'Invalid login credentials.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

# def system_view(request):
#     context = {
#         'username': 'Guest' if not request.user.is_authenticated else request.user.username,
#         'has_ranked_courses': False,
#     }
#
#     user_profile = UserProfile.objects.get(user=request.user) if request.user.is_authenticated else None
#     if user_profile and UserCourseRanking.objects.filter(user=user_profile).exists():
#         context['has_ranked_courses'] = True
#
#     # Check for a 'get_recommendations' GET parameter
#     if 'get_recommendations' in request.GET:
#         context['recommendations'] = get_course_recommendations(request)
#
#     return render(request, 'users/system.html', context)
def system_view(request):
    context = {
        'username': 'Guest' if not request.user.is_authenticated else request.user.username,
        'has_ranked_courses': False,
        'recommendations': None,  # Set default value for recommendations
    }

    user_profile = UserProfile.objects.get(user=request.user) if request.user.is_authenticated else None
    if user_profile and UserCourseRanking.objects.filter(user=user_profile).exists():
        context['has_ranked_courses'] = True

    if request.method == 'POST' and 'get_recommendations' in request.POST:
        context['recommendations'] = get_course_recommendations(request)

    return render(request, 'users/system.html', context)


def min_max_normalize(scores: list[tuple[int, float]]) -> list[tuple[int, float]]:
    """
    Normalize the scores of recommended items to a 1-5 range.

    Args:
        scores (list[tuple[int, float]]): A list of tuples where each tuple is (item_index, score).

    Returns:
        list[tuple[int, float]]: A list of tuples where each tuple is (item_index, normalized_score).
    """
    if not scores:
        return scores

    # Extract just the scores from the list of tuples
    only_scores = [score for _, score in scores]

    min_score, max_score = min(only_scores), max(only_scores)
    if min_score == max_score:  # Avoid division by zero if all scores are the same
        return [(item_index, 3) for item_index, _ in scores]  # Return a neutral score if all scores are equal

    # Apply min-max normalization to each score
    normalized_scores = [
        (item_index, 1 + (score - min_score) * 4 / (max_score - min_score))
        for item_index, score in scores
    ]

    return normalized_scores


def cf_recomendations(user_index: int, matrix: np.ndarray, U: np.ndarray, V: np.ndarray) -> list[tuple[int, float]]:
    """
    Recommend items to the user based on collaborative filtering.

    Args:
        user_index (int): The index for the user we want the rankings for.
        matrix (np.ndarray): Rows are the users, columns are the items, and the values are the ranking of the items.
                             Missing values should be 0.
        U (np.ndarray): The users factorization of matrix.
        V (np.ndarray): The items factorization of matrix.

    Returns:
        list[tuple[int, float]]: List of tuples where each tuple is the index of the recommended item and the item rating,
                                 sorted in descending order.
    """
    recommendations = U[user_index] @ V.T
    sorted_recommendations = [
        (item_index, score) for item_index, score in enumerate(recommendations)
        if matrix[user_index, item_index] == 0  # Exclude already rated items
    ]

    # Normalize the recommendation scores
    normalized_recommendations = min_max_normalize(sorted_recommendations)

    # Sort the recommendations in descending order by the normalized score
    normalized_recommendations.sort(key=lambda x: x[1], reverse=True)

    return normalized_recommendations


#working fine till here
# def cf_recomendations(user_index:int,matrix:np.ndarray, U:np.ndarray, V:np.ndarray)->list[tuple[int, float]]:
#     """ recomend items to the user based on colaborative filtering
#
#     Args:
#         user_index (int): the index for the user we want the rankings
#         matrix (np.ndarray): rows are the users columns are the items and the values are the ranking of the items.
#         mising values should be 0.
#         U (np.ndarray): the users factorization of matrix
#         V (np.ndarray): the items factorization of matrix
#
#     Returns:
#         list[tuple[int, float]]: list of tupels where each tuple is the index of the recomended item and the item raitng.
#         sorted in desending order.
#     """
#     recomendations = U[user_index]@V.T
#     sorted_recomedations = []
#     for item_index, item in enumerate(recomendations):
#         if matrix[user_index, item_index] != 0:
#             continue
#         sorted_recomedations.append((item_index, item))
#     sorted_recomedations.sort(key=lambda x:x[1],reverse=True)
#     return sorted_recomedations


def get_course_recommendations1(request):
    random.seed(88)
    np.random.seed(88)
    def course_ranking_matrix_from_df(user_courses_rankings):
        course_ranking_matrix = np.zeros((len(user_id_to_idx), len(course_id_to_idx)))
        for row in user_courses_rankings:
            user_idx = user_id_to_idx[str(row.user)]
            course_idx = course_id_to_idx[row.course.course_id]
            course_ranking_matrix[user_idx, course_idx] = row.ranking
        return course_ranking_matrix

    courses_query_set = Course.objects.all()
    idx_to_course_id = {}
    course_id_to_idx = {}
    for idx, course in enumerate(courses_query_set):
        idx_to_course_id[idx] = course.course_id
        course_id_to_idx[course.course_id] = idx
    user_courses_rankings = UserCourseRanking.objects.all()
    users = User.objects.all()
    idx_to_user_id = {}
    user_id_to_idx = {}
    for idx, row in enumerate(users):
        idx_to_user_id[idx] = str(row)
        user_id_to_idx[str(row)] = idx
    print("user_id_to_idx")
    print(user_id_to_idx)
    print("course_id_to_idx")
    print(course_id_to_idx)
    print("idx_to_user_id")
    print(idx_to_user_id)
    print("idx_to_course_id")
    print(idx_to_course_id)

    course_ranking_matrix = course_ranking_matrix_from_df(user_courses_rankings)
    U, V = creating_MF(course_ranking_matrix)
    predicted = U @ V.T
    print("course_ranking_matrix")
    for i in course_ranking_matrix:
        print(i)
    print("predicted")
    # for i in predicted:
    #     print(i)
    if request.user.is_authenticated:
        curent_username = request.user.username
    print("curent_username", curent_username)

    print("user_id_to_idx[curent_username]", user_id_to_idx[curent_username])
    recomendations = cf_recomendations(user_id_to_idx[curent_username], course_ranking_matrix, U, V)
    print("recomendations", recomendations)

    top20 = [(str(Course.objects.get(course_id=int(idx_to_course_id[r[0]])).course_name),(str(Course.objects.get(course_id=int(idx_to_course_id[r[0]])).syllabus)),round(r[1],2)) for r in recomendations[:20]]
    return top20




def creating_MF(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """given a matrix find the factorization of the matrix

    Args:
        matrix (np.ndarray): rows are the users columns are the items and the values are the ranking of the items(1-5).
        mising values should be 0.

    Returns:
        tuple[np.ndarray, np.ndarray]: the users embedings (U) and the items embedings (V)
    """
    hidden_dim = 6
    epochs_num = 300
    learning_rate = 0.005
    users_dim, items_dim = matrix.shape
    users_embeding = np.random.normal(size=(users_dim, hidden_dim))
    items_embeding = np.random.normal(size=(items_dim, hidden_dim))

    # training

    for epoch in tqdm(range(epochs_num)):
        for user in range(users_dim):
            for item in range(items_dim):
                if matrix[user, item] == 0:  # missing the ratings
                    continue  # compute the loss only on observed entries
                err = matrix[user, item] - users_embeding[user] @ items_embeding[item]
                user_gradient = learning_rate * err * items_embeding[item]
                item_gradient = learning_rate * err * users_embeding[user]
                users_embeding[user] += user_gradient
                items_embeding[item] += item_gradient

    return users_embeding, items_embeding


def recomended_courses_silaby(recomend):
    results_dict = {'course_name': {},
                    'course_basic_information': {}}
    for i, (course_name, sylabus ,score) in enumerate(recomend):
        results_dict['course_name'][i] = course_name
        results_dict['course_basic_information'][i] = sylabus

    return results_dict

def get_course_recommendations2(silabuses,request):
    print("Google API Key:", os.environ.get("GOOGLE_API_KEY"))
    if request.user.is_authenticated:
        curent_user = request.user
    all_feedbacks = Feedback.objects.filter(user=curent_user)
    feedbacks = ""
    temp_feedbacks = ""
    if len(all_feedbacks)>0:
        for i in all_feedbacks:
            temp_feedbacks += " " + i.text
        feedbacks = f"user feedback: {temp_feedbacks}"
    print("############feedbacks\n", feedbacks)

    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    genaimodel = llm
    explain_rankings_parser = PydanticOutputParser(pydantic_object=explain_rankings_model)
    task = "You are a course recomender system"
    task2 = "You are given a university students preferences and \
            a list of recomended courses and their silabuses based on colaborative filtering \
            you need to rerank this list and provide explanations for your recomendations"
    task3 = "\n{format_instructions}\n"
    task4 = "{query}\n"
    explain_rankings_promt = PromptTemplate(
        template=task + task2 + task3 + task4,
        input_variables=["query"],
        partial_variables={"format_instructions": explain_rankings_parser.get_format_instructions()}
    )
    prompt_and_model = explain_rankings_promt | genaimodel
    student_preferences = UserProfile.objects.get(user=request.user).preference_text
    print("student_preferences", student_preferences)
    total = student_preferences + str(silabuses) + feedbacks
    counter = 0
    for i in range(5):
        try:
            output = prompt_and_model.invoke({"query": total})
            print("-------------------------------output-----------------------")
            print(output)
            results = explain_rankings_parser.invoke(output)

            break
        except Exception as e:
            counter += 1
            print(f"exception {counter}", e)
    if counter == 5:
        return -1 #{"course_id":-1,"reason": -1}
    return results

class explain_rankings_model(BaseModel):
    course_id: list = Field(description="the unique courses identifiers ranked from the best course to the worst")
    reason: list = Field(description="the reason ranked from the best course to the worst")




def get_course_recommendations(request):
    top20 = get_course_recommendations1(request)


    top5 = top20[:5]
    print("**********top20", top20)
    redult_dict = recomended_courses_silaby(top20)
    print("redult_dict", redult_dict)
    res=get_course_recommendations2(redult_dict,request)
    if res!= -1:
        new_ordering, reasons = res.course_id, res.reason
    else:
        response_data = {
            'similarity': [],
            'ranking': top5,
        }
        return response_data
    # results = [(top20[int(order)], reason) for order, reason in zip(new_ordering, reasons)]
    results = [(i,j) for i,j in zip(new_ordering, reasons)]
    print("!!!!!!!!!results", results)

    # Create a response object
    response_data = {
        'similarity': results,
        'ranking': top5,
    }
    return response_data


def profile(request):
    return render(request, 'users/profile.html')


def recommendations(request):
    return render(request, 'users/recommendation.html')

def rankings(request):
    return render(request, 'users/rankings.html')
def home(request):
    return render(request, 'users/home.html')
    # return HttpResponse("Welcome to TechniMatch!")



import csv
from django.http import HttpResponse
from .models import Course

def export_courses_to_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="courses_infi.csv"'

    writer = csv.writer(response)
    # Define the header row.
    writer.writerow(['Course Name', 'Course ID', 'Course Information', 'Mandatory DS',
                     'Mandatory IE', 'Mandatory SE', 'Lecture Hours', 'Syllabus'])

    # Write data rows
    for course in Course.objects.all():
        writer.writerow([
            course.course_name,
            course.course_id,
            course.course_informetion,
            course.is_manadatory_ds,
            course.is_manadatory_ie,
            course.is_manadatory_se,
            course.lecture_hours,
            course.syllabus,
        ])

    # Return the response to the user
    return response



from django.shortcuts import render, redirect
from .forms import FeedbackForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Your feedback has been submitted successfully!')
            return redirect('system')
    else:
        form = FeedbackForm()
    return render(request, 'users/feedback.html', {'form': form})
