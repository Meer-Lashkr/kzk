from django.test import TestCase
from django.contrib.auth import get_user_model
from forum.models import Question, Answer, QuestionTag

User = get_user_model()

class ForumTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='asker',
            password='password123',
            email='asker@example.com'
        )
        self.user2 = User.objects.create_user(
            username='answerer',
            password='password123',
            email='answerer@example.com'
        )
        self.tag = QuestionTag.objects.create(name='Grammar')
        self.question = Question.objects.create(
            title='How does pluralization work?',
            body='Can someone explain the suffix?',
            author=self.user,
            status='active'
        )
        self.question.tags.add(self.tag)

    def test_question_creation(self):
        self.assertEqual(self.question.title, 'How does pluralization work?')
        self.assertEqual(self.question.author, self.user)
        self.assertEqual(self.question.tags.count(), 1)
        self.assertEqual(self.question.status, 'active')

    def test_answer_creation(self):
        answer = Answer.objects.create(
            question=self.question,
            body='You add -ekan',
            author=self.user2,
            is_accepted=False
        )
        self.assertEqual(answer.question, self.question)
        self.assertEqual(answer.author, self.user2)
        self.assertFalse(answer.is_accepted)

    def test_accept_answer(self):
        answer1 = Answer.objects.create(question=self.question, body='Ans 1', author=self.user2)
        answer2 = Answer.objects.create(question=self.question, body='Ans 2', author=self.user)
        
        # Accept answer 1
        answer1.is_accepted = True
        answer1.save(update_fields=['is_accepted'])
        
        self.assertTrue(answer1.is_accepted)
