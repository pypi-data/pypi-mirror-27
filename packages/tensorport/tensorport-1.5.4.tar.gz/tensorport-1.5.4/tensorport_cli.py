import six
import json
import os
import sys
import webbrowser
import py
import click
import git
import logging
import click_log
import functools
import time

from tensorport import TensorportClient, MATRIX_URL
from terminaltables import SingleTable
from version import VERSION
from utils import random_name_generator, normalize, normalize_string, select_valid_index, render_table, tokenize_repo, question, info, option, time_limit_validator, repo_name_validator, \
    job_name_validator, select_repo, describe, select_job, \
    select_valid_integer, get_current_version
from tf_runner import run_tf

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME_DIR = os.getcwd()
logger = logging.getLogger(__name__)


class Config(dict):
    def __init__(self, *args, **kwargs):
        self.config = py.path.local(
            click.get_app_dir('tensorport')).join('config.json')

        self.home = HOME_DIR

        super(Config, self).__init__(*args, **kwargs)

    def load(self):
        """load the JSON config file from disk"""
        try:
            self.update(json.loads(self.config.read()))
            # logger.info('Config file loaded.')
        except py.error.ENOENT:
            # logger.error('Cannot Load Config File')
            pass

    def save(self):
        self.config.ensure()
        with self.config.open('w') as f:
            f.write(json.dumps(self))
            # logger.info('Saving Tensorport Config File')

    def delete(self):
        self.config.ensure()
        self.config.remove()


# Bunch of global messages
global_config = Config()
global_config.__init__()
global_config.load()
if global_config.get('username') is None:
    owner_help_message = 'Specify owner by usernames'
else:
    owner_help_message = 'Specify owner by username, default: %s' % global_config.get(
        'username')


def authenticate():
    def decorator(f):

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                config = args[0]
            except:
                config = Config()
                config.__init__()
                config.load()

            username = config.get('username')
            token = config.get('token')
            if username == '' or token == '':
                print("You are not logged in yet. Use 'tport login'.")
                return
            return f(*args, **kwargs)

        return wrapper

    return decorator


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=VERSION)
@pass_config
def cli(config):
    """
    Welcome to TensorPort Command Line Interface.
    """
    config.load()
    click.echo()


@cli.group()
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
def get(config):
    """
    < project(s) | dataset(s) | job(s) | events >
    """
    pass


@cli.group()
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
def create(config):
    """
    < project | dataset | job >
    """
    pass


@cli.group()
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
def delete(config):
    """
    < project | dataset >
    """
    pass


@cli.command()
@click.option('--username', '-u', prompt=True)
@click.option('--password', '-p', prompt=True, hide_input=True)
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
def login(config, username, password):
    """
    Log into TensorPort
    """

    # Version Check
    if not get_current_version():
        click.echo(info("There is an updated version in PYPI - please run pip install tensorport --upgrade"))
        return

    client = TensorportClient()
    user, message = client.api_login(username, password)
    if user is not None:
        # Save Token and Username in Config File
        config['token'] = client.token
        config['git_token'] = client.git_token
        config['username'] = username
        config['password'] = password
        if user['first_name'] != '':
            config['first_name'] = user['first_name']
        else:
            config['first_name'] = username

        config.save()
        click.echo(info("Welcome %s! \nYour last login was on %s" %
                        (config['first_name'], user['last_login'])))

        return client.token
    else:
        click.echo(info("Login Failed! %s" % message))
        return


@cli.command()
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def logout(config):
    """
    Log out from TensorPort
    """

    if click.confirm("%s, Are you sure you want to log out?" %
                             (config.get('first_name'))):
        config.delete()
    pass


@cli.command()
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
def matrix(config):
    """
    Open Matrix in your browser
    """
    client = TensorportClient(
        token=config.get('token'), username=config.get('username'))
    click.echo(info("Entering Matrix: %s") % MATRIX_URL)
    client.open_dashboard()


@click.command()
@click.option(
    '--owner', default=global_config.get('username'), help=owner_help_message)
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def get_jobs(config, owner):
    """
    List jobs
    """
    # TODO: filter by owner name is not working
    client = TensorportClient(
        token=config.get('token'), username=config.get('username'))
    running_jobs = client.get_jobs(params={'owner': owner})
    if running_jobs:
        click.echo(info('List of %s jobs:' % (owner)))
        data = []
        data.append(['#', 'Job', 'Project', 'Status', 'Launched at'])

        i = 0
        valid_jobs = []
        for job in running_jobs:
            try:
                data.append([
                    i,
                    '%s/%s' % (job.get('owner'), job.get('display_name')),
                    '%s/%s:%s' %
                    (job.get('repository_owner'), job.get('repository_name'),
                     job.get('git_commit_hash')[:8]),
                    job.get('status'),
                    '' if job.get('launched_at') is None else job.get(
                        'launched_at')[:-5]
                ])
                i += 1
                valid_jobs.append(job)
            except:
                pass
        table = render_table(data, 36)
        click.echo(table.table)
        return running_jobs
    else:
        click.echo(info("You don't seem to have any jobs yet. Try tport create job to make one."))
        return


get.add_command(get_jobs, 'jobs')


