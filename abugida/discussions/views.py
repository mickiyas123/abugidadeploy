from unicodedata import name
from django.shortcuts import render, redirect
from .models import Questions, Room ,Topic, Answers
from .forms import RoomForm ,QuestionForm ,AnswerForm, QuestionRoomForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.


def home(request):
    return render(request, 'discussions/home.html')

def about(request):
    return render(request, 'discussions/about.html')

def course(request):
    return render(request, 'discussions/course.html')




def discussions(request):
    """ A method that shows the discutions page """
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    

    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    prof = request.user.profile 


    questions = Questions.objects.all()
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_discription = Room.description
    room_messages = Questions.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]
    context = {'prof': prof,'questions': questions, 'rooms': rooms, 'topics': topics,'room_count': room_count, 'room_messages': room_messages, 'room_discription': room_discription}
    return render(request, 'discussions/discussions.html', context)



def rooms(request):
    """ A method that shows list of rooms """
    prof = request.user.profile
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'discussions/rooms.html', context)


def room(request, pk):
    """ A method that shows a specific room"""
   # question = Questions.objects.all()

    room = Room.objects.get(id=pk)
    prof = request.user.profile
    questions = room.questions_set.all()
    answers = room.answers_set.all()
    question_form = QuestionRoomForm()
    answer_form = AnswerForm()
    context = {'room': room, 'questions': questions, 'answers': answers, 'question_form': question_form, 'answer_form': answer_form}
    return render(request, 'discussions/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    """ A method for creating new room """
    prof = request.user.profile
    profile = request.user.profile
    topics = Topic.objects.all()
    form = RoomForm()
    room = Room.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get("topic")
        
        if request.method == 'POST':
            topic_name = request.POST.get('topic')
            topic, created = Topic.objects.get_or_create(name=topic_name)

            new_room = Room.objects.create(
                host=profile,
                topic=topic,
                name = request.POST.get("name"),
                description = request.POST.get("description")
            )
            return redirect('rooms')
    context = {'prof':prof,'form': form, 'topics': topics, 'room':room}
    return render(request, 'discussions/room_form.html', context)




@login_required(login_url='login')
def createQuestion(request):
    """ A method for creating question """
    form = QuestionForm()
    prof = request.user.profile

    if request.method == 'POST':
        form = QuestionForm(request.POST)


        if form.is_valid():
            new_room=form.save(commit=False)
            new_room.user = request.user.profile
            new_room.save()
            

            return redirect('discussions')
        
    context = {'prof':prof,'form': form, 'rooms': rooms}
    return render(request, 'discussions/questions_form.html', context)

    



@login_required(login_url='login')
def createroomQuestion(request, pk):
    """ A method for creating question """
    qform = QuestionRoomForm()
    prof = request.user.profile
    room = Room.objects.get(id=pk)
    querier = request.user.profile
    body = request.POST.get("body")
    topic = room.topic

    if request.method == 'POST':
        Questions.objects.create(
            user = querier,
            room = room,
            body = body,
           topic = topic
        )
        return redirect('room', pk=room.id)




@login_required(login_url='login')
def updateRoom(request, pk):
    """ A method for updating a room """
    profile = request.user.profile
    prof = request.user.profile
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)

    if request.method == 'POST':
        topic_name = request.POST.get("topic")
        topic_names = []
        for topic in topics:
            topic_names.append(topic.name)
        
        if topic_name not in topic_names:
            topic = Topic.objects.create(
                    name=topic_name, creator=profile)
        else:
            topic = Topic.objects.get(name=topic_name)

        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        
        return redirect('discussion')
    context = {'form': form, 'room':room, 'topics': topics}
    return render(request, 'discussions/room_form.html', context)





@login_required(login_url='login')
def updateQuestion(request, pk):
    """ A method for updating specific question """
    question = Questions.objects.get(id=pk)
    room = question.room
    prof = request.user.profile
    room_id = room.id
    form = QuestionForm(instance=question)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():
            form.save()
            return redirect('room', pk=room_id)
    context = {'form': form}
    return render(request, 'discussions/question_form.html', context)


@login_required(login_url='login')
def createAnswer(request, pk):
    """ a method for creating an answer """
    user = request.user.profile
    question = Questions.objects.get(id=pk)
    body = request.POST.get("body")
    room = question.room
    room_id = room.id
    # topic = room.topic

    if request.method == 'POST':
        Answers.objects.create(
            user= user,
            question = question,
            room = room,
            body = body,
            # topic = topic
        )
        return redirect('room', pk=room_id)



@login_required(login_url='login')
def updateAnswer(request, pk):
    """ a method for updating specific question """
    answer = Answers.objects.get(id=pk)
    room = answer.room
    room_id = room.id
    form = AnswerForm(instance=answer)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)

        if form.is_valid():
            form.save()
            return redirect('room', pk=room_id)
    context = {'form': form}
    return render(request, 'discussions/answer_form.html', context)






@login_required(login_url='login')
def deleteRoom(request, pk):
    """ A method for deleteing a room """
    room = Room.objects.get(id=pk)
    # question = Question.objects.get(id=pk)
    # answer = Answer.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('discussion')
    return render(request, 'discussions/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteQuestion(request, pk):
    """ A method for deleting a question """
    question = Questions.objects.get(id=pk)
    room = question.room
    room_id = room.id
    # question = Question.objects.get(id=pk)
    # answer = Answer.objects.get(id=pk)

    if request.method == 'POST':
        question.delete()
        return redirect('room', pk=room_id)
    return render(request, 'discussions/delete.html', {'obj': question})


@login_required(login_url='login')
def deleteAnswer(request, pk):
    """ A method for deleting an answer """
    answer = Answers.objects.get(id=pk)
    # question = Question.objects.get(id=pk)
    # answer = Answer.objects.get(id=pk)

    if request.method == 'POST':
        answer.delete()
        return redirect('discussion')
    return render(request, 'discussions/delete.html', {'obj': answer})