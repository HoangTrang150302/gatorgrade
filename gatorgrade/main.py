"""Use Typer to run gatorgrade to run the GatorGrader checks."""

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown

from gatorgrade.input.parse_config import parse_config
from gatorgrade.output.output import run_checks
from gatorgrade.util import github
from gatorgrade.util import versions

# define constants used in this module
DEFAULT_VERSION = False
GATORGRADE_EMOJI_RICH = ":crocodile:"
FILE = "gatorgrade.yml"
FAILURE = 1
RICH_MARKUP_MODE_DEFAULT = "markdown"

# define the overall help message
help_message_markdown = f"""
{GATORGRADE_EMOJI_RICH} GatorGrade runs the GatorGrader checks in a specified configuration file.
"""

# create a Typer app that:
# --> does not support completion
# --> has a specified help message with an emoji for tagline
# --> uses "markdown" mode so that markdown and emojis work
app = typer.Typer(
    add_completion=False,
    help=help_message_markdown,
    rich_markup_mode=RICH_MARKUP_MODE_DEFAULT,
)

# create a default console for printing with rich
console = Console()


@app.callback(invoke_without_command=True)
def gatorgrade(
    ctx: typer.Context,
    filename: Path = typer.Option(FILE, "--config", "-c", help="Name of the YML file."),
    version: bool = typer.Option(
        DEFAULT_VERSION, "--version", "-v", help="Display version information."
    ),
):
    """Run the GatorGrader checks in the specified configuration file."""
    # if ctx.subcommand is None then this means
    # that, by default, gatorgrade should run in checking mode
    if ctx.invoked_subcommand is None:
        # requesting version information overrides all other commands;
        # if the version details are requested, print them and exit
        if version:
            # define the version label with suitable emoji
            version_label = ":wrench: Version information:"
            # define the message about the project versions
            version_message = versions.get_project_versions()
            # define a contribution message with suitable emoji
            contribution_message = (
                ":tada: Want to contribute to this project? Check these GitHub sites!"
            )
            # define the message about GitHub repositories
            github_message = github.get_github_projects()
            # output all of the details about gatorgrade
            # 1) standard help message that was defined previously
            console.print(help_message_markdown)
            # 2) version message
            console.print(version_label)
            console.print(Markdown(version_message))
            console.print()
            # 3) contribution message
            console.print(contribution_message)
            console.print(Markdown(github_message))
            console.print()
        # run the checking function since --version was not provided
        else:
            # parse the provided configuration file
            checks = parse_config(filename)
            # there are valid checks and thus the
            # tool should run them with run_checks
            if len(checks) > 0:
                checks_status = run_checks(checks)
            # no checks were created and this means
            # that, most likely, the file was not
            # valid and thus the tool cannot run checks
            else:
                checks_status = False
                console.print()
                console.print(
                    f"The file {filename} either does not exist or is not valid."
                )
                console.print("Exiting now!")
                console.print()
            # at least one of the checks did not pass or
            # the provided file was not valid and thus
            # the tool should return a non-zero exit
            # code to designate some type of failure
            if checks_status is not True:
                sys.exit(FAILURE)


# @app.command()
# def generate(
#     root: Path = typer.Argument(
#         Path("."),
#         help="Root directory of the assignment",
#         exists=True,
#         dir_okay=True,
#         writable=True,
#     ),
#     paths: List[Path] = typer.Option(
#         ["*"],
#         help="Paths to recurse through and generate checks for",
#         exists=False,
#     ),
# ):
#     """Generate a gatorgrade.yml file."""
#     targets = []
#     for path in paths:
#         targets.extend(glob.iglob(path.as_posix(), recursive=True))
#     generate_config(targets, root.as_posix())


if __name__ == "__main__":
    app()