@cli.command()
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def pulse(config):
    """
    Get status of jobs
    """
    # TODO: show resources for each job
    client = TensorportClient(
        token=config.get('token'), username=config.get('username'))
    running_jobs = client.get_jobs()  # TODO Check running job parameter
    if running_jobs:
        click.echo(info('Jobs:'))
        data = []
        data.append(['#', 'Job', 'Project', 'Status', 'Launched at'])

        i = 0
        valid_jobs = []
        for job in running_jobs:
            try:
                data.append([
                    i,
                    '%s/%s' % (job.get('owner'), job.get('display_name')),
                    '%s/%s:%s' %
                    (job.get('repository_owner'), job.get('repository_name'),
                     job.get('git_commit_hash')[:8]),
                    job.get('status'),
                    '' if job.get('launched_at') is None else job.get(
                        'launched_at')[:-5]
                ])
                i += 1
                valid_jobs.append(job)
            except:
                pass
        table = render_table(data, 36)
        click.echo(table.table)
        return running_jobs
    else:
        click.echo(info("You don't seem to have any jobs yet. Try 'tport create job' to make one."))
        return


@cli.command()
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def watch(config):
    """
    Shortcut for tport get events --watch
    """
    client = TensorportClient(
        token=config.get('token'), username=config.get('username'))
    while True:
        events = client.get_events()
        if events:
            data = [['Time', 'Job', 'Status', 'Event']]

            for e in events:
                try:
                    data.append([
                        e.get('created_at')[:19],
                        e.get('job_name'),
                        e.get('event_level_display'),
                        e.get('event_type_display')
                    ])
                except:
                    pass
            table = render_table(data, 54)
            os.system("printf '\033c'")
            click.echo(table.table)
            time.sleep(1)
        else:
            click.echo("Failed to query recent events. Perhaps you have not started a job yet. Try 'tport run'.")
            return None


@click.command()
@click.option('--link', is_flag=True, default=False, help='Link current git repository to an existing project.')
@click.option('--name')
@click.option('--description', default='')
@click.option('--repo-path', default=HOME_DIR)
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def create_project(config,
                   name=None,
                   description='',
                   repo_path=HOME_DIR,
                   link=False):
    """
    Create or link a project
    """
    client = TensorportClient(
        token=config.get('token'), username=config.get('username'))

    # Get Existing Repo
    # Check if repo exists:
    try:
        repo = git.Repo(repo_path)
    except git.InvalidGitRepositoryError:
        click.echo(info(
            "Couldn't find a git repository. Please run this command in a valid repository or provide a valid repo-path."))
        return

    if link:
        projects = client.get_projects(
            writer=config.get('username'))  # TODO: must fix, currently we only support owned projects, it should change to return all projects with writer access
        if projects:
            username, project_name = select_repo(projects, 'project')
            project = client.get_project(project_name, username=username)
            six.print_("Linking project %s " % project_name, end='')
        else:
            click.echo(
                info("It doesn't look like you have any projects yet. You can make a new one with 'tport create project'."))
    else:
        valid = False
        if name is None:
            name = click.prompt(text=question("Choose a valid project name"))
            valid, message = repo_name_validator(name, config)

        while not valid:
            valid, message = repo_name_validator(name, config)
            if valid:
                break
            else:
                name = click.prompt(text=question(
                    "Choose a valid project name, (%s)" % message))
        username = config.get('username')
        project_name = client.create_project(name, description)
        six.print_("Creating project (it may take a few minutes) %s " %
                   project_name, end='')

    # Check if we got repo created
    try:
        try:
            trial = 0
            while trial < 120:
                try:
                    project = client.get_project(project_name, username)
                    git_url = project.get('git_auth_link')
                    if len(git_url) > 0:
                        project_url = git_url
                        six.print_('\n', end='')
                        break
                except KeyboardInterrupt:
                    print('Interrupted!')
                    return
                except:
                    pass
                six.print_('.', end='')
                sys.stdout.flush()
                time.sleep(1)
                trial += 1
            if len(git_url) == 0:
                click.echo(
                    info("Failed to get git remote. Please contact TensorPort for support."))
                return
        except KeyboardInterrupt:
            print('Interrupted!')
    except:
        click.echo(
            info("Failed to get git remote. Please contact TensorPort for support."))
        return

    # Set current project
    config['current_project'] = project_name
    config['current_project_name'] = project.get('name')
    config.save()

    click.echo(info("Project %s/%s created successfully." % (username, project_name)))
    click.echo(info("Adding tensorport remote"))
    # Add check to add new remote
    try:
        origin = repo.create_remote('tensorport', project_url)
    except Exception as e:
        click.echo(info(
            "This repository already has a tensorport remote."))
        click.echo(info(
            "You can delete the remote using 'git remote remove tensorport' and link this repository using tport create project --link"))
        return

    click.echo(info("Project %s/%s is created.\nMatrix: %s\n" % (username,
                                                                 project_name,
                                                                 '%s/%s/%s' % (MATRIX_URL, username, project_name))))

    click.echo(
        info("Push the code to tensorport using 'git push tensorport master'"))
    return project_url


create.add_command(create_project, 'project')


