import requests

def get_repos(token):
    repo_names = []
    url = "https://api.github.com/orgs/BosklapperBende/repos"
    headers = { "Authorization" : token}
    jsonData = requests.get(url, headers=headers).json()
    for repoJson in jsonData:
        repo_names.append(repoJson['name'])
    print(repo_names)
    return repo_names


def get_commits_per_member(github_repo_list, token):
    commit_p_person = {}
    for github_repo in github_repo_list:
        url = "https://api.github.com/repos/BosklapperBende/{}/commits".format(github_repo)
        headers = { "Authorization" : token}
        jsonData = requests.get(url, headers=headers).json()

        for c in jsonData:
            if c['author']['login'] not in commit_p_person.keys():
                commit_p_person[c['author']['login']] = 0
            commit_p_person[c['author']['login']] += 1
    return commit_p_person
    