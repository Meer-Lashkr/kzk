from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Question, Answer, QuestionTag
from .forms import QuestionForm, AnswerForm
from accounts.models import ActivityLog


def question_list(request):
    query = request.GET.get('q', '')
    tag_slug = request.GET.get('tag', '')
    questions = Question.objects.exclude(status='deleted_soft').select_related('author').prefetch_related('tags').order_by('-created_at')

    if query:
        questions = questions.filter(
            Q(title__icontains=query) | Q(body__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()

    if tag_slug:
        questions = questions.filter(tags__slug=tag_slug)

    paginator = Paginator(questions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tags = QuestionTag.objects.all().order_by('name')

    return render(request, 'forum/question_list.html', {
        'page_obj': page_obj,
        'questions': page_obj,
        'query': query,
        'tags': tags,
        'active_tag': tag_slug,
    })


def question_detail(request, pk):
    question = get_object_or_404(Question.objects.select_related('author').prefetch_related('tags'), pk=pk)
    answers = question.answers.select_related('author').all().order_by('-is_accepted', 'created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            ActivityLog.objects.create(
                user=request.user,
                action_type='answer_created',
                target_type='Answer',
                target_id=answer.pk
            )
            messages.success(request, "Your answer has been posted.")
            return redirect('question_detail', pk=question.pk)
    else:
        form = AnswerForm()

    return render(request, 'forum/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form,
    })


@login_required
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            form.save_m2m()
            ActivityLog.objects.create(
                user=request.user,
                action_type='question_created',
                target_type='Question',
                target_id=question.pk
            )
            messages.success(request, "Your question has been posted!")
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'forum/question_create.html', {'form': form})


@login_required
def question_edit(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.author != request.user and not request.user.is_moderator:
        messages.error(request, "You do not have permission to edit this question.")
        return redirect('question_detail', pk=pk)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question updated.")
            return redirect('question_detail', pk=pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'forum/question_edit.html', {'form': form, 'question': question})


@login_required
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.author != request.user and not request.user.is_moderator:
        messages.error(request, "You do not have permission to delete this question.")
        return redirect('question_detail', pk=pk)

    if request.method == 'POST':
        question.status = 'deleted_soft'
        question.save()
        messages.success(request, "Question deleted.")
        return redirect('question_list')
    return render(request, 'forum/question_confirm_delete.html', {'question': question})


@login_required
def answer_edit(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if answer.author != request.user and not request.user.is_moderator:
        messages.error(request, "You do not have permission to edit this answer.")
        return redirect('question_detail', pk=answer.question.pk)

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            messages.success(request, "Answer updated.")
            return redirect('question_detail', pk=answer.question.pk)
    else:
        form = AnswerForm(instance=answer)
    return render(request, 'forum/answer_edit.html', {'form': form, 'answer': answer})


@login_required
def answer_delete(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    question_pk = answer.question.pk
    if answer.author != request.user and not request.user.is_moderator:
        messages.error(request, "You do not have permission to delete this answer.")
        return redirect('question_detail', pk=question_pk)

    if request.method == 'POST':
        answer.delete()
        messages.success(request, "Answer deleted.")
        return redirect('question_detail', pk=question_pk)
    return render(request, 'forum/answer_confirm_delete.html', {'answer': answer})


@login_required
def accept_answer(request, question_pk, answer_pk):
    question = get_object_or_404(Question, pk=question_pk)
    if question.author != request.user:
        messages.error(request, "Only the question author can accept an answer.")
        return redirect('question_detail', pk=question_pk)

    if request.method == 'POST':
        # Unaccept any previously accepted answer
        question.answers.update(is_accepted=False)
        answer = get_object_or_404(Answer, pk=answer_pk, question=question)
        answer.is_accepted = True
        answer.save()
        messages.success(request, "Answer marked as accepted.")
    return redirect('question_detail', pk=question_pk)