@click.command()
@click.option('--link', is_flag=True, default=False, help='Link current git repository to an existing project.')
@click.option('--name')
@click.option('--description', default='')
@click.option('--repo-path', default=HOME_DIR)
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def create_dataset(config,
                   name,
                   description='Tensorport Dataset',
                   repo_path=HOME_DIR,
                   link=False):
    """
    Create or link a dataset
    """
    client = TensorportClient(
        token=config.get('token'), username=config.get('username'))

    # Get Existing Repo
    # Check if repo exists:
    try:
        repo = git.Repo(repo_path)
    except git.InvalidGitRepositoryError:
        click.echo(info(
            "Couldn't find a git repository. Please run this command in a valid repository or provide a valid repo-path."))
        return

    if link:
        datasets = client.get_datasets(
            writer=config.get('username'))  # TODO: must fix
        if datasets:
            username, dataset_name = select_repo(datasets, 'dataset')
            dataset = client.get_dataset(dataset_name, username=username)
            six.print_("Linking dataset %s " % dataset_name, end='')
        else:
            click.echo(
                info("It doesn't look like you have any datasets yet. You can create a new one with 'tport create dataset'."))
    else:
        valid = False
        if name is None:
            name = click.prompt(text=question("Choose a valid dataset name"))
            valid, message = repo_name_validator(name, config)

        while not valid:
            valid, message = repo_name_validator(name, config)
            if valid:
                break
            else:
                name = click.prompt(text=question(
                    "Choose a valid dataset name, (%s)" % message))

        username = config.get('username')
        dataset_name = client.create_dataset(name, description)
        six.print_("Creating dataset (it may take a few minutes) %s " %
                   dataset_name, end='')

    # Check if we got repo created
    try:
        trial = 0
        while trial < 120:
            try:
                dataset = client.get_dataset(dataset_name, username)
                git_url = dataset.get('git_auth_link')
                if len(git_url) > 0:
                    dataset_url = git_url
                    six.print_('\n', end='')
                    break
            except KeyboardInterrupt:
                print('Interrupted!')
                return
            except:
                pass
            six.print_('.', end='')
            sys.stdout.flush()
            time.sleep(1)
            trial += 1
        if len(git_url) == 0:
            click.echo(
                info("Failed to get git remote. Please contact TensorPort for support."))
            return
    except:
        click.echo(
            info("Failed to get git remote. Please contact TensorPort for support."))
        return

    # Set current dataset
    config['current_dataset'] = dataset_name
    config['current_dataset_name'] = dataset.get('name')
    config.save()

    click.echo(info("Dataset %s/%s created successfully." % (username, dataset_name)))
    click.echo(info("Adding tensorport remote"))

    # Add check to add new remote
    try:
        origin = repo.create_remote('tensorport', dataset_url)
    except Exception as e:
        click.echo(info(
            "This repository already has a TensorPort remote."))
        click.echo(info(
            "You can delete the remote using 'git remote remove tensorport' and link this repository using tport create dataset --link"))
        return

    click.echo(info("Dataset %s/%s is linked.\nMatrix: %s\n" % (username,
                                                                dataset_name,
                                                                '%s/%s/%s' % (MATRIX_URL, username, dataset_name))))
    click.echo(
        info("Push the code to TensorPort using 'git push tensorport master'"))
    return dataset_url


create.add_command(create_dataset, 'dataset')


@click.command()
@click.option('--name', help="Project name, e.g. tensorport/mnist", prompt='Project name')
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def get_project(config, name):
    """
    Get information about a project
    """
    client = TensorportClient(
        token=config.get('token'), username=config.get('username'))
    username, project_name, _ = tokenize_repo(name)

    project = client.get_project(project_name, username=username)
    if project:
        click.echo(info("Project: %s | ID: %s" % (project.get('name'),
                                                  project.get('id'))))
        return project
    else:
        click.echo(info("Project not found"))


get.add_command(get_project, 'project')


# TODO


@click.command()
@click.option('--job-id', help="Job id")
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def get_job(config, job_id=None):
    """
    Get information about a job
    """
    client = TensorportClient(
        token=config.get('token'), username=config.get('username'))
    if job_id is None:
        jobs = client.get_jobs()
        if jobs:
            job_id, job_name = select_job(jobs, 'Select the job')
        else:
            click.echo(
                info(
                    "You do not seem to have any jobs yet. You can make a new one with 'tport create job'."
                ))
            return

    job = client.get_job(params={'job_id': job_id})
    params = job.get('parameters')
    job_dict = {'name': '%s/%s' % (job.get('owner'), job.get('display_name')),
                'project': '%s/%s:%s' % (job.get('repository_owner'), job.get('repository_name'), job.get('git_commit_hash')),
                'status': job.get('status'),
                'job id': job.get('job_id'),
                'time (minutes)': params['time_limit'],
                'worker type': params['worker_type'],
                'parameter server type': params['ps_type'],
                'tensorflow version': params['tf_version'],
                'module': params['module'],
                'package_path': params['package_path'],
                'requirements': params['requirements'],
                'instance_type': params['instance_type'],
                'mode': params['mode'],
                'worker replicas': params['worker_replicas'],
                'parameter server replicas': params['ps_replicas'],
                'data repositories': ','.join(['%s/%s:%s' % (d['url'].strip('/').split('/')[-2], d['url'].strip('/').split('/')[-1], d['hash']) for d in params['data_repos']]),
                'code repository': '%s/%s:%s' % (params['code_repo']['url'].strip('/').split('/')[-2], params['code_repo']['url'].strip('/').split('/')[-1], params['code_repo']['hash']),
                }
    describe(job_dict)


get.add_command(get_job, 'job')


@click.command()
@click.option('--owner')
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def get_projects(config, owner=None):
    """
    List projects
    """
    # TODO: fix owner
    client = TensorportClient(
        token=config.get('token'), username=config.get('username'))

    projects = client.get_projects()

    if projects:
        click.echo(info("All projects:"))
        data = []
        data.append(
            ['#', 'Project', 'Created at', 'Description'])

        i = 0
        for project in projects:
            try:
                data.append([
                    i,
                    "%s/%s" % (project.get('owner')
                               ['username'], project.get('name')),
                    project.get('created_at')[:19],
                    project.get('description')
                ])
                i += 1
            except:
                pass
        table = render_table(data, 36)
        click.echo(table.table)
        return projects
    else:
        click.echo(info(
            "No projects found. Use 'tport create project' to start a new one."))
        return None


get.add_command(get_projects, 'projects')


