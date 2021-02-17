from github import Github
import os

from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
from .ghproj import GithubProject

def index(request):
    reponame = os.environ.get("REPO_NAME")
    domain = request.GET.get('domain')
    if domain:
        return status(request, domain)
    context = { 'domains': GithubProject.list_domains(reponame) }
    return render(request, 'status/index.html', context)

def status(request, domain):
    reponame = os.environ.get("REPO_NAME")
    issues, ok = GithubProject.get_domain(reponame, domain)
    if issues or ok:
        context = {'reponame': reponame, 'domain': domain, 'issues': issues, 'ok': ok }
        return render(request, 'status/status.html', context)
    raise Http404(f"No such domain {domain}")
