from . import minimal_ext_cmd

MAIN_BRANCHES = {'master', 'production'}
DEFAULT_VERSION = '0.1'


# Return the git revision as a string
def git_version():
    try:
        # Extract the current branch name
        out = minimal_ext_cmd(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        branch = out.strip().decode('ascii').lower()

        if branch in MAIN_BRANCHES:
            # Get the last tag of the branch
            out = minimal_ext_cmd(['git', 'describe', '--abbrev=0'])
            tag = out.strip().decode('utf-8')
            if tag != '' and not tag.startswith('fatal'):
                version = tag
            else:
                version = DEFAULT_VERSION
        else:
            out = minimal_ext_cmd(['git', 'describe'])
            tag = out.strip().decode('utf-8')

            if tag != '' and not tag.startswith('fatal'):
                tag_commits_hash = tag.split('-')
                if len(tag_commits_hash) > 1 and int(tag_commits_hash[1]) == 0:
                    version = tag_commits_hash[0]
                else:
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
            out = minimal_ext_cmd(['git', 'describe'])
            tag = out.strip().decode('utf-8')
            branch_commits = 0

            if tag != '' and not tag.startswith('fatal'):
                tag_commits_hash = tag.split('-')
                if len(tag_commits_hash) > 1:
                    version = tag_commits_hash[0]
                    branch_commits = int(tag_commits_hash[1])
                else:
                    version = tag
            else:
                raise ValueError('Could not get the current version')

            if branch_commits == 0:
                raise ValueError('Cannot increment the version when there are no changes')
            else:
                major_minor_revision = version.split('.')
                major = int(major_minor_revision[0])
                if len(major_minor_revision) > 1:
                    minor = int(major_minor_revision[1])
                elif major > 0:
                    minor = 0
                else:
                    minor = 1
                message = ''
                if len(major_minor_revision) > 2:
                    revision = int(major_minor_revision[2])
                else:
                    revision = 0
                if update == '+':
                    revision += 1
                    message = 'Revision {}'
                elif update == '++':
                    minor += 1
                    revision = 0
                    message = 'Release {}'
                elif update == '+++':
                    major += 1
                    minor = 0
                    revision = 0
                    message = 'Release {}'
                if revision > 0:
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
