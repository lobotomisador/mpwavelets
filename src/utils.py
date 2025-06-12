import os
import pandas as pd
import numpy as np
import json
import copy
import shutil
import re
import subprocess
from scipy.optimize import curve_fit
from pathlib import Path
from pandas import read_csv, DataFrame, Series, set_option
from dataclasses import dataclass, field
from abc import ABC, abstractmethod, abstractproperty
from typing_extensions import TypeAlias
from enum import Enum
from scipy.stats.mstats import gmean


def find_folders(folder: Path, *, ignore_hidden=True, return_sorted=True):
    return find_files(
        folder,
        folders_only=True,
        ignore_hidden=ignore_hidden,
        return_sorted=return_sorted,
    )


def find_files(
    folder: Path,
    *,
    folders_only=False,
    files_only=False,
    ignore_hidden=True,
    only_yml=False,
    only_csv=False,
    return_sorted=True,
    filetype: str = None,
):
    all_files_or_dirs = os.listdir(folder)
    filters = []
    if files_only:
        filters.append(lambda f: os.path.isfile(os.path.join(folder, f)))

    if folders_only:
        filters.append(lambda f: not os.path.isfile(os.path.join(folder, f)))

    if ignore_hidden:
        filters.append(lambda f: not f.startswith("."))

    if only_yml:
        filters.append(lambda f: ".yml" in f)

    if only_csv:
        filters.append(lambda f: ".csv" in f)

    if filetype is not None:
        filters.append(lambda f: filetype in f)

    files = list(
        filter(
            lambda file_or_dir: all(fil(file_or_dir) for fil in filters),
            all_files_or_dirs,
        )
    )
    if return_sorted:
        files = sorted(files)

    return files
