import fishtrace_engine
import typer

from fishtrace_cli import __version__

app = typer.Typer(name="fishtrace", help="FishTrace email forensics command line interface")


@app.command()
def version() -> None:
    typer.echo(f"FishTrace CLI {__version__} (engine {fishtrace_engine.__version__})")


@app.command()
def status() -> None:
    typer.echo("FishTrace foundation is installed. Analysis commands are added in later milestones.")


if __name__ == "__main__":
    app()
