from . import minimal_ext_cmd

PRODUCTION_BRANCH = 'production'
DEVELOPMENT_BRANCH = 'master'
MAIN_BRANCHES = {DEVELOPMENT_BRANCH, PRODUCTION_BRANCH}
DEFAULT_VERSION = '0.1'
HOTFIX_STARTNAME = 'rev'


# Return the git revision as a string
def git_version():
    try:
        # Extract the current branch name
        out = minimal_ext_cmd(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        branch = out.strip().decode('ascii').lower()

        # Get the last tag of the branch
        out = minimal_ext_cmd(['git', 'describe'])
        tag = out.strip().decode('utf-8')
        if tag != '' and not tag.startswith('fatal'):
            version = tag
        else:
            version = DEFAULT_VERSION

    except OSError:
        version = ''

    return version


def update_git_version(update='+', push=False):
    try:
        # Extract the current branch name
        out = minimal_ext_cmd(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        branch = out.strip().decode('ascii').lower()
        if branch not in MAIN_BRANCHES:
            raise ValueError('The version cannot be incremented from a feature or hotfix branch')
        else:
            current_version = git_version()
            if current_version == '':
                raise ValueError('Could not get the current version')

            out = minimal_ext_cmd(['git', 'describe', '--abbrev=0'])
            tag = out.strip().decode('utf-8')
            branch_commits = 0

            if tag != '' and not tag.startswith('fatal'):
                version = tag
            else:
                raise ValueError('Could not get the current version')

            version_commits_hash = tag[len(current_version):].split('-')
            if version_commits_hash[0] != '':
                branch_commits = int(version_commits_hash[0])

            if branch_commits == 0:
                raise ValueError('Cannot increment the version when there are no changes')
            else:
                major_minor_revision = version.replace('-', '.').split('.')
                major = int(major_minor_revision[0])
                if len(major_minor_revision) > 1:
                    minor = int(major_minor_revision[1])
                elif major > 0:
                    minor = 0
                else:
                    minor = 1
                message = ''
                revision = 0

                if len(major_minor_revision) > 2:
                    if major_minor_revision[2].startswith(HOTFIX_STARTNAME):
                        revision = int(major_minor_revision[2][len(HOTFIX_STARTNAME):])
                    else:
                        revision = int(major_minor_revision[2])

                post = ''
                if update == '+':
                    revision += 1
                    if post == '' and branch == PRODUCTION_BRANCH:
                        post = HOTFIX_STARTNAME
                elif update == '++':
                    minor += 1
                    revision = 0
                elif update == '+++':
                    major += 1
                    minor = 0
                    revision = 0

                if post != '':
                    message = 'Hotfix {}'
                elif branch == DEVELOPMENT_BRANCH:
                    message = 'Revision {}'
                elif branch == PRODUCTION_BRANCH:
                    message = 'Release {}'

                if revision > 0:
                    if post != '':
                        new_version = '{}.{}-{}{}'.format(major, minor, post, revision)
                    else:
                        new_version = '{}.{}.{}'.format(major, minor, revision)
                else:
                    new_version = '{}.{}'.format(major, minor)
                if version != new_version:
                    minimal_ext_cmd(['git', 'tag', '-a', '-m', message.format(new_version), new_version])
                    print('Created tag {} for {}'.format(new_version, branch))
                    if push:
                        minimal_ext_cmd(['git', 'push', '--tags'])
    except OSError:
        raise ValueError('The version number could not be updated')