@click.command()
@click.option('--name', help="Project name, e.g. tensorport/mnist")
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def delete_project(config, name):
    """
    Delete a project
    """
    # TODO: fix owner
    try:
        client = TensorportClient(
            token=config.get('token'), username=config.get('username'))
        try:
            if name is not None:
                username, project_name, _ = tokenize_repo(name)
                project = client.get_project(project_name, username=username)
            else:
                project = None

            if project:
                click.confirm('Do you want to delete project %s/%s?' %
                              (username, project_name), abort=True)
                project = client.delete_project(project_name, username)
                click.echo(info("Project %s/%s deleted" %
                                (username, project_name)))
            else:
                projects = client.get_projects(owner=True)
                if projects:
                    click.echo(question("Select a project to delete"))
                    data = []
                    data.append(
                        ['#', 'Project', 'Modified at', 'Description'])

                    i = 0
                    valid_projects = []
                    for project in projects:
                        try:
                            data.append([
                                i,
                                "%s/%s" % (project.get('owner')
                                           ['username'], project.get('name')),
                                project.get('modified_at')[:19],
                                project.get('description')
                            ])
                            i += 1
                            valid_projects.append(project)
                        except:
                            pass
                    table = render_table(data, 36)
                    click.echo(table.table)
                    project_to_delete_id = select_valid_index(
                        0,
                        len(valid_projects) - 1,
                        question('Select the project you want to delete.'))
                    project_name = valid_projects[project_to_delete_id].get(
                        'name')
                    username = valid_projects[project_to_delete_id].get('owner')[
                        'username']
                    click.confirm('Do you want to delete project %s/%s?' %
                                  (username, project_name), abort=True)
                    project = client.delete_project(project_name, username)
                    click.echo(info("Project %s/%s deleted" %
                                    (username, project_name)))
                else:
                    click.echo(info("You don't seem to have any projects to delete."))
                    return
        except:
            click.echo(info("Couldn't delete the project."))
            return
    except Exception as e:
        logger.error("Failed to run 'tport delete project'", exc_info=True)
        return


delete.add_command(delete_project, 'project')


@click.command()
@click.option('--name', help="Dataset name, e.g. tensorport/mnist")
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def delete_dataset(config, name):
    """
    Delete a dataset
    """
    # TODO: fix owner
    try:
        client = TensorportClient(
            token=config.get('token'), username=config.get('username'))
        try:
            if name is not None:
                username, dataset_name, _ = tokenize_repo(name)
                dataset = client.get_dataset(dataset_name, username=username)
            else:
                dataset = None

            if dataset:
                click.confirm('Do you want to delete dataset %s/%s?' %
                              (username, dataset_name), abort=True)
                dataset = client.delete_dataset(dataset_name, username)
                click.echo(info("Dataset %s/%s deleted" %
                                (username, dataset_name)))
            else:
                datasets = client.get_datasets()
                if datasets:
                    click.echo(question("Select a dataset to delete"))
                    data = []
                    data.append(
                        ['#', 'Project', 'Modified at', 'Description'])

                    i = 0
                    valid_datasets = []
                    for dataset in datasets:
                        try:
                            data.append([
                                i,
                                "%s/%s" % (dataset.get('owner')
                                           ['username'], dataset.get('name')),
                                dataset.get('modified_at')[:19],
                                dataset.get('description')
                            ])
                            i += 1
                            valid_datasets.append(dataset)
                        except:
                            pass
                    table = render_table(data, 36)
                    click.echo(table.table)
                    dataset_to_delete_id = select_valid_index(
                        0,
                        len(valid_datasets) - 1,
                        question('Select the dataset you want to delete.'))
                    dataset_name = valid_datasets[dataset_to_delete_id].get(
                        'name')
                    username = valid_datasets[dataset_to_delete_id].get('owner')[
                        'username']
                    click.confirm('Do you want to delete dataset %s/%s?' %
                                  (username, dataset_name), abort=True)
                    dataset = client.delete_dataset(dataset_name, username)
                    click.echo(info("Dataset %s/%s deleted" %
                                    (username, dataset_name)))
                else:
                    click.echo(info("You don't seem to have any datasets to delete."))
                    return

        except:
            click.echo(info("Couldn't delete the dataset."))
            return
    except Exception as e:
        logger.error("Failed to run 'tport delete dataset'", exc_info=True)
        return


delete.add_command(delete_dataset, 'dataset')


@click.command()
@click.option('--name', prompt=True)
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def get_dataset(config, name):
    """
    Get information about a dataset
    """
    client = TensorportClient(
        token=config.get('token'), username=config.get('username'))
    dataset = client.get_dataset(name, config.get('username'))

    click.echo("Dataset: %s | ID: %s" % (dataset.get('name'),
                                         dataset.get('id')))
    return dataset


get.add_command(get_dataset, 'dataset')


@click.command()
@click.option('--owner')
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def get_datasets(config, owner=None):
    """
    List datasets
    """
    client = TensorportClient(
        token=config.get('token'), username=config.get('username'))
    datasets = client.get_datasets(owner)

    if datasets:
        click.echo(info("All datasets:"))
        data = []
        data.append(
            ['#', 'Dataset', 'Modified at', 'Description'])

        i = 0
        for project in datasets:
            try:
                data.append([
                    i,
                    "%s/%s" % (project.get('owner')
                               ['username'], project.get('name')),
                    project.get('modified_at')[:19],
                    project.get('description')
                ])
                i += 1
            except:
                pass
        table = render_table(data, 36)
        click.echo(table.table)
        return datasets
    else:
        click.echo("It doesn't look like you have any datasets yet. You can make a new one with 'tport create dataset'.")
        return None


