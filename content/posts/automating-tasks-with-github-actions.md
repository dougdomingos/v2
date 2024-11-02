+++
title = "Automating tasks with Github Actions"
date = "2024-11-01T17:35:48-03:00"
author = "Douglas Domingos"
tags = ["github-actions", "automation", "ci"]
keywords = ["github", "python", "automation", "ci"]
description = "GitHub Actions are a powerful, yet straightforward tool for automating tasks in your codebase, from running tests to building your project. Here, we'll approach its basic concepts and use cases."
showFullContent = false
readingTime = true
hideComments = false
+++

## Introduction

While developing software, it's very common to have a set of **tasks that must be executed
repeatedly, in a specific order or time**. This would require the team to create dedicated
scripts for those tasks, **increasing complexity and diverting the team's focus**.

It's in these situations that **CI/CD platforms** shines the brightest, simplifying the
development workflow by **automating tasks**, allowing devs to focus on the real software.
Today, we're taking a look on one of those: **GitHub Actions**.

## What are GitHub Actions?

**GitHub Actions** is a CI/CD platform directly integrated with GitHub, which allows you
to easily automate tasks in your repository. **Each repository can have multiple
workflows**, represented by YAML files inside the `.github/workflows/` directory of a
repository. This make workflows easy to write and understand.

{{< picture src="/img/github-actions.png" alt="GitHub Actions" caption="Actions can be use for a wide range of tasks" >}}

You can define workflows **triggered by different types of events** (like pushes and pull
requests), and use them for a vast variety of tasks, like testing, deploying to production,
code style checking, and many, many more. Not only that, workflows can also be **run on a
schedule**, **combined with other workflows** and even **edit your repository**, by adding
or modifying branches and files. You can even **use actions created by other developers**!

## Setting up an workflow

New workflows can be added to your repository in two ways:

- Through [GitHub](https://github.com/) itself. You may choose to either **create the
  YAML file from scratch** or **use a template workflow**

- **Manually creating YAML files** inside the `.github/workflows` directory

To fully understand the YAML structure of a workflow, let's create a simple action that
prints "Hello Actions!" when executed.

### Basic structure

A workflow YAML file have at least three blocks: `name`, `on`, and `jobs`.

- `name`: as it suggests, it defines the name of the workflow. If omitted, GitHub will
  use the **file path relative** to the root of the repository.

- `on`: defines the **events that will trigger the workflow's execution**. Workflows
  may have **multiple event triggers**, and can be **restricted to changes on a specific
  set of branches or files**.

- `jobs`: here's where you define **the tasks performed by the workflow**. You may define
  multiple jobs (that runs on parallel by default), and each job can also specify
  **the environment it runs on**, (e.g `ubuntu-latest`, `windows-latest`, `macos-latest`).

### Writing our "Hello Actions!" workflow

Considering our action that prints "Hello Actions!", here's the workflow YAML file:

```yaml
name: Simple Action

# The action will run at every push made to the repository
on: push

jobs:
  print-msg:
    runs-on: ubuntu-latest

    steps:
      - name: Print message
        run: echo "Hello Actions!"
```

Here, we have one job `print-msg` with only one step (that actually prints the
message). Each job can have multiple steps.

## Use case: automatically running tests for pull requests

Let's consider a Java application built with Maven. It would be very convenient to
**run the tests for every pull request made to the `main` branch**, right? So, let's
write a workflow for that.

Our workflow only needs to setup Java and execute the test suites, so we only need
one job:

```yaml
name: Run tests with Maven

# [...]

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

Now, to execute the workflow at each pull request to the `main` branch, add the
following code to the `on` block:

```yaml
# The action only runs for pull requests made to the main branch
on:
  pull_requests:
    branches: "main"
```

Here's the complete YAML file:

```yaml
name: Run tests with Maven

on:
  pull_request:
    branches: "main"

jobs:
  run-tests:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Java 17
        uses: actions/setup-java@v4
        with:
          java-version: "17"
          distribution: "temurin"
          cache: maven

      - name: Test with Maven
        run: mvn test
```

## Use case: schedule updates in your repository

This is the reason I've wrote this post: using GitHub Actions, I was able to write a
workflow that **updates my [project list](/projects) weekly**, fetching the data from
GitHub API and **commiting the repository list back to the repository**.

Here's the catch: fetching and ordering the data from GitHub API is **not fitted for
simple shellscripts**, so **I choose to use Python** for this task. But how can we
**integrate a Python script in our workflow**? Also, how can we **make the script run
automatically** every week?

First, let's create the script for fetching and parsing the data, at `.github/scripts/fetch_data.py`:

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
        # You can add more repository properties here
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

In the workflow, install Python and add the required `pyyaml` and `requests` libraries:

```yaml
name: Update project list

# The "env" property allows us to define environment variables
env:
  SCRIPT_PATH: .github/scripts/fetch_projects.py

on:
  workflow_dispatch: # this allows us to manually run the workflow in GitHub

jobs:
  update-list:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      # Install the required Python version
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      # Ensure required packages are installed
      - name: Install dependencies
        run: pip install pyyaml requests

      # Execute the script
      - name: Run script
        run: python ${{ env.SCRIPT_PATH }}
```

Now, we need to commit the updated file back to our repository. The workflow file
must have write permission to the repository. For that, add the following code:

```yaml
# This allows the workflow to make changes to the repository
# ...
permissions:
  contents: write

jobs:
  update-list:
    # ...
    # Commit the updated file into the repository
    - name: Commit changes to repository
      run: |
        git config --global user.name "<your-username-here>"
        git config --global user.email "<your-email-here>"
        git add ./data/projects.yaml
        git commit -m "chore(actions): update project list"
        git push
```

Finally, we want to schedule the script to run at a specific time (at 00h00 of
every Sunday). Luckily, Actions allows us to schedule workflows with Cron-like
syntax. Just add this code to your `on` block:

```yaml
# ...
on:
  schedule:
    - cron: "0 0 * * 0"
  workflow_dispatch:
# ...
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

Here's the complete workflow:

```yaml
name: Update project list

env:
  SCRIPT_PATH: .github/scripts/fetch_projects.py

permissions:
  contents: write

on:
  schedule:
    - cron: "0 0 * * 0"
  workflow_dispatch:

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

Also, to ensure that the updated list is avaliable in the website after the script is
executed, I've added the following block to my `build` workflow:

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

GitHub Actions, as well as other CI/CD platforms, are **a powerful tool to master**.
Although this post not nearly enough to make you an automation specialist, **I recommend
taking a deeper look into the [GitHub Actions documentation](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions)**.

See ya! :wave:
