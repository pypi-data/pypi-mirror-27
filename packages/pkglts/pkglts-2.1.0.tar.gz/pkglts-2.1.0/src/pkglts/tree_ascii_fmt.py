# coding: utf-8

from os import listdir
from os.path import isdir
from os.path import join as pj

from pkglts.config_management import Config


def nn(cfg, pth):
    tgt_name = cfg.render(pth)
    if tgt_name.endswith(".tpl"):
        tgt_name = tgt_name[:-4]

    return tgt_name


def tree(dname, padding, txt):
    pkg_cfg = dict(base={"namespace": None,
                         "owner": "owner",
                         "pkgname": "pkgname",
                         "url": None})

    cfg = Config(pkg_cfg)

    files = [(isdir(pj(dname, fname)), fname) for fname in listdir(dname)]
    files.sort()

    count = 0
    for is_dir, fname in files:
        count += 1
        txt += padding + '|\n'
        fmt_name = nn(cfg, fname)
        txt += padding + '+-' + fmt_name
        path = pj(dname, fname)
        if is_dir:
            txt += "/\n"
            if count == len(files):
                txt = tree(path, padding + ' ' + ' ' * int(len(fmt_name) / 2), txt)
            else:
                txt = tree(path, padding + '|' + ' ' * int(len(fmt_name) / 2), txt)
        else:
            txt += '\n'

    return txt


def fmt_tree(dname):
    return tree(dname, '', ".\n")