get.add_command(get_datasets, 'datasets')


@click.command()
@click.option('--watch', is_flag=True, default=False, help='Watch events every 1 second.')
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def get_events(config, watch):
    """
    See latest events
    """
    client = TensorportClient(
        token=config.get('token'), username=config.get('username'))
    flag = True
    while flag:
        flag = watch
        events = client.get_events()
        if events:
            data = [['Time', 'Job', 'Status', 'Event']]

            i = 0
            for e in events:
                try:
                    data.append([
                        e.get('created_at')[:19],
                        e.get('job_name'),
                        e.get('event_level_display'),
                        e.get('event_type_display')
                    ])
                    i += 1
                except:
                    pass
            table = render_table(data, 54)
            if flag:
                os.system("printf '\033c'")
            click.echo(table.table)
            if flag:
                time.sleep(1)
        else:
            click.echo("Failed to query recent events. Perhaps you have not started a job yet. Try 'tport run'.")
            return None


get.add_command(get_events, 'events')


@authenticate()
def _create_job(config,
                name=None,
                project=None,
                commit=None,
                datasets=None,
                module='main',
                package_manager='pip',
                package_path='',
                tf_version='1.0.0',
                requirements='requirements.txt',
                training_mode='distributed',
                instance_type=None,
                worker_replicas=None,
                worker_type=None,
                ps_replicas=None,
                ps_type=None,
                time_limit=None,
                description=None,
                framework='tensorflow',
                python_version='2.7'):
    client = TensorportClient(
        token=config.get('token'), username=config.get('username'))

    if name is None:
        random_job_name = random_name_generator()
        name = click.prompt(text=question('Job name'), default=random_job_name)

    # Check Project
    try:
        username, project_name, commit = tokenize_repo(project)
        project = client.get_project(project_name, username)
        if not project:
            click.echo(
                info("Can not find project %s/%s" % (username, project_name)))
            return None

        commits = project.get('commits')
        if not commits:
            click.echo(
                info("No commit available for %s/%s." % (username,
                                                         project_name)))
            click.echo(
                info(
                    "Consider pushing your commits to tensorport."
                ))
            click.echo(info("git push tensorport master"))
            return None

        all_commits = [c.get('id') for c in project.get('commits')]
        if commit and not commit in all_commits:
            click.echo(
                info("Can not find commit %s in %s/%s" % (
                    commit, username, project_name)))
            commit = None
        else:
            # select default one
            commit = all_commits[0]

    except Exception as e:
        click.echo(info("Can not find commit %s in %s" % (commit, project)))
        return None

    # Check Commits
    if commit is None:
        try:
            commits = project.get('commits')
            if not commits:
                click.echo(
                    info("No commit available for %s/%s." % (username,
                                                             project_name)))
                click.echo(
                    info("Consider pushing your commits to tensorport."))
                click.echo(info("git push tensorport master"))
                return None

            commit_to_use = commits[0].get('id')
        except Exception as e:
            logger.error("No commit found, aborting'", exc_info=True)
            return None
    else:
        # TODO: validate the commit
        commit_to_use = commit

    # Strip .py from module, many users leave it there!
    module = module.strip('.py')

    datasets_list = []
    if datasets:
        tmp_datasets = datasets.split(',')
        try:
            for d in tmp_datasets:
                user, repo, commit = tokenize_repo(d)
                dataset = client.get_dataset(repo, user)
                if commit is not None:
                    datasets_list.append({
                        'dataset':
                            dataset.get('id'),
                        'git_commit_hash':
                            commit,
                        'mount_point':
                            ''
                    })
        except:
            click.echo(info("Ignoring dataset %s because it is not valid." % d))


    # Specify Python Version
    python_versions = ['2.7', '3.5']
    if python_version not in python_versions:
        logger.error("Python Version Not Supported, aborting", exc_info=True)
        return None

    # Specify Framekwork
    frameworks = ['tensorflow', 'pytorch']
    if framework not in frameworks:
        logger.error("Framework Not Supported, aborting", exc_info=True)
        return None

    # Specify TensorFlow Version
    tf_versions = [v['name'] for v in client.get_tf_versions()]
    if not tf_version in tf_versions:
        logger.error("TensorFlow version %s Not Supported, aborting" % tf_version, exc_info=True)
        return None


    # Select training mode
    training_modes = ['single-node', 'distributed']
    if framework == 'tensorflow' and ((training_mode is None) or (not training_mode in training_modes)):

        if not training_mode in training_modes:
            logger.error("Training Mode %s for tensorflow not Supported, aborting" % training_mode, exc_info=True)
            return None

    elif framework == 'pytorch':
        training_mode = 'single-node'

    # Instance types and number of resources
    instance_types = client.get_instance_types()
    data = [['#', 'Name', 'CPU Cores', 'GPU', 'Memory (GB)']]

    i = 0
    valid_it = []
    for it in instance_types:
        try:
            data.append(
                [i,
                 it.get('type'),
                 it.get('cpu'),
                 "%d x NVIDIA K80" % (it.get('gpu')) if (it.get('gpu') > 0) else "None",
                 it.get('memory')])
            i += 1
            valid_it.append(it)
        except:
            pass
    it_table = render_table(data, 36)

    if training_mode == 'single-node':
        if instance_type is None:
            click.echo(question('Select instance type from:'))
            click.echo(it_table.table)
            it_id = select_valid_index(0,
                                       len(valid_it) - 1,
                                       question("Select instance type from"))
            instance_type = valid_it[it_id].get('type')
            click.echo(info("%s selected for instance type" % instance_type))

        # Set instance type
        worker_instance_type = instance_type
        ps_instance_type = instance_type

    else:
        if worker_replicas is None or worker_replicas < 1:
            # Specify number of workers
            worker_replicas = click.prompt(
                text=question('Select number of workers'), default=1)

        if (worker_type is None) or (not worker_type in [it.get('type') for it in valid_it]):
            # Specify worker type
            click.echo(question('Select instance type of workers from:'))
            click.echo(it_table.table)
            it_id = select_valid_index(
                0,
                len(valid_it) - 1,
                question("Select instance type of workers from"))
            worker_instance_type = valid_it[it_id].get('type')
            click.echo(
                info("%s selected for worker instance type" %
                     worker_instance_type))
        else:
            worker_instance_type = worker_type

        if ps_replicas is None or ps_replicas < 1:
            # Specify number of workers
            ps_replicas = click.prompt(
                text=question('Select number of parameter servers'), default=1)

        if (ps_type is None) or (not ps_type in [it.get('type') for it in valid_it]):
            # Specify worker type
            click.echo(
                question('Select instance type of parameter servers from:'))
            click.echo(it_table.table)
            it_id = select_valid_index(
                0,
                len(valid_it) - 1,
                question("Select instance type of parameter servers from"))
            ps_instance_type = valid_it[it_id].get('type')
            click.echo(
                info("%s selected for parameter server instance type" %
                     ps_instance_type))
        else:
            ps_instance_type = ps_type

    if time_limit:
        hours, minutes = time_limit_validator(time_limit)
    else:
        hours, minutes = None, None

    if (hours is None) or (minutes is None):
        while (hours is None) or (minutes is None):
            time_limit = click.prompt(
                text=question('Select the time limit for the job'),
                default='48h0m')
            hours, minutes = time_limit_validator(time_limit)
    click.echo(
        info("Job will run for %d hours and %d minutes" % (hours, minutes)))
    total_minutes = hours * 60 + minutes



    if training_mode == 'single-node':
        training_mode = 'single-node-tf'
    elif training_mode == 'distributed':
        training_mode = 'distributed-tf'
    else:
        click.echo("Invalid training mode.")
        return

    parameters = {
        "tensorport_api_token": config.get('token'),
        "module": module,
        "package_path": package_path,
        "package_manager": package_manager,
        "mode": training_mode,
        "worker_replicas": worker_replicas,
        "worker_type": worker_instance_type,
        "ps_replicas": ps_replicas,
        "ps_type": ps_instance_type,
        "instance_type": instance_type,
        "requirements": requirements,
        "time_limit": total_minutes,
        "datasets": datasets_list,
        "code": project.get('id'),
        "code_commit": commit_to_use,
        "tf_version": tf_version,
        "framework": framework,
        "python_version": python_version
    }

    # Send API Request
    job = client.create_job(
        project,
        name,
        description,
        parameters,
        commit_to_use,
        datasets=datasets_list)
    if job:
        click.echo(info("Job %s created successfully." % name))
        click.echo(info("You can see your job in matrix : %s/%s/%s." %
                        (MATRIX_URL, username, project_name)))
        return job
    else:
        click.echo(info("Failed to create the job."))
        return None


