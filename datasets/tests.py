from django.test import TestCase
from django.contrib.auth import get_user_model
from datasets.models import CorrectionSubmission, ParallelTextSubmission, SentenceJudgmentSubmission

User = get_user_model()

class DatasetsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='contributor',
            password='password123',
            email='contributor@example.com'
        )

    def test_correction_submission(self):
        c = CorrectionSubmission.objects.create(
            incorrect_text='Me is learning',
            corrected_text='I am learning',
            language_variant='sorani',
            topic='Grammar',
            submitted_by=self.user
        )
        self.assertEqual(c.incorrect_text, 'Me is learning')
        self.assertEqual(c.record_status, 'active')

    def test_parallel_text_submission(self):
        p = ParallelTextSubmission.objects.create(
            source_text='Silaw',
            target_text='Hello',
            source_language='Kurmanji',
            target_language='English',
            topic='Greetings',
            submitted_by=self.user
        )
        self.assertEqual(p.source_text, 'Silaw')
        self.assertEqual(p.record_status, 'active')

    def test_sentence_judgment_submission(self):
        j = SentenceJudgmentSubmission.objects.create(
            sentence_text='This is a valid sentence',
            binary_label='correct',
            language_variant='sorani',
            topic='General',
            submitted_by=self.user
        )
        self.assertEqual(j.binary_label, 'correct')
        self.assertEqual(j.record_status, 'active')
