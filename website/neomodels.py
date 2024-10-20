import os
from typing import List

from neomodel import config, StructuredNode, StringProperty, DateProperty, RelationshipTo

# Neo4j database connection
conn_type = os.getenv("NEO4J_CONN", "neo4j")
username = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PW")
hostname = os.getenv("NEO4J_HOST", "localhost")
tcp_port = os.getenv("NEO4J_PORT", 7687)
database = os.getenv("NEO4J_DB", "neo4j")

config.DATABASE_URL = f"{conn_type}://{username}:{password}@{hostname}:{tcp_port}"
config.DATABASE_NAME = database


# Property Graph models
class Department(StructuredNode):
    name = StringProperty(unique_index=True, required=True)


class Worker(StructuredNode):
    name = StringProperty(index=True, required=True)
    department = RelationshipTo('Department', 'IN_DEPARTMENT')


class Project(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    description = StringProperty(required=True)
    department = RelationshipTo('Department', 'IN_DEPARTMENT')

    def get_for_departments(self, departments: List[str]) -> List:
        # define query scope
        query: str | None
        if "Audit" in departments:
            query = f"""MATCH (p:Project) RETURN p"""
        else:
            query = f"""MATCH (d:Department) WHERE d.name in {departments} """
            query += f"""MATCH (p:Project)-[IN_DEPARTMENT]-(d) RETURN p"""

        # run query
        neo4j_data, _ = self.cypher(query)
        return [self.inflate(p[0]) for p in neo4j_data]


class ProjectTask(StructuredNode):
    description = StringProperty(required=True)
    created = DateProperty(index=True, required=True)
    priority = StringProperty(index=True, required=True, choices={"L": "low", "M": "medium", "H": "high"})
    project = RelationshipTo('Project', 'TASK_OF')
    worker = RelationshipTo('Worker', 'ASSIGNED_TO')

    @staticmethod
    def __data_to_dict(record):
        return {
            "project": record[0],
            "task_description": record[1],
            "created": record[2],
            "priority": record[3],
            "worker": record[4]
        }

    def get_for_scope(self, groups: List[str]):
        # define projects that are in authorized scope
        query: str | None
        if "Audit" in groups:
            query = f"""MATCH (p:Project) """
        else:
            query = f"""MATCH (d:Department) WHERE d.name in {groups} """
            query += f"""MATCH (p:Project)-[IN_DEPARTMENT]-(d) """

        # query for project tasks within the project scope
        query += """MATCH (t:ProjectTask)-[TASK_OF]-(p) """
        query += """MATCH (t)-[ASSIGNED_TO]-(w:Worker) """
        query += """RETURN p.name as project, t.description as task_description, t.created as created, t.priority as priority, w.name as worker"""

        response_data, _ = self.cypher(query)
        return [self.__data_to_dict(record) for record in response_data]

    def get_for_assigned_worker(self, worker: str):
        # define projects tasks that are in workers scope
        query = f"""MATCH (w:Worker) WHERE w.name = '{worker}' """
        query += f"""MATCH (t:ProjectTask)-[ASSIGNED_TO]-(w)"""
        query += f"""MATCH (t)-[TASK_OF]-(p:Project) """

        query += """RETURN p.name as project, t.description as task_description, t.created as created, t.priority as priority, w.name as worker"""

        response_data, _ = self.cypher(query)
        return [self.__data_to_dict(record) for record in response_data]
