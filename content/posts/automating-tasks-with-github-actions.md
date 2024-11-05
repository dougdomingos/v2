+++
title = "Automating tasks with Github Actions"
date = "2024-11-01T17:35:48-03:00"
author = "Douglas Domingos"
tags = ["github-actions", "automation", "ci-cd"]
keywords = ["github", "python", "automation", "ci-cd"]
description = "GitHub Actions are a powerful, yet straightforward tool for automating tasks in your codebase, from running tests to building your project. Here, we'll approach its basic concepts and use cases."
showFullContent = false
readingTime = true
hideComments = false
+++

## Introduction

In software development, it’s common to have some tasks that need to be executed regularly, at a
specific time or in a certain order. Usually, teams would write dedicated scripts for these tasks,
which **adds complexity and diverts focus** from the main product.

That's where **CI/CD platforms** comes in, streamlining development workflows by automating
repetitive tasks so developers can focus on the actual software. Here, we’ll be exploring one of
these platforms: **GitHub Actions**.

## What are GitHub Actions?

**GitHub Actions** is a **CI/CD platform integrated directly into GitHub**, which allows you to
easily automate tasks within repositories. **Each repository can have multiple workflows**,
represented by YAML files located in the `.github/workflows/` directory. As you'll see, this makes
workflows **easy to write and understand**.

{{< picture src="/img/github-actions.png" alt="GitHub Actions" caption="Some template workflows offered by GitHub" >}}

You can define **workflows triggered by various events**, such as pushes and pull requests, and use
them for a wide range of tasks — testing, deploying to production, enforcing code style, and much
more. Workflows can even be **scheduled**, **combined with other workflows**, and used to **update
your repositories**. Plus, **you can leverage actions created by other developers**!

## Setting up an workflow

New workflows can be added to your repository in two ways:

