from pydantic import BaseModel
from typing import Literal, Annotated
from annotated_types import Len
from langchain_openai import ChatOpenAI

class ProjectDetails(BaseModel):
    project_name: str
    project_description: str
    department_responsible: Literal['AI', 'Software']
    most_important_development_skills: Annotated[list[Literal['Java', 'Python', 'Torch', 'ScikitLearn', 'JUnit', 'Selenium', 'Cucumber', 'Jest', 'TestNG', 'Project Management', 'Agile', 'Scrum', 'Lean', 'Strategy', 'JavaScript', 'React', 'Postman', 'TensorFlow', 'Keras', 'PyTorch', 'NodeJs', 'Vue', 'Docker', 'Leadership', 'Communication', 'TestRail', 'Spring', 'Hibernate', 'MySQL', 'Kubernetes', 'Test Strategy', 'Automation', 'SQL', 'Test Automation', 'Time Management', 'CNN', 'Express', 'OpenCV', 'Angular', 'TypeScript', 'Team Building', 'Conflict Resolution', 'CV', 'Deep Learning', 'NLP', 'C#', 'Project Planning', 'Manual Testing', 'Machine Learning', 'Data Science', 'ML', 'Operations', 'UI Testing', 'Performance', 'C++', 'API Testing', 'Performance Testing', 'Automated Testing', 'HTML', 'CSS', 'Computer Vision', 'AI', 'Git', 'SciKitLearn', 'Team Coordination', 'ASP.NET', 'Azure', 'AWS', 'Load Testing', 'Appium', 'Django', 'Strategic Planning', 'Kotlin', 'Team Management', 'Jenkins', 'JS']], Len(max_length=6), Len(min_length=3)]

class LLMService:
    def __init__(self, api_key: str, model: str):
        self.llm = ChatOpenAI(api_key=api_key, model=model, temperature=0)

    def chat_with_llm(self, prompt, project_details):
        system_message = f"""
        This is the scenario: {project_details}
        The project is about to start. The team needs to be assembled.

        Your task explain every team members responsibility.

        Example:
        - Team Lead: Responsibilities.
        - Senior: Responsibilities.
        - Tester: Responsibilities.
        - Mid Level 1: Responsibilities.
        - Mid Level 2: Responsibilities.
        - Junior 1: Responsibilities.

        You can give more scenario related information while explaining the responsibilities.
        """
        messages = [
            ("system", system_message),
            ("human", prompt),
        ]

        ai_msg = self.llm.invoke(messages)

        return ai_msg.content

    def parse_project_details(self, prompt):
        structured_llm = self.llm.with_structured_output(ProjectDetails)
        return structured_llm.invoke(prompt.__str__())