# -*- coding: utf-8 -*-

import os
import sys
import json
import click

from subprocess import Popen, PIPE
from concurrent.futures import ThreadPoolExecutor, as_completed


class ParallelCondaInstaller:
    """
    Handles options sent to pconda install subcommand
    """

    @classmethod
    def install(cls, args):
        """
        Handle the parallel installation of package given args
        """
        _pconda = cls()

        click.secho('Running install w/ args: {}'.format(args), fg='yellow')

        install_packages, uninstall_packages = _pconda.get_install_plan(args)

        # Do uninstalls first.
        for package in uninstall_packages:
            click.secho('Uninstalling {}={}...'.format(package['name'], package['version']), nl=False)
            out, error = Popen(['conda', 'uninstall', '-yq', '{}'.format(package['name'])],
                           stdout=PIPE, stderr=PIPE).communicate()
            if error:
                click.secho('\nSeems there was an error uninstalling this package:\n{}'.format(error), color='red')
                sys.exit(1)
            click.secho('done.')

        # Execute installs in parallel.
        with ThreadPoolExecutor(max_workers=10) as executor:
            successes = []
            failures = []
            jobs = {executor.submit(_pconda.install_single_package, **package): package for package in
                    install_packages}
            for i, future in enumerate(as_completed(jobs)):
                package = jobs[future]
                try:
                    result = future.result()
                    successes.append(result)
                    click.secho('\rInstalling...{:.1f}% Complete'.format(((i+1) / len(jobs)) * 100), fg='green', nl=False)
                except Exception as exc:
                    failures.append({'name': package['name'],
                                     'version': package['version'],
                                     'error': '{}'.format(exc)}
                                    )

        # Summarize install successes and failures.
        click.secho('\n\nSummary:\n-----------------', fg='yellow')
        click.secho('Successful installs:', fg='green')
        for package, result in zip(install_packages, successes):
            click.echo('\t{}={}'.format(package.get('name'), package.get('version'), result.get('success')))

        # Output install failures
        if len(failures):
            click.secho('Failures: ', fg='red')
            for failure in failures:
                click.secho('\t{}={}\n\t\tError: {}'
                            .format(failure.get('name'), failure.get('version'), failure['error']), fg='red'
                            )
        else:
            click.secho('Failures: None', fg='green')
        click.secho('-----------------', fg='yellow')

        # Exit
        click.secho('\nInstall completed {fail_status} failures! {recommend}'
                    .format(fail_status='with' if len(failures) else 'without',
                            recommend='' if len(failures) else '-> Like pconda? Tell your friend(s)! :)'
                            ),
                    fg='red' if len(failures) else 'green'
                    )

    def get_install_plan(self, args):
        """
        Determine what conda will install to satisfy this package in the environment.
        """
        cmd = ['conda', 'install']
        cmd.extend([arg for arg in args])
        cmd.extend(['--json', '--dry-run'])
        info, _ = Popen(cmd, stdout=PIPE).communicate()
        actions = json.loads(info.decode('utf-8')).get('actions')[0]
        install_packages = actions.get('LINK', [])
        uninstall_packages = actions.get('UNLINK', [])
        for plan, packages in zip(['Install', 'Uninstall'], [install_packages, uninstall_packages]):
            click.echo('\n{} plan:\n--------------------'.format(plan, args))
            for package in packages:
                click.echo('{}={}'.format(package.get('name'), package.get('version')))
            click.echo('--------------------\n')

        # Confirm user wants this
        if '-y' not in args:
            click.confirm('Continue with this plan?', default=True, abort=True)

        return install_packages, uninstall_packages

    @staticmethod
    def install_single_package(**kwargs):
        """
        Installs a single package into the environment, forcing no dependencies.
        Intended to be used in parallel while other packages are installed
        """

        package = kwargs.get('name')
        version = kwargs.get('version')
        channel = kwargs.get('channel')

        info, _ = Popen(
            ['conda', 'install', '-y', '{}={}'.format(package, version),
             '-c', channel, '--no-deps', '--json'],
            stdout=PIPE
        ).communicate()

        return json.loads(info.decode('utf-8'))


@click.group()
def pconda():
    """
    Program to wrap conda with parallel abilities in installing package(s) and its requirements
    Example use: "pconda install numpy pandas"
    """
    pass


@pconda.command(context_settings={'ignore_unknown_options': True, 'allow_extra_args': True})
@click.pass_context
def install(ctx):
    """
    --Install package(s) and their dependencies in parallel.
    """
    ParallelCondaInstaller.install(args=ctx.args)


def go():
    pconda()


if __name__ == '__main__':
    go()
