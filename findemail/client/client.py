from . import (
    ClientBase, SearchMethods, UsersMethods
)


class Client(
    ClientBase, SearchMethods, UsersMethods
):
    pass
