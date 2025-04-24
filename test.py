import unittest
import sqlite3
from colour_runner.runner import ColourTextTestRunner
from database import UserDatabase
from _prompts import prompt, finalExpectedPrompt

def getLoginUserData():
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
    def getUserLoginData():
        userData = [
            ['FirstName', 'Jane'],
            ['LastName', 'Doe'],
            ['DateOfBirth', '03-22-1995'],
            ['GradeLevel', 9],
            ['TypeOfLearner', 'Textual'],
            ['StrongPersonalInterest', 'Painting']
        ]
        return userData

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
        userLoginData = self.getUserLoginData()
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
        userLoginData = self.getUserLoginData()
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


if __name__ == '__main__':
    unittest.main(testRunner=ColourTextTestRunner())
