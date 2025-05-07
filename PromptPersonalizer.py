import pendulum

class Prompt:
    def __init__(self, specificQuestion):
        self.specificQuestion = specificQuestion

    def personalize(self, basePrompt, userData):
        userProfile = self.createPromptUserProfile(userData)
        personalizedPrompt = self.personalizePrompt(basePrompt, userProfile)
        return self.placeSpecificQuestionInPrompt(personalizedPrompt, self.specificQuestion)

    def createPromptUserProfile(self, userData):
        return UserProfile(userData).createUserProfile()

    def personalizePrompt(self, basePrompt, userProfile):
        promptUserProfile = { }
        for item in userProfile:
            field = item[0]
            value = item[1]
            promptUserProfile[field] = value

        profileSection = f"""User Profile:
- Age: {promptUserProfile['Age']}
- Grade Level: {promptUserProfile['Grade Level']}
- Learning Preference: {promptUserProfile['TypeOfLearner']}
- Key Interest: {promptUserProfile['StrongPersonalInterest']}
"""
        return f"""{basePrompt}
{profileSection}
---

Clarification Request:
I feel the above requires more background knowledge than I currently have.
Please explain it in more detail, using expressive and clear language, while tailoring examples to the above user's profile interests and learning style.""".strip()

    def placeSpecificQuestionInPrompt(self, basePrompt, specificQuestion):
            separator = "---"
            promptSections = basePrompt.split(separator, 1)

            if len(promptSections) < 2:
                return basePrompt

            contentBeforeSeparator = promptSections[0]
            contentAfterSeparator = promptSections[1]

            lastLineBeforeSeparator = contentBeforeSeparator.split('\n')[-1]
            indentation = len(lastLineBeforeSeparator) - len(lastLineBeforeSeparator.lstrip())

            indentedQuestion = ' ' * indentation + f'"{specificQuestion}"\n\n'
            indentedSeparator = ' ' * indentation + separator

            modifiedPrompt = (
                contentBeforeSeparator.rstrip() + '\n\n' +
                indentedQuestion +
                indentedSeparator +
                contentAfterSeparator
            )

            return modifiedPrompt

class UserProfile:
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
