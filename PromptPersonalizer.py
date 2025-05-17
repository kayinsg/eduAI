import pendulum


class Prompt:
    def __init__(self, specificQuestion):
        self.specificQuestion = specificQuestion

    def personalize(self, basePrompt, userData):
        self.validateQuestion()
        userProfile = self.createPromptUserProfile(userData)
        personalizedPrompt = self.personalizePrompt(basePrompt, userProfile)
        return self.placeSpecificQuestionInPrompt(personalizedPrompt, self.specificQuestion)

    def validateQuestion(self):
        QuestionChecker(self.specificQuestion).validateQuestion()

    def createPromptUserProfile(self, userData):
        return PromptUserProfile(userData).createUserProfile()

    def personalizePrompt(self, basePrompt, userProfile):
        return PromptPersonalizer(basePrompt).personalize(userProfile)

    def placeSpecificQuestionInPrompt(self, basePrompt, specificQuestion):
            separator = "---"
            promptSections = basePrompt.split(separator, 1)

            contentBeforeSeparator = promptSections[0]
            contentAfterSeparator = promptSections[1]

            modifiedPrompt = (
                contentBeforeSeparator.rstrip() + '\n\n' +
                f'"{specificQuestion}"\n\n' +
                separator +
                contentAfterSeparator
            )

            return modifiedPrompt


class QuestionChecker:
    def __init__(self, question):
        self.question = question

    def validateQuestion(self):
        questionWords = ['Why', 'What', 'How', 'Where', 'When', 'Who']
        wordsInSpecificQuestion = self.question.split()
        if not self.question.endswith('?'):
            raise TypeError("Your question is missing a question mark.")
        else:
            numberOfWordsInSpecificQuestion = len(wordsInSpecificQuestion)
            wordsThatAreNotQuestionWords = 0
            for word in wordsInSpecificQuestion:
                if word not in questionWords:
                    wordsThatAreNotQuestionWords+= 1
                if numberOfWordsInSpecificQuestion == wordsThatAreNotQuestionWords:
                    raise TypeError("Please form a proper question.")

class PromptUserProfile:
    def __init__(self, userData):
        self.userData = userData
        self.userProfile = {}

    def createUserProfile(self):
        self.validateUserData()
        self.processUserData()
        return self.getCompletedUserProfile()

    def validateUserData(self):
        requiredData = [
            'DateOfBirth',
            'GradeLevel',
            'TypeOfLearner',
            'StrongPersonalInterest',
        ]
        receivedKeys = []
        for item in self.userData:
            receivedKeys.append(item[0])
        missingKeys = []
        for key in requiredData:
            if key not in receivedKeys:
                missingKeys.append(key)
        if len(missingKeys) > 0:
            errorMessage = 'You have malformed user data. Your data must contain all of the following values: '
            errorMessage += ', '.join(requiredData)
            raise ValueError(errorMessage)

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
    def __init__(self, basePrompt):
        self.basePrompt = basePrompt
        self.promptUserProfile = {}

    def personalize(self, userProfile):
        self.buildUserProfileHashMap(userProfile)
        personalizedPrompt = self.getFinalPrompt(self.basePrompt)
        return personalizedPrompt

    def buildUserProfileHashMap(self, userProfile):
        assignValuesToPromptUserProfile = lambda item: self.promptUserProfile.update({item[0]: item[1]})
        list(map(assignValuesToPromptUserProfile, userProfile))

    def getFinalPrompt(self, basePrompt):
        profileSection = self.getProfileSection()
        questionClarifier = self.getQuestionClarifier()

        personalizedPrompt = (
            f"{basePrompt}\n"
            f"{profileSection}\n"
            f"{questionClarifier}"
        )

        return personalizedPrompt

    def getProfileSection(self):
        return (
            "User Profile:\n"
            f"- Age: {self.promptUserProfile['Age']}\n"
            f"- Grade Level: {self.promptUserProfile['Grade Level']}\n"
            f"- Learning Preference: {self.promptUserProfile['TypeOfLearner']}\n"
            f"- Key Interest: {self.promptUserProfile['StrongPersonalInterest']}\n"
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
