"""Create a basic projects automatically with virtualenvwrapper."""

import configparser
import datetime
import pathlib
import logging
import os
import re


log = logging.getLogger('virtualenvwrapper.basic')


def owner_info():
    """Read owner name and email from the git global configuration."""
    home = pathlib.Path(os.path.expanduser('~'))
    git_config = home / '.gitconfig'

    config = configparser.ConfigParser()
    if git_config.exists():
        with git_config.open() as f:
            config.read_file(f)
    else:
        log.warn('Warning: .gitconfig was not found.')

    name = config.get('user', 'name', fallback='Anonymous')
    email = config.get('user', 'email', fallback='foo@bar')
    name = os.environ.get('AUTHOR_NAME', name)
    email = os.environ.get('AUTHOR_EMAIL', email)

    log.info('setting project owner to "%s <%s>"' % (name, email))
    return name, email


def multiple_replace(text, adict):
    """Replace multiple substrings in a string based on a translation dict."""
    rep = {re.escape(k): v for k, v in adict.items()}
    pattern = re.compile('|'.join(rep.keys()))
    return pattern.sub(lambda m: rep[re.escape(m.group(0))], text)


def _copy(self, target, env):
    if self.is_file():
        # replace variable in target path
        target = pathlib.Path(multiple_replace(str(target), env))
        target.parent.mkdir(exist_ok=True)  # create required directories
        with self.open('r') as fin:
            with target.open('w') as fout:
                for line in fin:
                    fout.write(multiple_replace(line, env))


pathlib.Path.copy_to = _copy


def template(args):
    """Create the basic skeleton for a python project."""
    project, project_dir = args
    skeleton = os.environ.get(
        'VIRTUALENVWRAPPER_BASIC',
        pathlib.Path(__file__).parent / 'basic.skel'
    )
    destination = pathlib.Path(project_dir)

    name, email = owner_info()
    env = {
        '$AUTHOR_NAME': name,
        '$AUTHOR_EMAIL': email,
        '$PROJECT_NAME': project,
        '$YEAR': str(datetime.datetime.now().year),
        '$MONTH': str(datetime.datetime.now().month),
        '$DAY': str(datetime.datetime.now().day),
        '$$': 'py',    # little hack to package .py template files.
    }

    for source in skeleton.rglob('*'):
        target = destination / source.relative_to(skeleton)
        source.copy_to(target, env)

    return
