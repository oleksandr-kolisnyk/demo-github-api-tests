# Demo project - testing GitHub REST API

## Setup

* install Python 3 (tested on Python 3.11 only)
* install project (`pip install -r requirements.txt`)
* create `.env` file and add configurations (more below)

## Configure environment

Add environment variables to your `.env` file (refer to `example.env` for example).
Supported env variables:
* `GH_PAT` (required) - your GitHub Personal Access Token. [How to create Personal Access Token](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). Token must be granted with `repo`, `user` and `delete_repo` privileges.
* `GH_API_VER` - version of GH API. Set to `2022-11-28` by default.
* `MAIN_BRANCH` - name of main branch setting for every repository in your account. Usually it is `master` or `main`. Set to `master` by default.

## Run tests

Just run:
```buildoutcfg
pytest -s
```
