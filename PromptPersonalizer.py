import pendulum

class Prompt:
    def __init__(self, specificQuestion):
        self.specificQuestion = specificQuestion

    def personalize(self, basePrompt, userData):
        userProfile = self.createPromptUserProfile(userData)
        personalizedPrompt = self.personalizePrompt(basePrompt, userProfile)
        return self.placeSpecificQuestionInPrompt(personalizedPrompt, self.specificQuestion)

    def createPromptUserProfile(self, userData):
        age = None
        gradeLevel = None
        learningStyle = None
        interest = None
        
        for item in userData:
            if item[0] == 'DateOfBirth':
                dobStr = item[1]
                birthYear = int(dobStr.split('-')[2])
                currentYear = pendulum.now().year
                age = currentYear - birthYear
            elif item[0] == 'GradeLevel':
                gradeLevel = item[1]
            elif item[0] == 'TypeOfLearner':
                learningStyle = item[1]
            elif item[0] == 'StrongPersonalInterest':
                interest = item[1]
        
        return [
            ['Age', age],
            ['Grade Level', gradeLevel],
            ['TypeOfLearner', learningStyle],
            ['StrongPersonalInterest', interest],
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
        parts = basePrompt.split('---', 1)
        
        if len(parts) > 1:
            lastLineBeforeSep = parts[0].split('\n')[-1]
            indent = len(lastLineBeforeSep) - len(lastLineBeforeSep.lstrip())
            
            indentedQuestion = ' ' * indent + f'"{specificQuestion}"\n\n'
            indentedSeparator = ' ' * indent + '---'
            
            modifiedPrompt = f"{parts[0].rstrip()}\n\n{indentedQuestion}{indentedSeparator}{parts[1]}"
            return modifiedPrompt
        return basePrompt