@click.command()
@click.option('--name', help='Job name')
@click.option('--project', help="Project name, e.g. 'tensorport/mnist:[GIT COMMIT HASH]'")
@click.option('--datasets', help="Comma separated list of the datasets to use for the job. e.g. 'tensorport/mnist-training:[GIT COMMIT HASH],tensorport/mnist-val:[GIT COMMIT HASH]'")
@click.option('--mode', 'training_mode', default='distributed', help='Train in single-node or distributed mode.')
@click.option('--module', help='Module name, e.g. main')
@click.option('--package-path', help='Package path')
@click.option('--package-manager', help='Package Manager, conda or pip', default="pip")
@click.option('--framework', help='Pytorch or Tensorflow', default="tensorflow", type=str, required=True)
@click.option('--framework-version', help='TensorFlow version, e.g. 1.0.0', default='1.3.0')
@click.option('--python-version', help='2.7 or 3.5', default="2.7", type=str)
@click.option('--requirements', help="pip requirements file, e.g 'requirements.txt'.")
@click.option('--instance-type', help="Instance type of the machine (for single node training only), e.g. 't2.small'")
@click.option('--worker-replicas', help='Number of workers (for distributed training only)', type=int)
@click.option(
    '--worker-type',
    help="Instance type for workers (for distributed training only), e.g. 't2.small'."
)
@click.option(
    '--ps-replicas',
    help='Nubmer of parameter servers (for distributed training only)',
    type=int)
@click.option(
    '--ps-type',
    help="Instance type for parameter servers (for distributed training only), e.g. 't2.small'."
)
@click.option('--time-limit', help="Time limit for the job, e.g. '22h30m'.")
@click.option(
    '--description', help='Job description [optional]', required=False)
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def create_job(config,
               name=None,
               project=None,
               datasets=None,
               module=None,
               package_manager=None,
               package_path=None,
               requirements=None,
               training_mode=None,
               instance_type=None,
               worker_replicas=None,
               worker_type=None,
               ps_replicas=None,
               ps_type=None,
               time_limit=None,
               description=None,
               python_version=None,
               framework=None,
               framework_version=None,
               ):
    """
    Create a job
    """
    training_mode = training_mode.replace('_', '-')
    try:
        job = _create_job(
            config=config,
            name=name,
            project=project,
            datasets=datasets,
            module=module,
            package_manager=package_manager,
            package_path=package_path,
            tf_version=framework_version,
            requirements=requirements,
            training_mode=training_mode,
            instance_type=instance_type,
            worker_replicas=worker_replicas,
            worker_type=worker_type,
            ps_replicas=ps_replicas,
            ps_type=ps_type,
            time_limit=time_limit,
            description=description,
            framework=framework,
            python_version=python_version)
    except Exception as e:
        logger.error("Failed to run 'tport create job'", exc_info=True)
        return


