from mimikopi_cli.lib import downloder


class App():
    def __init__(self) -> None:
        self.__downloader = downloder.Downloder()

    def dl(self) -> None:
        self.__downloader.dl()
