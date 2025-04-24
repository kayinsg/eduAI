import unittest
import sqlite3
from colour_runner.runner import ColourTextTestRunner
from database import UserDatabase
from _prompts import prompt, finalExpectedPrompt

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
        db = userDb.getDbConnection()
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

    def testShouldProvideAPersonalizedPromptWithUserData(self):
        # GIVEN the following preconditions corresponding to the system under test:
        baseTextPrompt = prompt
        userData = getUserData()
        # WHEN the following module is executed:
        finalPrompt = Prompt(userData).personalize(baseTextPrompt)
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(finalPrompt, finalExpectedPrompt)


if __name__ == '__main__':
    unittest.main(testRunner=ColourTextTestRunner())
