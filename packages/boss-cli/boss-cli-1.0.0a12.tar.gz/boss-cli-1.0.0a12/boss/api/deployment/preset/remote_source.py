'''
Remote Source deployment Preset.

This is a generic deployment preset, where the remote host contains the project
source code and the git repository. The deploy task would synchronize the remote
with the latest changes of the provided branch from the origin.
It then builds the project and restarts the service if needed.
'''


from fabric.api import task, hide
from fabric.colors import cyan
from fabric.context_managers import shell_env

import boss.constants as constants
from boss.config import fallback_branch
from boss.util import remote_info, remote_print
from boss.api import git, notif, shell, runner
from boss.core.constants.notification import (
    DEPLOYMENT_STARTED,
    DEPLOYMENT_FINISHED
)


@task
def deploy(branch=None):
    ''' Deploy to remote source. '''
    stage = shell.get_stage()
    deployer_user = shell.get_user()
    branch = branch or fallback_branch(stage)
    commit = git.last_commit(short=True)
    notif.send(DEPLOYMENT_STARTED, {
        'user': deployer_user,
        'branch': branch,
        'commit': commit,
        'stage': stage
    })

    # Get the latest code from the repository
    sync(branch)
    install_dependencies()

    # Building the app
    build(stage)
    reload_service()

    notif.send(DEPLOYMENT_FINISHED, {
        'user': deployer_user,
        'branch': branch,
        'commit': commit,
        'stage': stage
    })

    remote_info('Deployment Completed')


def reload_service():
    ''' Reload the service after deployment. '''
    runner.run_script_safely(constants.SCRIPT_RELOAD)
    runner.run_script_safely(constants.SCRIPT_STATUS_CHECK)


def install_dependencies():
    ''' Install dependencies. '''
    runner.run_script_safely(constants.SCRIPT_INSTALL)


@task
def sync(branch=None):
    ''' Sync the changes on the branch with the remote (origin). '''
    remote_info('Fetching the latest changes.')
    git.fetch()
    branch = branch or git.current_branch()
    remote_info('Checking out to branch {}.'.format(cyan(branch)))
    git.checkout(branch, True)
    remote_info('Synchronizing with the latest changes.')
    git.sync(branch)


@task
def build(stage_name=None):
    ''' Build the application. '''
    stage = shell.get_stage()

    with shell_env(STAGE=(stage_name or stage)):
        # Trigger the build script.
        runner.run_script_safely(constants.SCRIPT_BUILD)


@task
def stop():
    ''' Stop the service. '''
    runner.run_script_safely(constants.SCRIPT_STOP)


@task
def restart():
    ''' Restart the service. '''
    runner.run_script_safely(constants.SCRIPT_RELOAD)


@task
def status():
    ''' Check the status of the service. '''
    runner.run_script_safely(constants.SCRIPT_STATUS_CHECK)


@task
def check():
    ''' Check the current remote branch and the last commit. '''
    with hide('running'):
        # Show the current branch
        remote_branch = git.current_branch()
        remote_print('Branch: {}'.format(remote_branch))
        # Show the last commit
        git.show_last_commit()
