import json
import os
from collections import OrderedDict

columns = [f"column{i+1}" for i in range(15)]


def load_fds(file_path: str) -> OrderedDict[str, list[list[str]]]:
    """
    Parses all FDs in a file into a dictionary of dependants to list of determinants
    """
    file = open(file_path, "r")
    lines = file.readlines()

    res: dict[str, list[list[str]]] = OrderedDict([(name, list()) for name in columns])
    for line in lines:
        j = json.loads(line)
        dependant = j["dependant"]["columnIdentifier"]
        dets = j["determinant"]["columnIdentifiers"]
        dets = list(map(lambda d: d["columnIdentifier"], dets))

        if res.get(dependant) is None:
            res[dependant] = [dets]
        else:
            res[dependant].append(dets)

    return res

def load_fd_list(file_path: str) -> OrderedDict[str, list[list[str]]]:
    """
    Parses all FDs in a file into a list of FDs
    """
    file = open(file_path, "r")
    lines = file.readlines()

    res: list[tuple[str, list[str]]] = []
    for line in lines:
        j = json.loads(line)
        dependant = j["dependant"]["columnIdentifier"]
        dets = j["determinant"]["columnIdentifiers"]
        dets = list(map(lambda d: d["columnIdentifier"], dets))
        res.append((dependant, dets))

    return res