# -*- coding: utf-8 -*-

import json
import importlib
import inspect
import pkgutil
import pprint
import subprocess
import select
import textwrap
import time

import click
import sys
import yaml

import plugin_formatter

from . import __version__ as VERSION
from .commands import CommandRepo
from .freckles_defaults import *
from nsbl import tasks
from nsbl.defaults import *
from .utils import get_all_adapters_in_repos, download_extra_repos, DEFAULT_FRECKLES_CONFIG, DEFAULT_ABBREVIATIONS


def output(python_object, format="raw", pager=False):
    if format == 'yaml':
        output_string = yaml.safe_dump(python_object, default_flow_style=False, encoding='utf-8', allow_unicode=True)
    elif format == 'json':
        output_string = json.dumps(python_object, sort_keys=4, indent=4)
    elif format == 'raw':
        output_string = str(python_object)
    elif format == 'pformat':
        output_string = pprint.pformat(python_object)
    else:
        raise Exception("No valid output format provided. Supported: 'yaml', 'json', 'raw', 'pformat'")

    if pager:
        click.echo_via_pager(output_string)
    else:
        click.echo(output_string)


@click.group(invoke_without_command=True)
@click.option('--version', help='the version of frkl you are using', is_flag=True)
@click.option("--use-repo", "-r", required=False, multiple=True, help="extra context repos to use")
@click.pass_context
def cli(ctx, version, use_repo):
    """Console script for nsbl"""

    if version:
        click.echo(VERSION)
        sys.exit(0)

    ctx.obj = {}
    ctx.obj["config"] = DEFAULT_FRECKLES_CONFIG
    if use_repo:
        download_extra_repos(ctx, None, use_repo)


@cli.command('log')
@click.option('--follow', '-f', help="follow the log file", is_flag=True, default=False)
@click.pass_context
def log_current(ctx, follow):
    """Prints out the last runs ansible log (verbose)"""

    last_run_folder = os.path.expanduser("~/.local/freckles/runs/current")
    last_run_log_folder = os.path.join(last_run_folder, "logs")

    ansible_log_file = os.path.join(last_run_log_folder, "ansible_run_log")

    if not follow:
        f = subprocess.Popen(['cat', ansible_log_file], shell=False)

    else:

        link_target = os.readlink(last_run_folder)

        f = None

        while True:

            if not os.path.exists(ansible_log_file):
                time.sleep(1)
                continue

            if not f:
                    f = subprocess.Popen(['tail','-F', ansible_log_file], shell=False)

            time.sleep(1)
            new_link_target = os.readlink(last_run_folder)
            if new_link_target != link_target:
                f.terminate()
                f = None
                link_target = new_link_target


@cli.command('debug-last')
@click.pass_context
def debug_last(ctx):
    """Re-runs the last freckle run directly using ansible-playbook and verbose output."""

    last_run_folder = os.path.expanduser("~/.local/freckles/runs/current")

    last_run_debug_folder = os.path.join(last_run_folder, "debug")
    last_run_debug_script = os.path.join(last_run_debug_folder, "debug_all_plays.sh")

    run_env = os.environ.copy()

    #proc = subprocess.Popen(last_run_debug_script, stdout=subprocess.PIPE, stderr=sys.stdout.fileno(),
    proc = subprocess.Popen(last_run_debug_script, stdin=subprocess.PIPE, shell=True, env=run_env)

    proc.communicate()
    # for line in iter(proc.stdout.readline, ''):
        # click.echo(line, nl=False)


def get_all_modules(module_name, module_list):

    # import ansible.modules
    module = importlib.import_module(module_name)

    prefix = module.__name__ + "."
    for importer, modname, ispkg in pkgutil.iter_modules(module.__path__, prefix):
        # print "Found submodule %s (is a package: %s)" % (modname, ispkg)
        if ispkg:
            get_all_modules(modname, module_list)
        else:
            module_list.append(modname)
        # module = __import__(modname, fromlist="dummy")
        # print "Imported", module

@cli.command('list-modules')
@click.option('--filter', '-f', help="filters module names containing this string", required=False, default=None)
@click.option('--details', '-d', help="print details about matching modules", required=False, default=False, is_flag=True)
@click.pass_context
def list_modules_cli(ctx, filter, details):
    """Lists all ansible modules."""

    module_list = []
    get_all_modules('ansible.modules', module_list)
    for m in module_list:

        if filter and filter not in m:
            continue

        short_name = m.split(".")[-1]
        try:
            module_metadata = read_module(m)

            if details:
                click.echo("{}:".format(short_name))
                dets = pprint.pformat(module_metadata)
                click.echo(dets)
            else:
                click.echo("{}: {}".format(short_name, module_metadata["doc"]["short_description"]))

        except (ImportError):
            click.echo("{}: {}".format(short_name, "n/a (probably because of missing python dependencies)"))

