import pendulum


class Prompt:
    def __init__(self, specificQuestion):
        self.specificQuestion = specificQuestion

    def personalize(self, basePrompt, userData):
        self.validateQuestion()
        userProfile = self.createPromptUserProfile(userData)
        return self.personalizePrompt(basePrompt, userProfile)

    def validateQuestion(self):
        QuestionChecker(self.specificQuestion).validateQuestion()

    def createPromptUserProfile(self, userData):
        UserDataValidator(userData).validate()
        return PromptUserProfile(userData).createUserProfile()

    def personalizePrompt(self, basePrompt, userProfile):
        promptBuilder = PromptBuilder(basePrompt, self.specificQuestion)
        return PromptPersonalizer(basePrompt, promptBuilder).personalize(userProfile)


class QuestionChecker:
    def __init__(self, question):
        self.question = question

    def validateQuestion(self):
        self.checkIfQuestionHasQuestionMark()
        self.checkIfQuestionContainsAQuestionWord()

    def checkIfQuestionHasQuestionMark(self):
        if self.question.endswith('?'):
            pass
        else:
            raise TypeError("Your question is missing a question mark.")

    def checkIfQuestionContainsAQuestionWord(self):
        questionWords = ['Why', 'What', 'How', 'Where', 'When', 'Who']
        wordsInSpecificQuestion = self.question.split()
        numberOfWordsInSpecificQuestion = len(wordsInSpecificQuestion)
        wordsThatAreNotQuestionWords = 0
        for word in wordsInSpecificQuestion:
            if word not in questionWords:
                wordsThatAreNotQuestionWords+= 1
            if numberOfWordsInSpecificQuestion == wordsThatAreNotQuestionWords:
                raise TypeError("Please form a proper question.")


class UserDataValidator:
    def __init__(self, userData):
        self.userData = userData
        self.requiredData = [
            'DateOfBirth',
            'GradeLevel',
            'TypeOfLearner',
            'StrongPersonalInterest',
        ]

    def validate(self):
        missingKeys = self.getMissingKeys()
        if missingKeys:
            self.raiseValidationError()

    def getMissingKeys(self):
        receivedKeys = self.getReceivedKeys()
        missingKeys = []
        for key in self.requiredData:
            if key not in receivedKeys:
                missingKeys.append(key)
        return missingKeys

    def getReceivedKeys(self):
        receivedKeys = []
        for item in self.userData:
            receivedKeys.append(item[0])
        return receivedKeys

    def raiseValidationError(self):
        errorMessage = 'You have malformed user data. Your data must contain all of the following values: '
        errorMessage += ', '.join(self.requiredData)
        raise ValueError(errorMessage)

class PromptUserProfile:
    def __init__(self, userData):
        self.userData = userData
        self.userProfile = {}

    def createUserProfile(self):
        self.processUserData()
        return self.getCompletedUserProfile()

    def processUserData(self):
        for item in self.userData:
            field = item[0]
            value = item[1]

            if field in ("FirstName", "LastName"):
                pass
            elif field == 'DateOfBirth':
                self.userProfile['Age'] = self.computeAgeFromDateOfBirth(value)
            else:
                self.userProfile[field] = value

    def computeAgeFromDateOfBirth(self, dateOfBirth):
        birthYear = int(dateOfBirth.split('-')[2])
        currentYear = pendulum.now().year
        return currentYear - birthYear

    def getCompletedUserProfile(self):
        return [
            ['Age', self.userProfile['Age']],
            ['Grade Level', self.userProfile['GradeLevel']],
            ['TypeOfLearner', self.userProfile['TypeOfLearner']],
            ['StrongPersonalInterest', self.userProfile['StrongPersonalInterest']],
        ]


class PromptPersonalizer:
    def __init__(self, basePrompt, promptBuilder):
        self.basePrompt = basePrompt
        self.promptUserProfile = {}
        self.promptBuilder = promptBuilder

    def personalize(self, userProfile):
        self.buildUserProfileHashMap(userProfile)
        return self.promptBuilder.build(self.promptUserProfile)

    def buildUserProfileHashMap(self, userProfile):
        assignValuesToPromptUserProfile = lambda item: self.promptUserProfile.update({item[0]: item[1]})
        list(map(assignValuesToPromptUserProfile, userProfile))

    def getFinalPrompt(self):
        return self.promptBuilder.build(self.promptUserProfile)


class PromptBuilder:
    def __init__(self, basePrompt, specificQuestion):
        self.basePrompt = basePrompt
        self.specificQuestion = specificQuestion

    def build(self, userProfile):
        profileSection = self.getProfileSection(userProfile)
        questionClarifier = self.getQuestionClarifier()

        personalizedPrompt = (
            f"{self.basePrompt}\n"
            f"{profileSection}\n"
            f"{questionClarifier}"
        )

        return self.placeSpecificQuestionInPrompt(personalizedPrompt)

    def getProfileSection(self, userProfile):
        return (
            "User Profile:\n"
            f"- Age: {userProfile['Age']}\n"
            f"- Grade Level: {userProfile['Grade Level']}\n"
            f"- Learning Preference: {userProfile['TypeOfLearner']}\n"
            f"- Key Interest: {userProfile['StrongPersonalInterest']}\n"
        )

    def getQuestionClarifier(self):
        return (
            "---\n"
            "\n"
            "Clarification Request:\n"
            "I feel the above requires more background knowledge than I currently have.\n"
            "Please explain it in more detail, using expressive and clear language, "
            "while tailoring examples to the above user's profile interests and learning style."
       )

    def placeSpecificQuestionInPrompt(self, personalizedPrompt):
            separator = "---"
            promptSections = personalizedPrompt.split(separator, 1)

            contentBeforeSeparator = promptSections[0]
            contentAfterSeparator = promptSections[1]

            modifiedPrompt = (
                contentBeforeSeparator.rstrip() + '\n\n' +
                f'"{self.specificQuestion}"\n\n' +
                separator +
                contentAfterSeparator
            )

            return modifiedPrompt
