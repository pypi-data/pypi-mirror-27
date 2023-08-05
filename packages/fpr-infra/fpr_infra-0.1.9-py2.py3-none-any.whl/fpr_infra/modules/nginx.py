# coding: utf-8

from pyinfra.api import deploy
from pyinfra.modules import files
from fpr_infra import pyinfra


@deploy("Enable nginx application configuration")
def enable_conf(state, host, conf_file, dest=None, src_dir=None):
    dest = dest or conf_file
    src_dir = src_dir or state.deploy_dir
    pyinfra.move(
        state, host,
        f"{src_dir}/files/nginx/{conf_file}", f"/etc/nginx/sites-available/{dest}",
        sudo=True
    )
    if not host.fact.link(f"/etc/nginx/sites-available/{dest}"):
        files.link(
            state, host,
            {f"Enable {conf_file} site on http"},
            f"/etc/nginx/sites-enabled/{conf_file}", f"/etc/nginx/sites-available/{dest}",
            sudo=True
        )
