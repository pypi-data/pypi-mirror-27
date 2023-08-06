""" A Python gitlab template for initiating new projects in gitlab. The
boilerplate / template files that are copied are based on best-practices
for Python package development. """
import argparse
import logging
import shlex
import shutil
import os
from os import path


def copytree(src, dst, symlinks=False, ignore=None):
    """ The shutil.copytree version that enables copying to
    an already existing directory. """
    for item in os.listdir(src):
        s = path.join(src, item)
        d = path.join(dst, item)
        if path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            if ignore:
                if item in ignore(src, [item]):
                    continue
            shutil.copy2(s, d)


def ignore_names(src, names):
    """
    :param str src: the directory path being walked over
    :param list names: the list of file and directory names
    :return: a list of file / directory names to ignore.
    """
    ignore = ['.git', '.cache', '__pycache__']
    ignore += [name for name in names if name.endswith('.pyc')]
    if path.abspath(src) == path.dirname(path.abspath(__file__)):
        ignore += ['__init__.py']  # do not include this file
    return ignore


def copy_template(base_dir, package_name):
    """ copy the `mrg_gitlab_template` directory to the requested base directory,
    and rename it to the package name. """

    exists = False
    package_dir = path.join(path.abspath(base_dir), package_name)
    if path.exists(package_dir):
        logging.warning('Package directory already exists: %s', package_dir)
        exists = True

    copy_dir = path.dirname(path.abspath(__file__))
    if exists:
        copytree(copy_dir, package_dir, ignore=ignore_names)
    else:
        shutil.copytree(copy_dir, package_dir, ignore=ignore_names)

    pkg_dir = path.join(package_dir, 'package')
    src_dir = path.join(package_dir, package_name)
    os.rename(pkg_dir, src_dir)

    return package_dir


def replace_in_dir(base_dir, package, author, email, group, year, pages_domain, gitlab_url):
    ignore_file_ext = ['.png']
    package_dir = path.join(path.abspath(base_dir), package)
    if not path.exists(package_dir):
        logging.error('Package directory does not exist: %s', package_dir)

    for dir_path, dir_names, file_names in os.walk(package_dir):
        for file_name in file_names:
            file_path = path.join(dir_path, file_name)
            ext = path.splitext(file_name)[1]
            if ext.lower() in ignore_file_ext:
                logging.debug('Ignoring file conversion for: %s', file_path)
                continue
            try:
                with open(file_path) as file_obj:
                    content = file_obj.read()
                    content = content.replace('{{package}}', package)
                    content = content.replace('{{author}}', author)
                    content = content.replace('{{email}}', email)
                    content = content.replace('{{group}}', group)
                    content = content.replace('{{year}}', year)
                    content = content.replace('{{pages_domain}}', pages_domain)
                    content = content.replace('{{gitlab_url}}', gitlab_url)

                logging.info('Converted: %s', file_path)
                with open(file_path, 'w') as file_obj:
                    file_obj.write(content)

            except Exception as exc:
                logging.error('Could not convert: %s', file_path)
                logging.exception(exc)


def main(cmdline=None):
    """ main entry point of script. """
    import time

    parser = argparse.ArgumentParser(
        description='Create new project from template',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('package',
                        help='package name')
    parser.add_argument('-g', '--group', required=True,
                        help='the gitlab group or account name. '
                             'Example: mrg-tools, sci-fv, your account name, etc')
    parser.add_argument('-p', '--pages-domain', default='gitlab.io',
                        help='the gitlab pages url domain. '
                             'Example: gitlab.io, io.esa.int')
    parser.add_argument('-u', '--gitlab-url', default='gitlab.com',
                        help='the gitlab pages url domain. '
                             'Example: gitlab.com, gitlab.esa.int')
    parser.add_argument('-a', '--author', default='{{author}}',
                        help='author name')
    parser.add_argument('-e', '--email', default='{{email}}',
                        help='author email')
    parser.add_argument('-y', '--year', default=time.strftime('%Y'),
                        help='author email')
    parser.add_argument('-d', '--directory', default='.',
                        help='base directory location')
    # parser.add_argument('-c', '--config', type=str,
    #                     help='The configuration file to load.')
    parser.add_argument('-v', '--verbosity', action='count', default=0,
                        help='Increase output verbosity')

    if cmdline:
        cmdline = shlex.split(cmdline)

    opts = parser.parse_args(cmdline)
    log_format = '%(asctime)s %(levelname)-7s %(name)-30s %(thread)-8d %(message)s'
    log_level = [logging.ERROR, logging.INFO, logging.DEBUG][min(opts.verbosity, 2)]
    logging.basicConfig(level=log_level, format=log_format)

    logging.info('Copying template directory...')
    copy_template(opts.directory, opts.package)
    logging.info('Converting placeholders...')

    replace_in_dir(opts.directory, opts.package, opts.author, opts.email, opts.group, opts.year, opts.pages_domain, opts.gitlab_url)
    logging.info('Finished.')


if __name__ == '__main__':
    _CMDLINE = None
    main(_CMDLINE)
