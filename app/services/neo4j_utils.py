from langchain_community.graphs import Neo4jGraph
import os 

def search_from_neo4j(graph, department_list, seniority_list, skills_list, max_user_count, dont_select="noone"):
    query_text = f"""
    MATCH (p:Person)-[:HAS_SKILL]->(s:Skill), 
      (p)-[:HAS_LEVEL]->(l:SeniorityLevel), 
      (d:Department)-[:HAS_MEMBER]->(p)
    WHERE p.isAvailable = TRUE
    AND p.name <> '{dont_select}'
    AND d.name IN {department_list}
    AND l.name IN {seniority_list}
    AND s.name IN {skills_list}
    WITH DISTINCT p
    MATCH (p)-[:HAS_SKILL]->(allSkills:Skill)
    RETURN p, collect(allSkills.name) AS skills
    LIMIT {max_user_count} """
    return graph.query(query_text)


def update_graph_with_csv():
    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_user = os.getenv("NEO4J_USERNAME")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    graph = Neo4jGraph(username=neo4j_user, password=neo4j_password, url=neo4j_uri)

    members_query = """
    LOAD CSV WITH HEADERS FROM 
    'https://raw.githubusercontent.com/OmerSukruAk/team_formation_using_knowledgegraphs/refs/heads/main/team_members.csv'
    AS row

    MERGE (p:Person {id: row.Team_member_id, name: row.Team_member_name})
    SET p.level = row.Team_member_level,
        p.isAvailable = (row.IsAvailable = 'True')  // Correctly assign boolean value

    FOREACH (skill IN split(row.Team_member_skills, '-') |
        MERGE (s:Skill {name: trim(skill)})
        MERGE (p)-[:HAS_SKILL]->(s)
    )

    MERGE (level:SeniorityLevel {name: row.Team_member_level})
    MERGE (p)-[:HAS_LEVEL]->(level)

    MERGE (d:Department {name: row.Team_member_department})
    MERGE (d)-[:HAS_MEMBER]->(p)

    MERGE (a:Availability {status: p.isAvailable})
    MERGE (p)-[:HAS_AVAILABILITY]->(a)
    """
    
    graph.query(members_query)