create.add_command(create_job, 'job')


@cli.command()
@click.option('--local', is_flag=True, default=False, help='Run the job locally. Works both with distributed or single-node.')
@click.option('--existing', is_flag=True, default=False, help='Run existing TensorPort job.')
@click.option('--job-id', help='ID of the TensorPort job to run (if running an existing job).')
@click.option('--name', help='Job name')
@click.option('--project', help="Project name, e.g. 'tensorport/mnist:[GIT COMMIT HASH]'")
@click.option('--datasets', help="Comma separated list of the datasets to use for the job. e.g. 'tensorport/mnist-training:[GIT COMMIT HASH],tensorport/mnist-val:[GIT COMMIT HASH]'")
@click.option('--mode', 'training_mode', default='distributed', help='Train in distributed or single node mode.')
@click.option('--module', help='Module name, e.g. main')
@click.option('--package-path', help='Package path', default="")
@click.option('--package-manager', help='Package Manager, conda or pip', default="pip")
@click.option('--framework-version', help='TensorFlow version, e.g. 1.0.0', default='1.3.0', required=False)
@click.option('--python-version', help='2.7 or 3.5', default="2.7", type=str)
@click.option('--framework', help='Pytorch or Tensorflow', default="tensorflow", type=str, required=True)
@click.option(
    '--requirements', help="pip requirements file, e.g 'requirements.txt'.")
@click.option(
    '--instance-type',
    help="Instance type of the machine (for single node training only), e.g. 't2.small'"
)
@click.option(
    '--worker-replicas',
    help='Number of workers (for distributed training only)',
    type=int)
@click.option(
    '--worker-type',
    help="Instance type for workers (for distributed training only), e.g. 't2.small'."
)
@click.option(
    '--ps-replicas',
    help='Number of parameter servers (for distributed training only)',
    type=int)
@click.option(
    '--ps-type',
    help="Instance type for parameter servers (for distributed training only), e.g. 't2.small'."
)
@click.option('--time-limit', help="Time limit for the job, e.g. '22h30m'.")
@click.option(
    '--description', help='Job description [optional]', required=False)
@click.option('--current_env', is_flag=True, default=False, help='Use current environment when running locally.')
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
def run(config,
        name=None,
        project=None,
        datasets=None,
        module=None,
        package_path=None,
        package_manager=None,
        requirements=None,
        training_mode=None,
        instance_type=None,
        worker_replicas=None,
        worker_type=None,
        ps_replicas=None,
        ps_type=None,
        time_limit=None,
        local=None,
        description=None,
        existing=False,
        job_id=None,
        framework=None,
        framework_version=None,
        python_version=None,
        current_env=False):
    """
    Run a job (--local, --existing, ...)
    """
    # Todo Remove this
    if training_mode:
        training_mode = training_mode.replace('_', '-')

    try:
        if local:
            run_local_tf(package_path, module, training_mode, worker_replicas,
                         ps_replicas, requirements, current_env, framework_version)
        else:
            if existing:
                _start_job(config, job_id)
            else:
                job = _create_job(
                    config=config,
                    name=name,
                    project=project,
                    datasets=datasets,
                    module=module,
                    package_path=package_path,
                    package_manager=package_manager,
                    tf_version=framework_version,
                    requirements=requirements,
                    training_mode=training_mode,
                    instance_type=instance_type,
                    worker_replicas=worker_replicas,
                    worker_type=worker_type,
                    ps_replicas=ps_replicas,
                    ps_type=ps_type,
                    time_limit=time_limit,
                    framework=framework,
                    description=description,
                    python_version=python_version)
                if job:
                    _start_job(config, job.get('job_id'))
                    click.echo(info("Job started."))

    except Exception as e:
        logger.error("Failed to run 'tport run'", exc_info=True)
        return


def run_local_tf(package_path, module, training_mode, worker_replicas,
                 ps_replicas, requirements=None, current_env=False, tf_version=None):
    # Select training mode
    training_modes = ['single-node', 'distributed']
    if (training_mode is None) or (not training_mode in training_modes):
        if not training_mode:
            mode = click.echo(question('Select a training mode from'))
        else:
            mode = click.echo(
                question('%s is not a valid training mode. Select from' %
                         training_mode))
        for i, mode in enumerate(training_modes):
            click.echo('%s | %s' % (i, mode))
        mode_id = select_valid_index(0,
                                     len(training_modes) - 1,
                                     question("Select training mode from"))
        training_mode = training_modes[mode_id]

    if training_mode == 'distributed':
        # Specify number of workers
        if worker_replicas == None:
            worker_replicas = click.prompt(
                text=question('Select number of workers'), default=1)
        else:
            worker_replicas = int(worker_replicas)
        # Specify number of parameter servers
        if ps_replicas == None:
            ps_replicas = click.prompt(
                text=question('Select number of parameter servers'), default=1)
        else:
            ps_replicas = int(ps_replicas)

    # Specify module
    if module is None:
        module = click.prompt(
            text=question('Specify the python module to run'),
            default='main')

    # Strip .py from module, many users leave it there!
    module = module.strip('.py')

    if not current_env:
        if requirements is None:
            choice = select_valid_index(0, 2,
                                        question(
                                            "Requirements file not specified. You can \n    0- Specify a requirements file\n    1- Run without installing any requirements\n    2- Use your current environment (not recommended).\n -> Which one do you want?"))
            if choice == 0:
                current_env = False
                requirements = click.prompt(
                    text=question('Specify the requirements file'),
                    default='requirements.txt')
                requirements = os.path.join(os.getcwd(), requirements)
            elif choice == 1:
                current_env = False
                requirements = None
            elif choice == 2:
                current_env = True

    if tf_version is None:
        tf_version = '1.0.0'

    print("Running %s locally" % training_mode)
    assert (training_mode in ['single-node', 'distributed'])
    run_tf(
        cwd=os.getcwd(),
        package_path=package_path,
        module=module,
        mode=training_mode,
        worker_replicas=worker_replicas,
        ps_replicas=ps_replicas,
        requirements=requirements,
        current_env=current_env,
        tf_version=tf_version)


