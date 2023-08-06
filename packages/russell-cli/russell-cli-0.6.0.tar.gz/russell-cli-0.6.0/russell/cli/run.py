# coding: utf-8
from __future__ import print_function
import click
import sys

from russell.client.data import DataClient

try:
    from pipes import quote as shell_quote
except ImportError:
    from shlex import quote as shell_quote

from shutil import rmtree
from tabulate import tabulate
from time import sleep

from russell.cli.utils import (get_task_url, get_module_task_instance_id,
                               get_mode_parameter, wait_for_url, force_unicode,
                               get_files_in_directory, save_dir)
from russell.client.files import FsClient
from russell.client.experiment import ExperimentClient
from russell.client.module import ModuleClient
from russell.manager.auth_config import AuthConfigManager
from russell.manager.experiment_config import ExperimentConfigManager
from russell.constants import CPU_INSTANCE_TYPE, GPU_INSTANCE_TYPE, ENV_LIST, DEFAULT_ENV, DEFAULT_INSTANCE_TYPE
from russell.model.module import Module
from russell.model.experiment import ExperimentRequest
from russell.log import logger as russell_logger
import webbrowser



@click.command()
@click.option('--gpu/--cpu', default=False, help='Run on a gpu instance')
@click.option('--data',
              multiple=True,
              help='Data source id(s) to use')
@click.option('--mode',
              help='Different russell modes',
              default='job',
              type=click.Choice(['job', 'jupyter', 'serve']))
@click.option('--env',
              help='Environment type to use',
              type=click.Choice(sorted(ENV_LIST)))
@click.option('--message', '-m',
              help='Message to commit',
              type=click.STRING,
              default="")
@click.option('--tensorboard/--no-tensorboard',
              help='Run tensorboard')
@click.argument('command', nargs=-1)
@click.pass_context
def run(ctx, gpu, env, data, mode, command, message, tensorboard):
    """
    Run a command on Russell. Russell will upload contents of the
    current directory and run your command remotely.
    This command will generate a run id for reference.
    """
    if message and len(message) > 1024:
        russell_logger.error("Message body length over limit")
        sys.exit()

    success, data_ids = process_data_ids(data)
    if not success:
        sys.exit(2)

    _TEMP_DIR = '.russellCodeTemp'

    command_str = ' '.join(command)
    experiment_config = ExperimentConfigManager.get_config()

    access_token = AuthConfigManager.get_access_token()
    version = experiment_config.version

    # Gen temp dir
    try:
        upload_files, total_file_size_fmt, total_file_size = get_files_in_directory('.', 'code')
        save_dir(upload_files, _TEMP_DIR)
    except OSError:
        sys.exit("Directory contains too many files to upload. Add unused directories to .russellignore file.")
    russell_logger.info("Creating project run. Total upload size: {}".format(total_file_size_fmt))
    russell_logger.debug("Creating module. Uploading: {} files".format(len(upload_files)))

    # Create module
    module = Module(name=experiment_config.name,
                    description=message,
                    family_id=experiment_config.family_id,
                    version=version,
                    module_type="code",
                    entity_id=experiment_config.project_id)
    module_resp = ModuleClient().create(module)
    if not module_resp:
        russell_logger.error("Remote project does not existed")
        return
    version = module_resp.get('version')
    experiment_config.set_version(version=version)
    ExperimentConfigManager.set_config(experiment_config)

    module_id = module_resp.get('id')
    project_id = module_resp.get('entity_id')
    if not project_id == experiment_config.project_id:
        russell_logger.error("Project conflict")

    russell_logger.debug("Created module with id : {}".format(module_id))

    # Upload code to fs
    russell_logger.info("Syncing code ...")
    fc = FsClient()
    try:
        fc.socket_upload(file_type="code",
                         filename=_TEMP_DIR,
                         access_token=access_token.token,
                         file_id=module_id,
                         user_name=access_token.username,
                         data_name=experiment_config.name)
    except Exception as e:
        sys.exit(e)

    # rm temp dir
    rmtree(_TEMP_DIR)
    russell_logger.debug("Created code with id : {}".format(module_id))
    russell_logger.info("\nUpload finished")

    # Create experiment request
    instance_type = GPU_INSTANCE_TYPE if gpu else CPU_INSTANCE_TYPE
    experiment_request = ExperimentRequest(name=experiment_config.name,
                                           description=message,
                                           module_id=module_id,
                                           data_ids=data_ids,
                                           command=command_str,
                                           full_command=get_command_line(instance_type=instance_type,
                                                                         data=data,
                                                                         open_notebook=True,
                                                                         env=env,
                                                                         message=message,
                                                                         mode=mode,
                                                                         tensorboard=tensorboard,
                                                                         command_str=command_str
                                                                         ),
                                           mode=get_mode_parameter(mode),
                                           predecessor=experiment_config.experiment_predecessor,
                                           family_id=experiment_config.family_id,
                                           project_id=experiment_config.project_id,
                                           version=version,
                                           instance_type=instance_type,
                                           environment=env)
    experiment_id = ExperimentClient().create(experiment_request)
    russell_logger.debug("Created experiment : {}".format(experiment_id))

    # Update expt config including predecessor
    experiment_config.set_module_predecessor(module_id)
    experiment_config.set_experiment_predecessor(experiment_id)
    ExperimentConfigManager.set_config(experiment_config)
    experiment_name = "{}/{}:{}".format(access_token.username,
                                        experiment_config.name,
                                        version)

    table_output = [["RUN ID", "NAME", "VERSION"],
                    [experiment_id, force_unicode(experiment_name), version]]
    russell_logger.info(tabulate(table_output, headers="firstrow"))
    russell_logger.info("")

    if mode in ['jupyter', 'serve']:
        while True:
            # Wait for the experiment / task instances to become available
            try:
                experiment = ExperimentClient().get(experiment_id)
                if experiment.state != "waiting" and experiment.task_instances:
                    break
            except Exception as e:
                russell_logger.debug("Experiment not available yet: {}".format(experiment_id))

            russell_logger.debug("Experiment not available yet: {}".format(experiment_id))
            sleep(1)
            continue

        # Print the path to jupyter notebook
        if mode == 'jupyter':
            # jupyter_url = get_task_url(get_module_task_instance_id(experiment.task_instances))
            jupyter_url = get_task_url(experiment_id, gpu)
            print("Setting up your instance and waiting for Jupyter notebook to become available ...")
            if wait_for_url(jupyter_url, sleep_duration_seconds=2, iterations=900):
                russell_logger.info("\nPath to jupyter notebook: {}".format(jupyter_url))
                webbrowser.open(jupyter_url)
            else:
                russell_logger.info("\nPath to jupyter notebook: {}".format(jupyter_url))
                russell_logger.info("Notebook is still loading or can not be connected now. View logs to track progress")

        # Print the path to serving endpoint
        if mode == 'serve':
            russell_logger.info("Path to service endpoint: {}".format(
                get_task_url(get_module_task_instance_id(experiment.task_instances),gpu)))

    russell_logger.info("""
    To view logs enter:
        russell logs {}
            """.format(experiment_id))


