import logging
from datetime import date

from django.contrib.auth.models import Group, User

from .neomodels import *


class DemoData:

    @staticmethod
    def django_users_groups() -> None:
        logging.info("Creating groups and users in Django DB")

        # Finance
        finance, _ = Group.objects.get_or_create(name="NEO4J_Finance")

        shaniqua = User.objects.create_user("shaniqua", "shaniqua@acme.com", "shaniqua")
        finance.user_set.add(shaniqua)

        tyrone = User.objects.create_user("tyrone", "tyrone@acme.com", "tyrone")
        finance.user_set.add(tyrone)

        # Sales
        sales, _ = Group.objects.get_or_create(name="NEO4J_Sales")

        loraine = User.objects.create_user("loraine", "loraine@acme.com", "loraine")
        sales.user_set.add(loraine)

        chen = User.objects.create_user("chen", "chen@acme.com", "chen")
        sales.user_set.add(chen)

        # Group that can see all data
        audit, _ = Group.objects.get_or_create(name="NEO4J_Audit")

        devon = User.objects.create_user("devon", "devon@acme.com", "devon")
        audit.user_set.add(devon)

    @staticmethod
    def neo4j_demo_data() -> None:
        logging.info("Creating project data in Neo4J")

        # Finance dept.
        finance_dept = Department(name="Finance").save()

        shaniqua = Worker(name="shaniqua").save()
        shaniqua.department.connect(finance_dept)

        tyrone = Worker(name="tyrone").save()
        tyrone.department.connect(finance_dept)

        # Finance - Project SOXX Compliance
        project_sox = Project(name="SOX comp 2025",
                              description="All our efforts for retained compliance").save()
        project_sox.department.connect(finance_dept)

        task_internalaudit = ProjectTask(
            description="Coordinate internal audit",
            created=date.fromisoformat("2024-05-01"),
            priority="H"
        ).save()
        task_internalaudit.project.connect(project_sox)
        task_internalaudit.worker.connect(shaniqua)

        task_gapanalysis = ProjectTask(
            description="Compliance gap analysis",
            created=date.fromisoformat("2024-05-20"),
            priority="M"
        ).save()
        task_gapanalysis.project.connect(project_sox)
        task_gapanalysis.worker.connect(shaniqua)

        # Finance - Project Tax neutrality
        project_taxneutral = Project(name="Tax neutrality 2029",
                                     description="Becoming tax neutral for our ultimate beneficial owners").save()
        project_taxneutral.department.connect(finance_dept)

        task_evaluatelegal = ProjectTask(
            description="Evaluate legal assistance firms",
            created=date.fromisoformat("2024-03-27"),
            priority="L"
        ).save()
        task_evaluatelegal.project.connect(project_taxneutral)
        task_evaluatelegal.worker.connect(tyrone)

        task_setmilestones = ProjectTask(
            description="Set milestones for 2024/2025",
            created=date.fromisoformat("2024-05-13"),
            priority="M"
        ).save()
        task_setmilestones.project.connect(project_taxneutral)
        task_setmilestones.worker.connect(tyrone)

        # Sales department
        sales_dept = Department(name="Sales").save()

        loraine = Worker(name="loraine").save()
        loraine.department.connect(sales_dept)

        chen = Worker(name="chen").save()
        chen.department.connect(sales_dept)

        # Sales - project marketplace integrator
        project_dachonline = Project(
            name="DACH marketplace integrator",
            description="connect with an integrator for online marketplaces in DACH"
        ).save()
        project_dachonline.department.connect(sales_dept)

        task_dachpartner = ProjectTask(
            description="select an integrator based on strategic and cost factors",
            created=date.fromisoformat("2024-03-06"),
            priority="M"
        ).save()
        task_dachpartner.project.connect(project_dachonline)
        task_dachpartner.worker.connect(loraine)

        task_dachtargets12m = ProjectTask(
            description="set DACH online sales targets for the first 12 months",
            created=date.fromisoformat("2023-04-18"),
            priority="L"
        ).save()
        task_dachtargets12m.project.connect(project_dachonline)
        task_dachtargets12m.worker.connect(loraine)

        task_dachit1 = ProjectTask(
            description="manage IT resource planning and partner expectations",
            created=date.fromisoformat("2024-03-25"),
            priority="M"
        ).save()
        task_dachit1.project.connect(project_dachonline)
        task_dachit1.worker.connect(chen)

        task_dachit2 = ProjectTask(
            description="determine additional human and IT needs and a cost estimation",
            created=date.fromisoformat("2024-04-16"),
            priority="M"
        ).save()
        task_dachit2.project.connect(project_dachonline)
        task_dachit2.worker.connect(chen)
