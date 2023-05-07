from rich import print
from typer import Typer

app = Typer()


@app.command()
def describe():
    from damnit_knockoff.context_reader import MODELS

    for model in MODELS:
        schema = model.schema()
        print(schema)


@app.command()
def test(proposal: int, path: str, run: int):
    """Make requests via HTTPX"""
    import httpx

    with httpx.Client() as client:
        res = client.post(
            "http://localhost:8000/trigger",
            json={"proposal": proposal, "path": path, "run": run},
        )
        print(res.json())


if __name__ == "__main__":
    app()