def get_command_line(instance_type, env, message, data, mode, open_notebook, tensorboard, command_str):
    """
    Return a string representing the full floyd command entered in the command line
    """
    russell_command = ["russell", "run"]
    if instance_type and not instance_type == DEFAULT_INSTANCE_TYPE:
        russell_command.append('--' + instance_type)
    if env and not env == DEFAULT_ENV :
        russell_command += ["--env", env]
    if message:
        russell_command += ["--message", shell_quote(message)]
    if data:
        for item in data:
            russell_command += ["--data", item]
    if tensorboard:
        russell_command.append("--tensorboard")
    if not mode == "job":
        russell_command += ["--mode", mode]
        if mode == 'jupyter':
            if not open_notebook:
                russell_command.append("--no-open")
    else:
        if command_str:
            russell_command.append(shell_quote(command_str))
    return ' '.join(russell_command)


def validate_env(env, instance_type):
    # arch = instance_type
    # env_map = EnvClient().get_all()
    # envs = env_map.get(arch)
    # if envs:
    #     if env not in envs:
    #         russell_logger.error(
    #             "{} is not in the list of supported environments:\n{}".format(
    #                 env, tabulate([[env_name] for env_name in envs.keys()])))
    #         return False
    # else:
    #     russell_logger.error("invalid instance type")
    #     return False
    # return True
    pass


def process_data_ids(data):
    if len(data) > 5:
        russell_logger.error(
            "Cannot attach more than 5 datasets to a task")
        return False, None
    # Get the data entity from the server to:
    # 1. Confirm that the data id or uri exists and has the right permissions
    # 2. If uri is used, get the id of the dataset
    data_ids = []
    mc = ModuleClient()
    for data_id_and_path in data:
        if ':' in data_id_and_path:
            data_id, path = data_id_and_path.split(':')
        else:
            data_id = data_id_and_path
            path = None
        data_obj = mc.get(data_id)
        if not data_obj:
            russell_logger.error("Data not found forid: {}".format(data_id))
            return False, None
        else:
            if path is None:
                path = "{}-{}".format(data_obj.name, data_obj.version)
            data_ids.append("{id}:{path}".format(id=data_obj.id, path=path))

    return True, data_ids