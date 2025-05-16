import unittest
import sqlite3
from colour_runner.runner import ColourTextTestRunner
from UserDatabase import UserDatabase
from PromptPersonalizer import Prompt

def getUserData():
    userData = [
        ['FirstName', 'Jane'],
        ['LastName', 'Doe'],
        ['DateOfBirth', '03-22-1995'],
        ['GradeLevel', 9],
        ['TypeOfLearner', 'Textual'],
        ['StrongPersonalInterest', 'Painting']
    ]
    return userData

class DatabaseTests(unittest.TestCase):

    @staticmethod
    def getFakeDatabase():
        return sqlite3.connect(':memory:')

    @staticmethod
    def getDatabaseHeaders(db, table):
        cursor = db.cursor()
        cursor.execute(f"PRAGMA table_info({table})")
        return [col[1] for col in cursor.fetchall()]

    @staticmethod
    def getDatabaseUserRecord(userDb, expectedRecord):
        """Test helper method to fetch the first user record"""
        db = userDb.db
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Users")
        record = cursor.fetchone()
        return list(record) if record else None

    def testShouldCreateHeaderRowsForUser(self):
        # GIVEN
        userLoginData = getUserData()
        fakeDatabase = self.getFakeDatabase()
        expectedDatabaseFieldNames = [
            'FirstName',
            'LastName',
            'DateOfBirth',
            'GradeLevel',
            'TypeOfLearner',
            'StrongPersonalInterest',
        ]
        database = UserDatabase(fakeDatabase)
        # WHEN
        database.createTableFieldNames(userLoginData)
        # THEN
        databaseFields = self.getDatabaseHeaders(fakeDatabase, 'Users')
        self.assertEqual(databaseFields, expectedDatabaseFieldNames)

    def testShouldUploadUserInformationToDatabase(self):
        # GIVEN
        userLoginData = getUserData()
        expectedUserRecord = [
            'Jane',
            'Doe',
            '03-22-1995',
            9,
            'Textual',
            'Painting',
        ]
        fakeDatabase = self.getFakeDatabase()
        database = UserDatabase(fakeDatabase)
        # WHEN
        database.upload(userLoginData)
        # THEN
        databaseUserRecord = self.getDatabaseUserRecord(database, expectedUserRecord)
        self.assertEqual(databaseUserRecord, expectedUserRecord)


class PromptsTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def testShouldSuccesfullyProduceFinalPrompt(self):
        # GIVEN the following preconditions corresponding to the system under test:
        def getUserData():
            userData = [
                ['FirstName', 'Richard'],
                ['LastName', 'Johanssen'],
                ['DateOfBirth', '03-22-2008'],
                ['GradeLevel', 12],
                ['TypeOfLearner', 'Visual'],
                ['StrongPersonalInterest', 'Public Speaking']
            ]
            return userData

        userData = getUserData()
        specificQuestion = "Why is the sky blue?"
        basePrompt = """Ensure your answers meet these criteria:
1. Easy to understand for the average person:
    1.1 Use clear, simple language.
    1.2 Avoid technical jargon or complex terminology.
    1.3 Do not omit important details, even if they seem difficult. True understanding comes from full explanations.

    2. Break down complex ideas into basic components:
    2.1 Present information in small, digestible chunks.
    2.2 Use concrete examples to explain abstract ideas.

    3. Present information in a logical, flowing manner:
    3.1 Use transition words (e.g., "next," "however," "therefore") to connect ideas.
    3.2 Make sure each paragraph leads smoothly to the next.
    3.3 Keep a clear, consistent narrative throughout.
    3.4 Always use active voice (e.g., "You can do this" instead of "This can be done").

    4. Use paragraph format unless specified otherwise:
    4.1 Split long explanations into multiple short paragraphs.
    4.2 Keep paragraphs short (3-5 sentences) for easy reading.
    4.3 If lists are needed, embed them naturally in paragraphs.

---
"""
        expectedFinalPrompt = """Ensure your answers meet these criteria:
1. Easy to understand for the average person:
    1.1 Use clear, simple language.
    1.2 Avoid technical jargon or complex terminology.
    1.3 Do not omit important details, even if they seem difficult. True understanding comes from full explanations.

    2. Break down complex ideas into basic components:
    2.1 Present information in small, digestible chunks.
    2.2 Use concrete examples to explain abstract ideas.

    3. Present information in a logical, flowing manner:
    3.1 Use transition words (e.g., "next," "however," "therefore") to connect ideas.
    3.2 Make sure each paragraph leads smoothly to the next.
    3.3 Keep a clear, consistent narrative throughout.
    3.4 Always use active voice (e.g., "You can do this" instead of "This can be done").

    4. Use paragraph format unless specified otherwise:
    4.1 Split long explanations into multiple short paragraphs.
    4.2 Keep paragraphs short (3-5 sentences) for easy reading.
    4.3 If lists are needed, embed them naturally in paragraphs.

"Why is the sky blue?"

---

User Profile:
- Age: 17
- Grade Level: 12
- Learning Preference: Visual
- Key Interest: Public Speaking

---

Clarification Request:
I feel the above requires more background knowledge than I currently have.
Please explain it in more detail, using expressive and clear language, while tailoring examples to the above user's profile interests and learning style."""
        # WHEN the following module is executed:
        finalPrompt = Prompt(specificQuestion).personalize(basePrompt, userData)
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(finalPrompt, expectedFinalPrompt)


if __name__ == '__main__':
    unittest.main(testRunner=ColourTextTestRunner(verbosity=2))
