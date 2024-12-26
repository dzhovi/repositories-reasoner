# The MIT License (MIT)
#
# Copyright (c) 2024 Vakhidov Dzhovidon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import requests
import logging
from datetime import datetime
from dataclasses import dataclass


@dataclass
class RepositoryMetrics:
    """
    Data model to hold repository metrics.
    """

    stars: int
    forks: int
    last_push: datetime
    open_issues: int
    archived: bool

    @property
    def days_since_last_push(self) -> int:
        """
        Calculate the number of days since the repository was last pushed.
        """
        return (datetime.utcnow() - self.last_push).days


class GitHubRepository:
    """
    A class to fetch and analyze GitHub repository details.
    """

    BASE_URL = "https://api.github.com/repos"

    def __init__(self, repository: str):
        """
        Initialize with repository name in the format 'owner/repo'.
        """
        self.repository = repository
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        self.repo_data = None

    def fetch_repository_data(self):
        """
        Fetch repository details from the GitHub API.
        """
        url = f"{self.BASE_URL}/{self.repository}"
        self.logger.info("Fetching repository data from %s", url)
        response = requests.get(url)

        if response.status_code == 200:
            self.repo_data = response.json()

        elif response.status_code == 404:
            self.logger.error("Repository not found: %s", self.repository)
            raise ValueError(f"Repository '{self.repository}' not found.")
        else:
            self.logger.error(
                "Failed to fetch repository data. Status code: %d",
                response.status_code,
            )
            raise ValueError(
                f"Repository '{self.repository}' could not be fetched."
            )

    def get_key_metrics(self) -> RepositoryMetrics:
        """
        Extract key metrics from the repository data and return a
        RepositoryMetrics object.
        """
        if not self.repo_data:
            raise RuntimeError("Repository data not fetched yet.")

        return RepositoryMetrics(
            stars=self.repo_data.get("stargazers_count", 0),
            forks=self.repo_data.get("forks_count", 0),
            last_push=datetime.fromisoformat(
                self.repo_data.get("pushed_at", "").replace("Z", "")
            ),
            open_issues=self.repo_data.get("open_issues_count", 0),
            archived=self.repo_data.get("archived", False),
        )
