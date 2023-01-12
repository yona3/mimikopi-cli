from mimikopi_cli.lib import downloder, splitter


class App:
    def __init__(self) -> None:
        self.__downloader = downloder.Downloder()
        self.__splitter = splitter.Splitter()

    def dl(self) -> None:
        self.__downloader.dl()

    def sp(self, mode: int = 5) -> None:
        self.__splitter.sp(mode=mode)
