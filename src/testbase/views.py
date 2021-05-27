import json
import random
import string

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import Choices, Questions, Answer, Form, Responses


@login_required
def index(request):
    forms = Form.objects.filter(creator=request.user)
    return render(request, "index/index.html", {
        "forms": forms
    })


@login_required
def create_form(request):
    if request.user.type != 'teacher':
        return HttpResponseRedirect(reverse("403"))
    # Create a blank form API
    if request.method == "POST":
        data = json.loads(request.body)
        title = data["title"]
        code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(30))
        choices = Choices(choice="Option 1")
        choices.save()
        question = Questions(question_type="multiple choice", question="Untitled Question", required=False)
        question.save()
        question.choices.add(choices)
        question.save()
        form = Form(code=code, title=title, creator=request.user)
        form.save()
        form.questions.add(question)
        form.save()
        return JsonResponse({"message": "Sucess", "code": code})


@login_required
def edit_form(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    return render(request, "index/form.html", {
        "code": code,
        "form": form_info
    })


@login_required
def edit_title(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        if len(data["title"]) > 0:
            form_info.title = data["title"]
            form_info.save()
        else:
            form_info.title = form_info.title[0]
            form_info.save()
        return JsonResponse({"message": "Success", "title": form_info.title})


@login_required
def edit_description(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        form_info.description = data["description"]
        form_info.save()
        return JsonResponse({"message": "Success", "description": form_info.description})


@login_required
def edit_bg_color(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        form_info.background_color = data["bgColor"]
        form_info.save()
        return JsonResponse({"message": "Success", "bgColor": form_info.background_color})


@login_required
def edit_text_color(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        form_info.text_color = data["textColor"]
        form_info.save()
        return JsonResponse({"message": "Success", "textColor": form_info.text_color})


@login_required
def edit_setting(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        form_info.collect_email = data["collect_email"]
        form_info.is_quiz = data["is_quiz"]
        form_info.authenticated_responder = data["authenticated_responder"]
        form_info.confirmation_message = data["confirmation_message"]
        form_info.edit_after_submit = data["edit_after_submit"]
        form_info.allow_view_score = data["allow_view_score"]
        form_info.save()
        return JsonResponse({'message': "Success"})


@login_required
def delete_form(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse("404"))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "DELETE":
        # Delete all questions and choices
        for i in form_info.questions.all():
            for j in i.choices.all():
                j.delete()
            i.delete()
        for i in Responses.objects.filter(response_to=form_info):
            for j in i.response.all():
                j.delete()
            i.delete()
        form_info.delete()
        return JsonResponse({'message': "Success"})


@login_required
def edit_question(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        question_id = data["id"]
        question = Questions.objects.filter(id=question_id)
        if question.count() == 0:
            return HttpResponseRedirect(reverse("404"))
        else:
            question = question[0]
        question.question = data["question"]
        question.question_type = data["question_type"]
        question.required = data["required"]
        if data.get("score"):
            question.score = data["score"]
        if data.get("answer_key"):
            question.answer_key = data["answer_key"]
        question.save()
        return JsonResponse({'message': "Success"})


@login_required
def edit_choice(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        choice_id = data["id"]
        choice = Choices.objects.filter(id=choice_id)
        if choice.count() == 0:
            return HttpResponseRedirect(reverse("404"))
        else:
            choice = choice[0]
        choice.choice = data["choice"]
        if data.get('is_answer'):
            choice.is_answer = data["is_answer"]
        choice.save()
        return JsonResponse({'message': "Success"})


@login_required
def add_choice(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        choice = Choices(choice="Option")
        choice.save()
        form_info.questions.get(pk=data["question"]).choices.add(choice)
        form_info.save()
        return JsonResponse({"message": "Success", "choice": choice.choice, "id": choice.id})


@login_required
def remove_choice(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        data = json.loads(request.body)
        choice = Choices.objects.filter(pk=data["id"])
        if choice.count() == 0:
            return HttpResponseRedirect(reverse("404"))
        else:
            choice = choice[0]
        choice.delete()
        return JsonResponse({"message": "Success"})


@login_required
def get_choice(request, code, question):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "GET":
        question = Questions.objects.filter(id=question)
        if question.count() == 0:
            return HttpResponseRedirect(reverse('404'))
        else:
            question = question[0]
        choices = question.choices.all()
        choices = [{"choice": i.choice, "is_answer": i.is_answer, "id": i.id} for i in choices]
        return JsonResponse({"choices": choices, "question": question.question, "question_type": question.question_type,
                             "question_id": question.id})


@login_required
def add_question(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "POST":
        choices = Choices(choice="Option 1")
        choices.save()
        question = Questions(question_type="multiple choice", question="Untitled Question", required=False)
        question.save()
        question.choices.add(choices)
        question.save()
        form_info.questions.add(question)
        form_info.save()
        return JsonResponse({'question': {'question': "Untitled Question", "question_type": "multiple choice",
                                          "required": False, "id": question.id},
                             "choices": {"choice": "Option 1", "is_answer": False, 'id': choices.id}})


@login_required
def delete_question(request, code, question):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "DELETE":
        question = Questions.objects.filter(id=question)
        if question.count() == 0:
            return HttpResponseRedirect(reverse("404"))
        else:
            question = question[0]
        for i in question.choices.all():
            i.delete()
            question.delete()
        return JsonResponse({"message": "Success"})


@login_required
def score(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if not form_info.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args=[code]))
    else:
        return render(request, "index/score.html", {
            "form": form_info
        })


@login_required
def edit_score(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if not form_info.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args=[code]))
    else:
        if request.method == "POST":
            data = json.loads(request.body)
            question_id = data["question_id"]
            question = form_info.questions.filter(id=question_id)
            if question.count() == 0:
                return HttpResponseRedirect(reverse("edit_form", args=[code]))
            else:
                question = question[0]
            score = data["score"]
            if score == "":
                score = 0
            question.score = score
            question.save()
            return JsonResponse({"message": "Success"})


@login_required
def answer_key(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if not form_info.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args=[code]))
    else:
        if request.method == "POST":
            data = json.loads(request.body)
            question = Questions.objects.filter(id=data["question_id"])
            if question.count() == 0:
                return HttpResponseRedirect(reverse("edit_form", args=[code]))
            else:
                question = question[0]
            if question.question_type == "short" or question.question_type == "paragraph":
                question.answer_key = data["answer_key"]
                question.save()
            else:
                for i in question.choices.all():
                    i.is_answer = False
                    i.save()
                if question.question_type == "multiple choice":
                    choice = question.choices.get(pk=data["answer_key"])
                    choice.is_answer = True
                    choice.save()
                else:
                    for i in data["answer_key"]:
                        choice = question.choices.get(id=i)
                        choice.is_answer = True
                        choice.save()
                question.save()
            return JsonResponse({'message': "Success"})


@login_required
def feedback(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if not form_info.is_quiz:
        return HttpResponseRedirect(reverse("edit_form", args=[code]))
    else:
        if request.method == "POST":
            data = json.loads(request.body)
            question = form_info.questions.get(id=data["question_id"])
            question.feedback = data["feedback"]
            question.save()
            return JsonResponse({'message': "Success"})


def view_form(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    if form_info.authenticated_responder:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("account_login"))
    return render(request, "index/view_form.html", {
        "form": form_info
    })


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def submit_form(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    if form_info.authenticated_responder:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("account_login"))
    if request.method == "POST":
        code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(20))
        if form_info.authenticated_responder:
            response = Responses(response_code=code, response_to=form_info, responder_ip=get_client_ip(request),
                                 responder=request.user)
            response.save()
        else:
            if not form_info.collect_email:
                response = Responses(response_code=code, response_to=form_info, responder_ip=get_client_ip(request))
                response.save()
            else:
                response = Responses(response_code=code, response_to=form_info, responder_ip=get_client_ip(request),
                                     responder_email=request.POST["email-address"])
                response.save()

        for i in request.POST:
            # Excluding csrf token
            if i == "csrfmiddlewaretoken" or i == "email-address":
                continue
            question = form_info.questions.get(id=i)
            for j in request.POST.getlist(i):
                answer = Answer(answer=j, answer_to=question)
                answer.save()
                response.response.add(answer)
                response.save()
        return render(request, "index/form_response.html", {
            "form": form_info,
            "code": code
        })


@login_required
def responses(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    return render(request, "index/responses.html", {
        "form": form_info,
        "responses": Responses.objects.filter(response_to=form_info)
    })


def response(request, code, response_code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if not form_info.allow_view_score:
        if form_info.creator != request.user:
            return HttpResponseRedirect(reverse("403"))
    total_score = 0
    score = 0
    response_info = Responses.objects.filter(response_code=response_code)
    if response_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        response_info = response_info[0]
    if form_info.is_quiz:
        for i in form_info.questions.all():
            total_score += i.score
        for i in response_info.response.all():
            if i.answer_to.question_type == "short" or i.answer_to.question_type == "paragraph":
                if i.answer == i.answer_to.answer_key: score += i.answer_to.score
            elif i.answer_to.question_type == "multiple choice":
                answer_key = None
                for j in i.answer_to.choices.all():
                    if j.is_answer:
                        answer_key = j.id
                if answer_key is not None and int(answer_key) == int(i.answer):
                    score += i.answer_to.score
        _temp = []
        for i in response_info.response.all():
            if i.answer_to.question_type == "checkbox" and i.answer_to.pk not in _temp:
                answers = []
                answer_keys = []
                for j in response_info.response.filter(answer_to__pk=i.answer_to.pk):
                    answers.append(int(j.answer))
                    for k in j.answer_to.choices.all():
                        if k.is_answer and k.pk not in answer_keys: answer_keys.append(k.pk)
                    _temp.append(i.answer_to.pk)
                if answers == answer_keys: score += i.answer_to.score
    return render(request, "index/response.html", {
        "form": form_info,
        "response": response_info,
        "score": score,
        "total_score": total_score
    })


def edit_response(request, code, response_code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    response = Responses.objects.filter(response_code=response_code, response_to=form_info)
    if response.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        response = response[0]
    if form_info.authenticated_responder:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("account_login"))
        if response.responder != request.user:
            return HttpResponseRedirect(reverse('403'))
    if request.method == "POST":
        if form_info.authenticated_responder and not response.responder:
            response.responder = request.user
            response.save()
        if form_info.collect_email:
            response.responder_email = request.POST["email-address"]
            response.save()
        # Deleting all existing answers
        for i in response.response.all():
            i.delete()
        for i in request.POST:
            # Excluding csrf token and email address
            if i == "csrfmiddlewaretoken" or i == "email-address":
                continue
            question = form_info.questions.get(id=i)
            for j in request.POST.getlist(i):
                answer = Answer(answer=j, answer_to=question)
                answer.save()
                response.response.add(answer)
                response.save()
        if form_info.is_quiz:
            return HttpResponseRedirect(reverse("response", args=[form_info.code, response.response_code]))
        else:
            return render(request, "index/form_response.html", {
                "form": form_info,
                "code": response.response_code
            })
    return render(request, "index/edit_response.html", {
        "form": form_info,
        "response": response
    })


@login_required
def contact_form_template(request):
    # Create a blank form API
    if request.method == "POST":
        code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(30))
        name = Questions(question_type="short", question="Name", required=True)
        name.save()
        email = Questions(question_type="short", question="Email", required=True)
        email.save()
        address = Questions(question_type="paragraph", question="Address", required=True)
        address.save()
        phone = Questions(question_type="short", question="Phone number", required=False)
        phone.save()
        comments = Questions(question_type="paragraph", question="Comments", required=False)
        comments.save()
        form = Form(code=code, title="Contact information", creator=request.user, background_color="#e2eee0",
                    allow_view_score=False, edit_after_submit=True)
        form.save()
        form.questions.add(name)
        form.questions.add(email)
        form.questions.add(address)
        form.questions.add(phone)
        form.questions.add(comments)
        form.save()
        return JsonResponse({"message": "Sucess", "code": code})


@login_required
def customer_feedback_template(request):
    # Create a blank form API
    if request.method == "POST":
        code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(30))
        comment = Choices(choice="Comments")
        comment.save()
        question = Choices(choice="Questions")
        question.save()
        bug = Choices(choice="Bug Reports")
        bug.save()
        feature = Choices(choice="Feature Request")
        feature.save()
        feedback_type = Questions(question="Feedback Type", question_type="multiple choice", required=False)
        feedback_type.save()
        feedback_type.choices.add(comment)
        feedback_type.choices.add(bug)
        feedback_type.choices.add(question)
        feedback_type.choices.add(feature)
        feedback_type.save()
        feedback = Questions(question="Feedback", question_type="paragraph", required=True)
        feedback.save()
        suggestion = Questions(question="Suggestions for improvement", question_type="paragraph", required=False)
        suggestion.save()
        name = Questions(question="Name", question_type="short", required=False)
        name.save()
        email = Questions(question="Email", question_type="short", required=False)
        email.save()
        form = Form(code=code, title="Customer Feedback", creator=request.user, background_color="#e2eee0",
                    confirmation_message="Thanks so much for giving us feedback!",
                    description="We would love to hear your thoughts or feedback on how we can improve your experience!",
                    allow_view_score=False, edit_after_submit=True)
        form.save()
        form.questions.add(feedback_type)
        form.questions.add(feedback)
        form.questions.add(suggestion)
        form.questions.add(name)
        form.questions.add(email)
        return JsonResponse({"message": "Sucess", "code": code})


@login_required
def event_registration_template(request):
    # Create a blank form API
    if request.method == "POST":
        code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(30))
        name = Questions(question="Name", question_type="short", required=False)
        name.save()
        email = Questions(question="email", question_type="short", required=True)
        email.save()
        organization = Questions(question="Organization", question_type="short", required=True)
        organization.save()
        day1 = Choices(choice="Day 1")
        day1.save()
        day2 = Choices(choice="Day 2")
        day2.save()
        day3 = Choices(choice="Day 3")
        day3.save()
        day = Questions(question="What days will you attend?", question_type="checkbox", required=True)
        day.save()
        day.choices.add(day1)
        day.choices.add(day2)
        day.choices.add(day3)
        day.save()
        dietary_none = Choices(choice="None")
        dietary_none.save()
        dietary_vegetarian = Choices(choice="Vegetarian")
        dietary_vegetarian.save()
        dietary_kosher = Choices(choice="Kosher")
        dietary_kosher.save()
        dietary_gluten = Choices(choice="Gluten-free")
        dietary_gluten.save()
        dietary = Questions(question="Dietary restrictions", question_type="multiple choice", required=True)
        dietary.save()
        dietary.choices.add(dietary_none)
        dietary.choices.add(dietary_vegetarian)
        dietary.choices.add(dietary_gluten)
        dietary.choices.add(dietary_kosher)
        dietary.save()
        accept_agreement = Choices(choice="Yes")
        accept_agreement.save()
        agreement = Questions(question="I understand that I will have to pay $$ upon arrival", question_type="checkbox",
                              required=True)
        agreement.save()
        agreement.choices.add(accept_agreement)
        agreement.save()
        form = Form(code=code, title="Event Registration", creator=request.user, background_color="#fdefc3",
                    confirmation_message="We have received your registration.\n\
Insert other information here.\n\
\n\
Save the link below, which can be used to edit your registration up until the registration closing date.",
                    description="Event Timing: January 4th-6th, 2016\n\
Event Address: 123 Your Street Your City, ST 12345\n\
Contact us at (123) 456-7890 or no_reply@example.com", edit_after_submit=True, allow_view_score=False)
        form.save()
        form.questions.add(name)
        form.questions.add(email)
        form.questions.add(organization)
        form.questions.add(day)
        form.questions.add(dietary)
        form.questions.add(agreement)
        form.save()
        return JsonResponse({"message": "Sucess", "code": code})


@login_required
def delete_responses(request, code):
    form_info = Form.objects.filter(code=code)
    # Checking if form exists
    if form_info.count() == 0:
        return HttpResponseRedirect(reverse('404'))
    else:
        form_info = form_info[0]
    # Checking if form creator is user
    if form_info.creator != request.user:
        return HttpResponseRedirect(reverse("403"))
    if request.method == "DELETE":
        responses = Responses.objects.filter(response_to=form_info)
        for response in responses:
            for i in response.response.all():
                i.delete()
            response.delete()
        return JsonResponse({"message": "Success"})


# Error handler
def four_zero_three(request):
    return render(request, "error/403.html")


def four_zero_four(request):
    return render(request, "error/404.html")
