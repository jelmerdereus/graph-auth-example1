import json
import logging
from typing import List

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed, \
    HttpResponseNotFound, \
    HttpResponseServerError
from django.template import loader

from website.neomodels import ProjectTask


# illegal requests
def illegal(req: HttpRequest) -> HttpResponse:
    logging.warning(f"Request not allowed: {req.method} @ {req.path} by {req.get_host()}")
    return HttpResponseNotAllowed("Illegal request")


# index page
def index(req: HttpRequest) -> HttpResponse:
    if req.method != "GET":
        return illegal(req)

    template = loader.get_template('index.html')
    return HttpResponse(template.render(request=req))


# login page
def login_form(req: HttpRequest) -> HttpResponse:
    template = loader.get_template("login.html")

    # load the login page
    if req.method == "GET":
        return HttpResponse(template.render(request=req))

    # process a login attempt
    elif req.method == "POST":
        user = req.POST.get("inputUser")
        password = req.POST.get("inputPassword")

        user = authenticate(request=req, username=user, password=password)
        if user is not None:
            login(req, user)
            return HttpResponseRedirect("/")
        else:
            context = {"login_error_message": "Could not log you in. Try again"}
            return HttpResponse(template.render(context, request=req))

    # other methods not allowed
    return illegal(req)


# logout request
def logout_link(req: HttpRequest) -> HttpResponse:
    if req.method != "GET":
        return illegal(req)

    logout(req)
    return HttpResponseRedirect("/")


@login_required()
def project_tasks(req: HttpRequest):
    if req.method != "GET":
        return illegal(req)

    user: User = req.user

    # we need to know the department visibility based on user groups starting with NEO4J_
    neo4j_depts: List[str] = django_neo4j_groups(user)
    if not neo4j_depts:
        return HttpResponseNotFound("data not found for your user account")

    # retrieve project tasks that are visible for this user
    try:
        project_tasks = ProjectTask().get_for_scope(neo4j_depts)
        json_data = json.dumps(project_tasks)
        return HttpResponse(json_data)
    except Exception as ex:
        logging.error(f"Exception: {ex}")
        return HttpResponseServerError("Something went wrong")


@login_required()
def own_project_tasks(req: HttpRequest):
    if req.method != "GET":
        return illegal(req)

    user: User = req.user

    # we need to know the department visibility based on user groups starting with NEO4J_
    neo4j_depts: List[str] = django_neo4j_groups(user)
    if not neo4j_depts:
        return HttpResponseNotFound("data not found for your user account")

    # retrieve project tasks that are assigned to the user
    try:
        project_tasks = ProjectTask().get_for_assigned_worker(user.username)

        json_data = json.dumps(project_tasks)
        return HttpResponse(json_data)
    except Exception as ex:
        logging.error(f"Exception: {ex}")
        return HttpResponseServerError("Something went wrong")


# return zero or more user groups starting with NEO4J_
def django_neo4j_groups(user: User) -> List[str]:
    neo4j_depts = [gr.name[6:] for gr in user.groups.all() if gr.name.startswith("NEO4J_")]
    return neo4j_depts
