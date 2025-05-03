import pendulum

class Prompt:
    def __init__(self, specificQuestion):
        self.specificQuestion = specificQuestion

    def personalize(self, basePrompt, userData):
        userProfile = self.createPromptUserProfile(userData)
        personalizedPrompt = self.personalizePrompt(basePrompt, userProfile)
        return self.placeSpecificQuestionInPrompt(personalizedPrompt, self.specificQuestion)

    def createPromptUserProfile(self, userData):
        userProfile = {}

        for item in userData:
            field = item[0]
            value = item[1]

            if field in ("FirstName" or "LastName"):
                pass
            elif field == 'DateOfBirth':
                dobStr = value
                birthYear = int(dobStr.split('-')[2])
                currentYear = pendulum.now().year
                age = currentYear - birthYear
                userProfile['Age'] = age
            else:
                userProfile[field] = value

        return [
            ['Age', userProfile['Age']],
            ['Grade Level', userProfile['GradeLevel']],
            ['TypeOfLearner', userProfile['TypeOfLearner']],
            ['StrongPersonalInterest', userProfile['StrongPersonalInterest']],
        ]

    def personalizePrompt(self, basePrompt, userProfile):
        age = None
        learningStyle = None
        interest = None
        gradeLevel = None
        for item in userProfile:
            if item[0] == 'Age':
                age = item[1]
            elif item[0] == 'TypeOfLearner':
                learningStyle = item[1]
            elif item[0] == 'StrongPersonalInterest':
                interest = item[1]
            elif item[0] == 'Grade Level':
                gradeLevel = item[1]
        profileSection = f"""User Profile:
- Age: {age}
- Grade Level: {gradeLevel}
- Learning Preference: {learningStyle}
- Key Interest: {interest}
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
