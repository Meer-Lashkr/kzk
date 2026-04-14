from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from forum.models import Question, Answer, QuestionTag
from datasets.models import CorrectionSubmission, ParallelTextSubmission, SentenceJudgmentSubmission

User = get_user_model()


class Command(BaseCommand):
    help = "Seed demo data: admin, moderator, 5 users, forum Q&As, all 3 contribution types"

    def handle(self, *args, **options):
        self.stdout.write("🌱 Seeding database...")

        # --- Create admin ---
        admin, created = User.objects.get_or_create(username='admin', defaults={
            'email': 'admin@kzk.platform',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
            'first_name': 'Admin',
            'bio': 'Platform administrator.',
        })
        if created:
            admin.set_password('admin1234')
            admin.save()
            self.stdout.write("  ✅ Admin user created (username: admin, password: admin1234)")
        else:
            self.stdout.write("  ⏭  Admin user already exists")

        # --- Create moderator ---
        mod, created = User.objects.get_or_create(username='moderator', defaults={
            'email': 'mod@kzk.platform',
            'role': 'moderator',
            'first_name': 'Mêdyator',
            'bio': 'Keeping the platform clean and constructive.',
        })
        if created:
            mod.set_password('mod12345')
            mod.save()
            self.stdout.write("  ✅ Moderator created (username: moderator, password: mod12345)")
        else:
            self.stdout.write("  ⏭  Moderator already exists")

        # --- Create 5 users ---
        demo_users_data = [
            {'username': 'sara_k', 'email': 'sara@kzk.platform', 'first_name': 'Sara', 'bio': 'Kurdish linguist and learner.'},
            {'username': 'diyar', 'email': 'diyar@kzk.platform', 'first_name': 'Diyar', 'bio': 'Software developer building Kurdish NLP.'},
            {'username': 'hawkar', 'email': 'hawkar@kzk.platform', 'first_name': 'Hawkar', 'bio': 'Language teacher.'},
            {'username': 'nadia_m', 'email': 'nadia@kzk.platform', 'first_name': 'Nadia', 'bio': 'Translator (Kurdish–English).'},
            {'username': 'karo', 'email': 'karo@kzk.platform', 'first_name': 'Karo', 'bio': 'Researcher, Kurdish dialects.'},
        ]
        users = []
        for data in demo_users_data:
            u, created = User.objects.get_or_create(username=data['username'], defaults={**data, 'role': 'normal_user'})
            if created:
                u.set_password('demo1234')
                u.save()
            users.append(u)
        self.stdout.write(f"  ✅ 5 demo users ready (password: demo1234)")

        # --- Create tags ---
        tag_names = ['Grammar', 'Sorani', 'Kurmanji', 'Spelling', 'Dialect', 'Vocabulary', 'Translation']
        tags = {}
        for name in tag_names:
            tag, _ = QuestionTag.objects.get_or_create(name=name)
            tags[name] = tag

        # --- Forum questions ---
        q1, _ = Question.objects.get_or_create(
            title="What is the correct spelling of 'school' in Sorani Kurdish?",
            defaults={'body': "I've seen it written as مەکتەب and قوتابخانە in different sources. Which is correct or more common in modern Sorani?", 'author': users[0], 'status': 'active'}
        )
        q1.tags.add(tags['Sorani'], tags['Spelling'])

        q2, _ = Question.objects.get_or_create(
            title="How do plural forms work in Sorani Kurdish?",
            defaults={'body': "I'm learning Sorani and struggling with plural formation. Are there regular rules, or is it irregular like in English?", 'author': users[1], 'status': 'active'}
        )
        q2.tags.add(tags['Grammar'], tags['Sorani'])

        q3, _ = Question.objects.get_or_create(
            title="What are the major differences between Kurmanji and Sorani dialects?",
            defaults={'body': "I speak some Sorani but want to understand Kurmanji too. What are the biggest grammatical and vocabulary differences?", 'author': users[2], 'status': 'active'}
        )
        q3.tags.add(tags['Dialect'], tags['Kurmanji'], tags['Sorani'])

        q4, _ = Question.objects.get_or_create(
            title="How do I say 'I am happy' in different Kurdish dialects?",
            defaults={'body': "Looking to compare how emotion expressions differ across Sorani, Kurmanji, and Hawrami.", 'author': users[3], 'status': 'active'}
        )
        q4.tags.add(tags['Vocabulary'], tags['Dialect'])

        # --- Answers ---
        if not q1.answers.exists():
            Answer.objects.create(question=q1, body="قوتابخانە is the more native Kurdish word and is preferred in modern Sorani usage. مەکتەب is borrowed from Arabic.", author=mod)
            Answer.objects.create(question=q1, body="Both are used, but قوتابخانە is more commonly found in formal writing and education contexts.", author=users[4])

        if not q2.answers.exists():
            Answer.objects.create(question=q2, body="Sorani plural is generally formed by adding -ەکان for definite plural and -ان for indefinite. For example: کتێب (book) → کتێبەکان (the books).", author=admin, is_accepted=True)

        if not q3.answers.exists():
            Answer.objects.create(question=q3, body="Key differences: Kurmanji uses Latin/Cyrillic scripts, Sorani uses Arabic script. Kurmanji has grammatical gender (masculine/feminine), Sorani does not. Verb conjugation patterns also differ significantly.", author=users[0])

        self.stdout.write("  ✅ Forum questions and answers seeded")

        # --- Correction submissions ---
        corrections = [
            ('من کتێبەکە خوێند', 'من کتێبەکەم خوێند', 'sorani', 'Grammar'),
            ('ئەو رۆژانە باشن', 'ئەو رۆژانە باشن', 'sorani', 'Daily Speech'),
            ('Ez dibixwim kitêb', 'Ez kitêb dixwînim', 'kurmanji', 'Grammar'),
        ]
        for inc, corr, lv, topic in corrections:
            CorrectionSubmission.objects.get_or_create(
                incorrect_text=inc,
                defaults={'corrected_text': corr, 'language_variant': lv, 'topic': topic, 'submitted_by': users[1]}
            )
        self.stdout.write(f"  ✅ {len(corrections)} correction submissions seeded")

        # --- Parallel text submissions ---
        parallel = [
            ('ئەمڕۆ هەوای باشە', 'The weather is nice today', 'Sorani Kurdish', 'English', 'Daily Life'),
            ('من مامۆستام', 'I am a teacher', 'Sorani Kurdish', 'English', 'Introduction'),
            ('Roj baş', 'Good morning', 'Kurmanji Kurdish', 'English', 'Greetings'),
            ('کتێبەکە لە سەر مێزەکەدایە', 'The book is on the table', 'Sorani Kurdish', 'English', 'Vocabulary'),
        ]
        for src, tgt, sl, tl, topic in parallel:
            ParallelTextSubmission.objects.get_or_create(
                source_text=src,
                defaults={'target_text': tgt, 'source_language': sl, 'target_language': tl, 'topic': topic, 'submitted_by': users[2]}
            )
        self.stdout.write(f"  ✅ {len(parallel)} parallel text submissions seeded")

        # --- Sentence judgment submissions ---
        judgments = [
            ('من بە خانووەکانە دەچم', 'incorrect', 'sorani', 'Grammar'),
            ('ئەو کتێبێکی باشی نووسی', 'correct', 'sorani', 'Literature'),
            ('Ez diçim malê', 'correct', 'kurmanji', 'Daily Life'),
            ('ئەمە زمانی کوردییە', 'correct', 'sorani', 'Identity'),
        ]
        for sent, label, lv, topic in judgments:
            SentenceJudgmentSubmission.objects.get_or_create(
                sentence_text=sent,
                defaults={'binary_label': label, 'language_variant': lv, 'topic': topic, 'submitted_by': users[3]}
            )
        self.stdout.write(f"  ✅ {len(judgments)} sentence judgment submissions seeded")

        self.stdout.write(self.style.SUCCESS("\n✨ Database seeded successfully!"))
        self.stdout.write("\nDemo Credentials:")
        self.stdout.write("  Admin:     admin / admin1234")
        self.stdout.write("  Moderator: moderator / mod12345")
        self.stdout.write("  Users:     sara_k, diyar, hawkar, nadia_m, karo / demo1234")