- Through [GitHub](https://github.com/), where you can choose from many template workflows and
  adjust them as needed

- **By manually creating the workflow file** inside `.github/workflows`

Regardless of your choice, describing workflows is writing YAML files. And, to fully understand the
structure of a workflow, let's create one that simply prints "Hello Actions!" at each push made to
the repository.

## Workflow structure

Implementing our "Hello Actions" workflow is as simple as this:

```yaml
name: Simple Action

on: push

jobs:
  print-msg:
    runs-on: ubuntu-latest

    steps:
      - name: Print message
        run: echo "Hello Actions!"
```

Now, let's understand what each part of this code does:

- `name`, as it suggests, defines the name of the workflow. While it is optional, **I strongly
  recommend** to always specify the workflow name — not only for readability, but also to **allow
  workflow composition**.

- `on` defines the **events that will trigger the workflow's execution**. You can specify **multiple
  triggers** for the same workflow, and even **restrict the event scope** (e.g. pull requests to a
  specific branch, or changes made to a specific file).

- `jobs` describe **the actions performed by the workflow**. An workflow can have multiple jobs
  (that are executed on parallel by default), where each job is **identified by an unique name**.

  - Each job must define **the environment it runs on** (which is specified by the `runs-on` key)

  - A job describes **the tasks it executes as a sequence of `steps`**. Each step can execute
    commands, setup tasks and even other actions

## Example 1: Automating tests for pull requests made to the `main` branch

**Automating tests plays a crucial role at code maintainabilty**, as it ensures that **changes made
to the codebase do not break what previously worked**. Such task can be easily achieved with GitHub
Actions by setting up **an workflow that is executed for every pull request** made to the
repository.

Consider a project written in Java with Maven as build tool. We want to **automatically run all test
classes** for every pull request made to the `main` branch. This can be achieved with the following
workflow:

```yaml
name: Run tests with Maven

# The workflow only runs for pull requests made to the "main" branch
on:
  pull_requests:
    branches: "main"

jobs:
  run-tests:
    runs-on: ubuntu-latest

    steps:
      # Checks out (e.g. clones) the repository into the Actions runner
      - uses: actions/checkout@v4

      # Install the required Java version
      - name: Set up Java 17
        uses: actions/setup-java@v4
        with:
          java-version: "17"
          distribution: "temurin"
          cache: maven

      # Run tests with Maven
      - name: Test with Maven
        run: mvn test
```

## Example 2: Scheduled updates of a repository

In my [old website](https://github.com/dougdomingos/portfolio-v1), I've set up Next.js to regularly
fetch my repository list from [GitHub API](https://api.github.com), so that my project list would
always be updated. After migrating to [Hugo](https://gohugo.io/), I kept wondering on how to
implement this functionality with as little overhead as possible.

It turns out that **GitHub Actions was perfect for my scenario**. Simply write a workflow that
**fetches data from GitHub API** and **commits the updated list into the repository**. After some
_googling_ (and a little help from ChatGPT), I was able to come up with an working solution.

While **I chose to use Python for the fetch script**, you could write a similar solution in plain
old Shell Script (though the equivalent code would likely be _much_ more verbose) or in any language
you prefer.

First, here's my Python script for fetching and parsing the data, at `.github/scripts/fetch_data.py`:

```python
import requests
import yaml


def fetch_github_repos(username: str):
    """Fetch the repositories of a user from GitHub API

    Args:
        username (str): The username of the account to be fetched

    Returns:
        The contents of the response as a JSON object
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
        # You can add more properties here
        project = {
            "link": repo["html_url"],
            "info": {"title": repo["name"], "description": repo["description"]},
            "tags": repo["topics"],
        }

        projects.append(project)

    data = {"projects": projects}

    # Saves the project list as a YAML file
    with open("./data/projects.yaml", "w") as outfile:
        yaml.dump(data, outfile, default_flow_style=False, sort_keys=False)


if __name__ == "__main__":
    convert_to_yaml(fetch_github_repos("your_username"))
```

As for the workflow file, at `.github/workflows/fetch_projects.yaml`:

```yaml
name: Update project list

# Actions allow you to define environment variables too!
env:
  SCRIPT_PATH: .github/scripts/fetch_projects.py

# Gives the workflow write permissions over the repository
permissions:
  contents: write

# Workflow is scheduled to run every Sunday at 00h00
on:
  schedule:
    - cron: "0 0 * * 0"
  workflow_dispatch: # this allows us to manually run the workflow in GitHub

jobs:
  update-list:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: pip install pyyaml requests

      - name: Run script
        run: python ${{ env.SCRIPT_PATH }}

      - name: Commit changes to repository
        run: |
          git config --global user.name "<your-username-here>"
          git config --global user.email "<your-email-here>"
          git add ./data/projects.yaml
          git commit -m "chore(actions): update project list"
          git push
```

> **Cron syntax**: Cron schedules are specified by strings composed of five fields in a
> `M H DM MN DW` format, as described below:
>
> ```text
> M  H DM MN DW
> |  |  |  |  |
> |  |  |  |  └── Day of the week (0-7, where 0 and 7 = Sunday)
> |  |  |  └───── Month (1-12)
> |  |  └──────── Day of the month (1-31)
> |  └─────────── Hour (0-23)
> └────────────── Minute (0-59)
> ```
>
> So, `0 0 * * 0` means "at 00h00 of any day of any month on Sunday"

Also, to ensure that the updated list is avaliable in the website after the script is executed, I've
added a "hook" to **trigger the `build` workflow every time the `Update project list` workflow is
executed** — thus the importance of **always naming your workflows**:

```yaml
# ...
on:
  # ...
  # Specifies that the "build" workflow should execute after the
  # "Update project list" workflow is completed
  workflow_run:
    workflows: ["Update project list"]
    types:
      - completed
# ...
```

## Conclusion

GitHub Actions, as well as other CI/CD platforms, are **a powerful tool to master**. While I do
believe this post may help you with the basics, **I recommend taking a deeper look into the
[GitHub Actions documentation](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)**.

Also, feel free to use any of the workflows you've seen here in your projects. Try adding some new
features, or combining them with your own.

That's it for now. See ya! :wave:
