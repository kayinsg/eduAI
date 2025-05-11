import pendulum

class Prompt:
    def __init__(self, specificQuestion):
        self.specificQuestion = specificQuestion

    def personalize(self, basePrompt, userData):
        userProfile = self.createPromptUserProfile(userData)
        personalizedPrompt = self.personalizePrompt(basePrompt, userProfile)
        return self.placeSpecificQuestionInPrompt(personalizedPrompt, self.specificQuestion)

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
    def __init__(self, basePrompt):
        self.basePrompt = basePrompt
        self.promptUserProfile = {}

    def personalize(self, userProfile):
        self.buildUserProfileHashMap(userProfile)
        personalizedPrompt = self.getFinalPrompt(self.basePrompt)
        return personalizedPrompt

    def buildUserProfileHashMap(self, userProfile):
        for item in userProfile:
            field = item[0]
            value = item[1]
            self.promptUserProfile[field] = value

    def getFinalPrompt(self, basePrompt):
        personalizedPrompt = f"""{basePrompt}
{self.getProfileSection()}
{self.getQuestionClarifier()}"""
        return personalizedPrompt

    def getProfileSection(self):
        return f"""User Profile:
- Age: {self.promptUserProfile['Age']}
- Grade Level: {self.promptUserProfile['Grade Level']}
- Learning Preference: {self.promptUserProfile['TypeOfLearner']}
- Key Interest: {self.promptUserProfile['StrongPersonalInterest']}
"""

    def getQuestionClarifier(self):
        return """---

Clarification Request:
I feel the above requires more background knowledge than I currently have.
Please explain it in more detail, using expressive and clear language, while tailoring examples to the above user's profile interests and learning style.""".strip()
