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

"""
Cli runner.
"""
import csv
from typing import Optional
import typer
from typer.cli import app
from src.github_repository import GitHubRepository
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from src import NAME


@app.command()
def filter_unmaintained(
    repositories: str = typer.Option(
        ..., "--repositories", help="Path to the input repositories CSV file."
    ),
    output: str = typer.Option(
        ..., "--output", help="Path to the output CSV file."
    ),
    api_key: str = typer.Option(
        ..., "--key", help="Your API key to access LLM."
    ),
    model: str = typer.Option(
        "GigaChat", "--model", help="Name of Gigachat Model"
    ),
):
    """
    Filter repositories to identify maintained ones.
    """
    try:
        maintained_repos = []

        # Read the input CSV file
        with open(repositories, mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                repository = row["full_name"]

                # Call is_maintained for each repository
                maintained = is_maintained(repository, model, api_key).lower()
                if maintained == "yes":
                    maintained_repos.append(row)

        # Write the maintained repositories to the output CSV file
        with open(output, mode="w", encoding="utf-8", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(maintained_repos)

        typer.echo(f"Filtered repositories written to {output}")

    except Exception as e:
        typer.echo(f"An unexpected error occurred: {e}")


@app.command()
def is_maintained(
    repository: str = typer.Option(
        ..., "--repository", help="GitHub repository name (e.g., 'owner/repo')"
    ),
    model: str = typer.Option(
        "GigaChat", "--model", help="Name of Gigachat Model"
    ),
    api_key: str = typer.Option(
        ..., "--key", help="your api key to access llm"
    ),
):
    """
    Decides whether the repository is maintained or not.
    """
    try:
        # Initialize the GitHubRepository class
        github_repo = GitHubRepository(repository)

        # Fetch repository data
        github_repo.fetch_repository_data()

        # Extract metrics
        metrics = github_repo.get_key_metrics()

        # Log details for debugging
        typer.echo(
            f"Metrics: Stars={metrics.stars}, Forks={metrics.forks}, "
            f"Last Push={metrics.last_push}, "
            f"Open Issues={metrics.open_issues}, "
            f"Archived={metrics.archived}"
        )

        # Analyze and decide maintenance status

        # GigaChat initialization
        llm = GigaChat(
            credentials=api_key,
            # Replace with your auth key
            scope="GIGACHAT_API_PERS",
            model=str(model),
            verify_ssl_certs=False,
            streaming=False,
        )

        # System prompt for GigaChat
        system_message = SystemMessage(
            content=(
                "You are an AI assistant that analyzes GitHub repositories"
                "to determine if they are maintained."
                "You will use the following metrics:"
                "stars, forks, last push date, open issues,"
                "and archived status."
                'Respond "yes" if the repository is maintained '
                'and "no" otherwise.'
                "Do not provide any justifications, just single word"
            )
        )

        # Human prompt with repository metrics
        user_message = HumanMessage(
            content=(
                f"Here are the repository metrics:\n"
                f"- Stars: {metrics.stars}\n"
                f"- Forks: {metrics.forks}\n"
                f"- Last Push: {metrics.last_push}\n"
                f"- Open Issues: {metrics.open_issues}\n"
                f"- Archived: {metrics.archived}\n\n"
                f"Is the repository maintained?"
            )
        )

        # GigaChat invocation
        messages = [system_message, user_message]
        response = llm.invoke(messages)

        # Log and display the response
        typer.echo(f"is {repository} maintained?: {response.content}")
        return response.content

    except ValueError as ve:
        typer.echo(str(ve))
    except Exception as e:
        typer.echo(f"An unexpected error occurred: {e}")


# Run it.
@app.callback()
def main(
    # pylint: disable=unused-argument
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        help="Show the application's version and exit.",
        is_eager=True,
    )
) -> None:
    f"""
    {NAME}
    """
    return
