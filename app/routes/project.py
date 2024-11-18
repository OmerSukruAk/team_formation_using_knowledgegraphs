from fastapi import APIRouter
from app.services.llm_service import LLMService
from app.services.neo4j_utils import Neo4jGraph, search_from_neo4j
from config.settings import get_env_variable

router = APIRouter()

service = LLMService(api_key=get_env_variable("OPENAI_API_KEY"), model="gpt-4o-mini")

@router.post("/project_details")
def read_project_details(project_details: str):
    
    skills_required_for_project = service.parse_project_details(project_details)

    neo4j_uri = get_env_variable("NEO4J_URI")
    neo4j_user = get_env_variable("NEO4J_USERNAME")
    neo4j_password = get_env_variable("NEO4J_PASSWORD")

    graph = Neo4jGraph(username=neo4j_user, password=neo4j_password, url=neo4j_uri)

    team_lead = search_from_neo4j(graph, [skills_required_for_project.department_responsible], ['Team Lead'], skills_required_for_project.most_important_development_skills, 1)
    senior = search_from_neo4j(graph, [skills_required_for_project.department_responsible], ['Senior'], skills_required_for_project.most_important_development_skills, 1)
    tester = search_from_neo4j(graph, [skills_required_for_project.department_responsible,"Test"], ['Senior','Mid-Level'], skills_required_for_project.most_important_development_skills, 1,senior[0]['p']['name'])
    mid_level = search_from_neo4j(graph, [skills_required_for_project.department_responsible], ['Mid-Level'], skills_required_for_project.most_important_development_skills, 2)
    junior = search_from_neo4j(graph, [skills_required_for_project.department_responsible], ['Junior'], skills_required_for_project.most_important_development_skills, 2)


    try: 
        prompt = f"""
        Our ai system determined those will be in the team:
        - Team Lead: {team_lead[0]['p']['name']}
        - Senior: {senior[0]['p']['name']}
        - Tester: {tester[0]['p']['name']}
        - Mid Level 1: {mid_level[0]['p']['name']}
        - Mid Level 2: {mid_level[1]['p']['name']}
        - Junior 1: {junior[0]['p']['name']}
        """

        return {"project_details": service.chat_with_llm(prompt, project_details), "status": "success"}
    except Exception as e:
        return {"project_details": f"No team found for the project details: {project_details}", "status": "failed"}