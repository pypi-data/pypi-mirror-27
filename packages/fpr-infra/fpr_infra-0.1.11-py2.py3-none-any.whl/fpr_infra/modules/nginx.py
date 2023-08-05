# coding: utf-8

from pyinfra.api import deploy
from pyinfra.modules import files, server
from fpr_infra import pyinfra


@deploy("Enable nginx application configuration")
def enable_conf(state, host, conf_file, dest=None):
    dest = dest or conf_file

    # set available conf
    if host.fact.file(f"/etc/nginx/sites-available/{dest}"):
        server.shell(
            state, host,
            f"rm /etc/nginx/sites-available/{dest}",
            sudo=True
        )
    pyinfra.move(
        state, host,
        conf_file, f"/etc/nginx/sites-available/{dest}",
        sudo=True
    )

    # set available conf as enabled
    if host.fact.file(f"/etc/nginx/sites-enabled/{dest}"):
        server.shell(
            state, host,
            f"rm /etc/nginx/sites-enabled/{dest}",
            sudo=True
        )
    files.link(
        state, host,
        {f"Enable {dest} site on http"},
        f"/etc/nginx/sites-enabled/{dest}", f"/etc/nginx/sites-available/{dest}",
        sudo=True
    )
