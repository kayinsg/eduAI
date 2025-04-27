import pendulum

class Prompt:
    def __init__(self, userData):
        self.userData = userData

    def personalizePrompt(self, basePrompt, userProfile):
        age = None
        learningStyle = None
        interest = None

        for item in userProfile:
            if item[0] == 'Age':
                age = item[1]
            elif item[0] == 'TypeOfLearner':
                learningStyle = item[1]
            elif item[0] == 'StrongPersonalInterest':
                interest = item[1]

        personalizedSection = f"""
User Profile:
- Age: {age}
- Learning Preference: {learningStyle}
- Key Interest: {interest}
"""

        finalPrompt = (
            basePrompt +
            personalizedSection +
            "\n---\n\nClarification Request:\nI feel the above requires more background knowledge than I currently have. \n" +
            "Please explain it in more detail, using expressive and clear language, " +
            "while tailoring examples to the above user's profile interests and learning style."
        )

        return finalPrompt.strip()

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

    def placeSpecificQuestionInPrompt(self, basePrompt, specificQuestion):
        parts = basePrompt.split('---', 1)

        if len(parts) > 1:
            last_line_before_sep = parts[0].split('\n')[-1]
            indent = len(last_line_before_sep) - len(last_line_before_sep.lstrip())

            indented_question = ' ' * indent + f'"{specificQuestion}"\n\n'
            indented_separator = ' ' * indent + '---'

            modified_prompt = f"{parts[0].rstrip()}\n\n{indented_question}{indented_separator}{parts[1]}"
            return modified_prompt
        return basePrompt
