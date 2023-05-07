import os
from os import getenv

from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv(".env")


GH_PAT = getenv("GH_PAT")
GH_API_VER = getenv("GH_API_VER") or "2022-11-28"

GH_URI = "https://api.github.com/"

MAIN_BRANCH = getenv("MAIN_BRANCH") or "master"
