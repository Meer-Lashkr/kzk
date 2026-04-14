from django.shortcuts import render
from accounts.models import User
from forum.models import Question
from datasets.models import CorrectionSubmission, ParallelTextSubmission, SentenceJudgmentSubmission

def home_view(request):
    total_users = User.objects.count()
    total_questions = Question.objects.count()
    
    total_contributions = (
        CorrectionSubmission.objects.count() +
        ParallelTextSubmission.objects.count() +
        SentenceJudgmentSubmission.objects.count()
    )
    
    context = {
        'total_users': total_users,
        'total_questions': total_questions,
        'total_contributions': total_contributions,
    }
    return render(request, 'home.html', context)