def list_modules():

    module_list = []
    get_all_modules('ansible.modules', module_list)
    return module_list

# @cli.command('get-module')
# @click.argument('module_name', nargs=1)
# @click.pass_context
# def get_module(ctx, module_name):

#     matches = [x for x in list_modules() if x.endswith(module_name)]

#     for m in matches:

#         path, name = m.rsplit('.',1)

#         module_info = read_module(m)

#         pprint.pprint(module_info["doc"]["options"])

#         # info_all = read_package(path)
#         # module_info = info_all[0][name]
#         # yaml_text = yaml.dump(module_info["doc"]["options"], default_flow_style=False)
#         # print yaml_text


def read_package(package_name):

    module = importlib.import_module(package_name)
    path = os.path.abspath(os.path.join(module.__file__, os.pardir))

    info = plugin_formatter.get_plugin_info(path)
    return info


def read_module(module_name):

    module = importlib.import_module(module_name)
    members = inspect.getmembers(module)

    doc_string = [x[1] for x in members if x[0] == "DOCUMENTATION"][0]
    examples_string = [x[1] for x in members if x[0] == "EXAMPLES"][0]

    doc = yaml.safe_load(doc_string)
    examples = yaml.safe_load(examples_string)

    return {"doc": doc, "examples": examples}

@cli.command("list-roles")
@click.option('--filter', '-f', help="filters module names containing this string", required=False, default=None)
@click.option('--readme', '-r', help="print readme of matching modules", required=False, default=False, is_flag=True)
@click.option('--defaults', '-d', help="print defaults file of matching modules", required=False, default=False, is_flag=True)
@click.pass_context
def list_roles_cli(ctx, filter, readme, defaults):

    config = ctx.obj["config"]

    repos = tasks.get_local_repos(config.trusted_repos, "roles", DEFAULT_LOCAL_REPO_PATH_BASE, DEFAULT_REPOS, DEFAULT_ABBREVIATIONS)

    click.echo("")
    click.echo("Available roles:")
    click.echo("")

    for repo in repos:
        for role, role_details in tasks.get_role_details_in_repo(repo).items():

            if filter and filter not in role:
                continue

            if readme:
                click.echo(role_details["readme"])
            else:
                click.echo(role)

            if defaults:
                click.echo("Defaults:\n")
                for key, value in role_details["defaults"].items():
                    click.echo("file '{}':".format(key))
                    yaml_string = yaml.dump(value, default_flow_style=False)
                    click.echo("   " + yaml_string.replace("\n", "\n   "))
                    click.echo("")


    click.echo("")

@cli.command("list-aliases")
@click.option("--filter", "-f", help="filter aliases contains the provided string", required=False, default=None)
@click.option('--details', '-r', help="print alias details", required=False, default=False, is_flag=True)
@click.pass_context
def list_aliases_cli(ctx, filter, details):

    config = ctx.obj["config"]
    role_repos = tasks.get_local_repos(config.trusted_repos, "roles", DEFAULT_LOCAL_REPO_PATH_BASE, DEFAULT_REPOS, DEFAULT_ABBREVIATIONS)

    task_descs = calculate_task_descs(None, role_repos, add_upper_case_versions=False)

    for d in task_descs:

        meta = d.get(TASKS_META_KEY, {})

        name = meta.get(TASK_META_NAME_KEY, "")
        task_name = meta.get(TASK_NAME_KEY, name)
        task_type = meta.get(TASK_TYPE_KEY, None)

        if not task_type:
            if "." in task_name:
                task_type = ROLE_NAME_KEY
            else:
                task_type = TASK_TASK_TYPE

        if filter and not filter in name:
            continue

        if not details:
            click.echo("{}: {} '{}'".format(name, task_type, task_name))
        else:
            # vars = d.get(VARS_KEY)

            click.echo("\nalias '{}' (type: {}):".format(name, task_type))
            yaml_string = yaml.safe_dump(d, default_flow_style=False, allow_unicode=True, encoding="utf-8")
            click.echo("   " + yaml_string.replace("\n", "\n    "))

if __name__ == '__main__':
    cli()
