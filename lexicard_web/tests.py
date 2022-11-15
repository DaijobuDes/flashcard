from django.test import TestCase
from lexicard_web.models import User, Document, Deck, Flashcard, QA
from django.db import transaction

# Create your tests here.
class UserTestCase(TestCase):
    """
    Test cases for the user model
    """

    def setUp(self):
        User.objects.create(
            username="test",
            email="test@test.com",
            password="12345"
        )
        User.objects.create(
            username="test2",
            email="test2@test.com",
            password="12345"
        )
        User.objects.create(
            username="test3",
            email="test3@test.com",
            password="testr"
        )

    def test_fetch_user(self):
        user1 = User.objects.get(username="test")
        user2 = User.objects.get(username="test2")
        user3 = User.objects.get(username="test3")
        self.assertEqual(user1.username, "test")
        self.assertEqual(user2.password, "12345")
        self.assertEqual(user3.email, "test3@test.com")

class FlashcardTestCase(TestCase):

    def setUp(self):
        User.objects.create(
            username="test",
            email="test@test.com",
            password="12345"
        )
        user1 = User.objects.get(username="test")
        document1 = Document.objects.create(
            user_id = user1,
            document_name = "test document",
            document_format = "DOC"
        )
        deck1 = Deck.objects.create(
            user_id = user1,
            document_id = document1,
            deck_name = "test deck"
        )
        flashcard1 = Flashcard.objects.create(
            user_id = user1,
            deck_id = deck1
        )

        self.user1 = user1

        questions_array = [
            "distinct",
            "rare"
        ]
        answers_array = [
            "Readily distinguishable from all others",
            "Infrequently occurring"
        ]

        with transaction.atomic():
            for x, y in zip(questions_array, answers_array):
                data = QA.objects.create(
                    flashcard_question = x,
                    flashcard_answer = y,
                    flashcard_id = flashcard1,
                )
                print(x)
                data.save()

    def test_arrays(self):
        str1 = "Readily distinguishable from all others"
        str2 = "Infrequently occurring"
        str3 = "distinct"
        str4 = "rare"

        data_q1 = QA.objects.get(QA_id=1)
        data_q2 = QA.objects.get(QA_id=2)

        self.assertEqual(str3, data_q1.flashcard_question)
        self.assertEqual(str4, data_q2.flashcard_question)

        self.assertEqual(str1, data_q1.flashcard_answer)
        self.assertEqual(str2, data_q2.flashcard_answer)

    def test_flashcard(self):
        str1 = "distinct"
        str2 = "rare"
        str3 = "Readily distinguishable from all others"
        str4 = "Infrequently occurring"

        edit1 = "common"
        edit2 = "Belonging equally to or shared equally by two or more"

        # document = Document.objects.filter(
        #     document_name = "Lorem ipsum",
        #     document_format = "DOC",
        #     user_id_id = self.user1
        # ).first()
        # deck = Deck.objects.filter(
        #     user_id_id = self.user1,
        #     document_id_id = document.document_id
        # )

        flashcard = Flashcard.objects.get(deck_id=1)

        qa1 = QA.objects.filter(
            flashcard_id_id=flashcard.flashcard_id,
            QA_id=1
        ).first()

        self.assertEqual(str1, qa1.flashcard_question)
        self.assertEqual(str3, qa1.flashcard_answer)

        qa2 = QA.objects.filter(
            flashcard_id_id=flashcard.flashcard_id,
            QA_id=1
        ).update(
            flashcard_question=edit1,
            flashcard_answer=edit2
        )

        self.assertNotEqual(qa1, qa2)