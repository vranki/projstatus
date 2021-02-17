from github import Github
import re
import json

# Helper class with reusable code for github project stuff
class GithubProject:
    def get_domains(description):
        p = re.compile('domains=\{.*\}')
        matches = json.loads(p.findall(description)[0][8:])
        return matches

    def list_domains(reponame):
        g = Github()
        repo = g.get_repo(reponame)
        domainjson = GithubProject.get_domains(repo.description)
        domains = []
        for name, color in domainjson.items():
            domains.append(name)
        return tuple(domains)

    def get_domain(reponame, domain):
        g = Github()
        repo = g.get_repo(reponame)
        domains = GithubProject.get_domains(repo.description)
        if(not len(domains)):
            return None, None
        domain_color = domains.get(domain, None)
        if not domain_color:
            return None, None

        open_issues = repo.get_issues(state='open')
        domain_labels = []
        labels = repo.get_labels()
        for label in labels:
            if label.color == domain_color[1:]:
                domain_labels.append(label)

        domain_issues = dict()
        domain_ok = []
        for label in domain_labels:
            label_issues = []
            for issue in open_issues:
                if label in issue.labels:
                    label_issues.append(issue)
            if len(label_issues):
                domain_issues[label.name] = label_issues
            else:
                domain_ok.append(label.name)

        return domain_issues, domain_ok

    def domain_to_string(reponame, issues, ok):
        text_out = reponame + ":\n"
        for label in issues.keys():
            text_out = text_out + f'{label}: '
            for issue in issues[label]:
                # todo: add {issue.html_url} when URL previews can be disabled
                text_out = text_out + f'[{issue.title}] '
            text_out = text_out + f'\n'

        text_out = text_out + " OK : " + ', '.join(ok)
        return text_out

    def domain_to_html(reponame, issues, ok):
        html_out = f'<b>{reponame}:</b> <br/>'
        for label in issues.keys():
            html_out = html_out + f'🚧 {label}: '
            for issue in issues[label]:
                # todo: add {issue.html_url} when URL previews can be disabled
                html_out = html_out + f'[{issue.title}] '
            html_out = html_out + f'<br/>'

        html_out = html_out + " OK ☑️ " + ', '.join(ok)
        return html_out