def _start_job(config, job_id=None):
    """
    Starts Job
    """
    try:
        client = TensorportClient(
            token=config.get('token'), username=config.get('username'))
        # We get list of user jobs and allow user to select them
        if not job_id:
            jobs = client.get_jobs(params={'status': 'stopped'})
            if jobs:
                click.echo(info('Jobs to start:'))
                data = []
                data.append(
                    ['#', 'Job Name', 'Project', 'Status', 'Launch at'])

                i = 0
                valid_jobs = []
                for job in jobs:
                    try:
                        data.append([
                            i,
                            '%s/%s' % (job.get('owner'),
                                       job.get('display_name')),
                            '%s/%s:%s' %
                            (job.get('repository_owner'), job.get('repository_name'),
                             job.get('git_commit_hash')[:8]),
                            job.get('status'),
                            '' if job.get('launched_at') is None else job.get(
                                'launched_at')[:-5]
                        ])
                        i += 1
                        valid_jobs.append(job)
                    except:
                        pass
                table = render_table(data, max_length=36)
                click.echo(table.table)

                # Select the job
                job_to_start_id = select_valid_index(
                    0,
                    len(valid_jobs) - 1,
                    question('Select the job you want to start.'))

                job_id = valid_jobs[job_to_start_id].get('job_id')
                job_name = valid_jobs[job_to_start_id].get('display_name')
            else:
                click.echo(
                    info(
                        "It doesn't look like you have any jobs to start. Use 'tport create job' or 'tport run' to run a job."
                    ))
                return
        else:
            try:
                job = client.get_job(params={'job_id': job_id})
                if job:
                    job_id = job.get('job_id')
                    job_name = job.get('display_name')
                else:
                    click.echo(info("%s is not a valid job id." % job_id))
                    return
            except:
                click.echo(info("%s is not a valid job id." % job_id))
                return

        # Start Job
        job = client.start_job(job_id)
        if job:
            click.echo(info("Job '%s' started." % job.get('display_name')))
    except Exception as e:
        logger.error("Failed to run 'tport start'", exc_info=True)
        return


@cli.command()
@click.option('--job-id')
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def pause(config, job_id=None):
    """
    Pause a job
    """
    try:
        client = TensorportClient(
            token=config.get('token'), username=config.get('username'))
        # We get list of user jobs and allow user to select them
        if not job_id:
            # TODO: limit jobs that this user can pause
            jobs = client.get_jobs(params={'status': 'started'})
            if jobs:
                job_id, job_name = select_job(jobs, 'Select the job you want to pause')
            else:
                click.echo(
                    info(
                        "You do not seem to have any running jobs. Use 'tport run' to run a job."
                    ))
                return
        else:
            job = client.get_job(params={'job_id': job_id})
            if job:
                job_id = job.get('job_id')
                job_name = job.get('display_name')
            else:
                click.echo(info("%s is not a valid job id." % job_id))
                return
        job = client.stop_job(job_id)

        if job:
            click.echo(info("Job '%s' is paused." % job.get('display_name')))
    except Exception as e:
        logger.error("Failed to run 'tport pause'", exc_info=True)
        return


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, resolve_path=True))
@click.option('--job-id')
@click_log.simple_verbosity_option()
@click_log.init(__name__)
@pass_config
@authenticate()
def download_files(config, path, job_id=None):
    """
    downloads all outputs and saves at specified path
    """
    try:
        client = TensorportClient(
            token=config.get('token'), username=config.get('username'))
        # We get list of user jobs and allow user to select them
        if not job_id:
            jobs = client.get_jobs()
            if jobs:
                job_id, job_name = select_job(jobs, 'Select the job you want to download files from')
            else:
                click.echo(
                    info(
                        "You do not seem to have any jobs. Use 'tport run' to run a job."
                    ))
                return
        else:
            job = client.get_job(params={'job_id': job_id})
            if job:
                job_id = job.get('job_id')
                job_name = job.get('display_name')
            else:
                click.echo(info("%s is not a valid job id." % job_id))
                return
        # Download file list
        job_file_list = client.get_file_list(job_id)
        counter = 0
        for file in job_file_list:
            counter += 1
            # Display the files
            click.echo(
                option('%s | %s | %s kb' % (counter, file['name'], file['size'] / 1024)))
            try:
                if file['size'] > 0:
                    # Save file in specified path
                    file_content = client.download_file(job_id, file['name'])
                    file_path = os.path.join(path, file['name'])
                    f = open(file_path, "w")
                    f.write(file_content)
                    f.close()

            except Exception as e:
                click.echo("Failed to download files: %s" % str(e))
                logger.error("Failed to download file: %s" % str(e), exc_info=True)
                continue

    except Exception as e:
        logger.error("Failed to download files", exc_info=True)
        return


if __name__ == '__main__':
    cli()
