import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

from src.github_repository import RepositoryMetrics, GitHubRepository


def test_days_since_last_push():
    last_push = datetime.utcnow() - timedelta(days=10)
    metrics = RepositoryMetrics(
        stars=10, forks=5, last_push=last_push, open_issues=3, archived=False
    )
    assert metrics.days_since_last_push == 10


@patch("src.github_repository.requests.get")
def test_fetch_repository_data_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "stargazers_count": 42,
        "forks_count": 10,
        "pushed_at": "2024-12-15T12:00:00Z",
        "open_issues_count": 5,
        "archived": False,
    }
    mock_get.return_value = mock_response

    repo = GitHubRepository("owner/repo")
    repo.fetch_repository_data()

    assert repo.repo_data is not None
    assert repo.repo_data["stargazers_count"] == 42


@patch("src.github_repository.requests.get")
def test_fetch_repository_data_not_found(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    repo = GitHubRepository("owner/nonexistent")

    with pytest.raises(ValueError):
        repo.fetch_repository_data()


@patch("src.github_repository.requests.get")
def test_fetch_repository_data_other_error(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    repo = GitHubRepository("owner/repo")

    with pytest.raises(ValueError):
        repo.fetch_repository_data()


def test_get_key_metrics_success():
    repo = GitHubRepository("owner/repo")
    repo.repo_data = {
        "stargazers_count": 42,
        "forks_count": 10,
        "pushed_at": "2024-12-15T12:00:00Z",
        "open_issues_count": 5,
        "archived": False,
    }

    metrics = repo.get_key_metrics()

    assert metrics.stars == 42
    assert metrics.forks == 10
    assert metrics.open_issues == 5
    assert not metrics.archived
    assert metrics.last_push == datetime(2024, 12, 15, 12, 0, 0)


def test_get_key_metrics_not_fetched():
    repo = GitHubRepository("owner/repo")

    with pytest.raises(RuntimeError):
        repo.get_key_metrics()
