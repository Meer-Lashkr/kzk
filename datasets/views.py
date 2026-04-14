from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CorrectionSubmission, ParallelTextSubmission, SentenceJudgmentSubmission
from .forms import CorrectThisForm, ParallelTextForm, IsThisCorrectForm
from accounts.models import ActivityLog


def contribute_home(request):
    return render(request, 'contribution/home.html')


@login_required
def correct_this_submit(request):
    if request.method == 'POST':
        form = CorrectThisForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.submitted_by = request.user
            submission.save()
            ActivityLog.objects.create(
                user=request.user,
                action_type='correction_submitted',
                target_type='CorrectionSubmission',
                target_id=submission.pk
            )
            messages.success(request, "Thank you! Your correction has been submitted.")
            return redirect('contribute_home')
    else:
        form = CorrectThisForm()
    return render(request, 'contribution/correct_this.html', {'form': form})


@login_required
def parallel_text_submit(request):
    if request.method == 'POST':
        form = ParallelTextForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.submitted_by = request.user
            submission.save()
            ActivityLog.objects.create(
                user=request.user,
                action_type='parallel_text_submitted',
                target_type='ParallelTextSubmission',
                target_id=submission.pk
            )
            messages.success(request, "Thank you! Your parallel text has been submitted.")
            return redirect('contribute_home')
    else:
        form = ParallelTextForm()
    return render(request, 'contribution/parallel_text.html', {'form': form})


@login_required
def is_this_correct_submit(request):
    if request.method == 'POST':
        form = IsThisCorrectForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.submitted_by = request.user
            submission.save()
            ActivityLog.objects.create(
                user=request.user,
                action_type='judgment_submitted',
                target_type='SentenceJudgmentSubmission',
                target_id=submission.pk
            )
            messages.success(request, "Thank you! Your judgment has been submitted.")
            return redirect('contribute_home')
    else:
        form = IsThisCorrectForm()
    return render(request, 'contribution/is_this_correct.html', {'form': form})


@login_required
def my_submissions(request):
    filter_type = request.GET.get('type', 'all')
    user = request.user

    corrections = CorrectionSubmission.objects.filter(submitted_by=user).order_by('-created_at')
    parallel_texts = ParallelTextSubmission.objects.filter(submitted_by=user).order_by('-created_at')
    judgments = SentenceJudgmentSubmission.objects.filter(submitted_by=user).order_by('-created_at')

    context = {
        'corrections': corrections,
        'parallel_texts': parallel_texts,
        'judgments': judgments,
        'filter_type': filter_type,
        'total': corrections.count() + parallel_texts.count() + judgments.count(),
    }
    return render(request, 'contribution/my_submissions.html', context)
