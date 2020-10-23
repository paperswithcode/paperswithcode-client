import typer

from tea_console.commands.config import app as config_app


app = typer.Typer(name="pwc", help="PapersWithCode client.")

# Add tea-console apps
app.add_typer(config_app)
