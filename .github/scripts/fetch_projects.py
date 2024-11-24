import requests
import yaml


def fetch_github_repos(username: str):
    """Fetch the repositories of a user from GitHub API

    Args:
        username (str): The username of the account to be fetched

    Returns:
        _any_: The contents of the response in a JSON structure
    """

    FETCH_URL = f"https://api.github.com/users/{username}/repos"
    response = requests.get(FETCH_URL)

    if response.status_code != 200:
        print(f"Failed while fetching data: HTTP {response.status_code}")
        return []

    return response.json()


def convert_to_yaml(repo_list: list):
    """Given the contents of the request, create the equivalent YAML file.

    Args:
        repos_data (list): The JSON structure of repository
    """

    # Order repositories by most recent updated
    repo_list = sorted(repo_list, key=lambda repo: repo["updated_at"], reverse=True)
    projects = []

    for repo in repo_list:
        project = {
            "link": repo["html_url"],
            "info": {"title": repo["name"], "description": repo["description"]},
            "tags": repo["topics"],
        }

        projects.append(project)

    with open("./data/projects.yaml", "w") as outfile:
        yaml.dump(projects, outfile, default_flow_style=False, sort_keys=False)


if __name__ == "__main__":
    convert_to_yaml(fetch_github_repos("dougdomingos"))
