import fire

from mimikopi_cli.app import App


def main() -> None:
    app = App()
    fire.Fire(app)
