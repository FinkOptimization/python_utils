import subprocess
import os
import hashlib

DEVELOPMENT_BRANCH = 'master'
PRODUCTION_BRANCH = 'production'


def last(x: int, offset=0):
    if x <= 0:
        return 0
    return x + offset + last(x - 1, offset)


def n_pairing(x: int, y: int, c=50):
    start = last(x, 1)
    step = last(int(y/c), x)
    return (start + step) * c + (y % c)


# Return the git revision as a string
def git_version():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH', 'HOME']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env).communicate()[0]
        return out

    try:
        # Extract the current branch name
        out = _minimal_ext_cmd(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        branch = out.strip().decode('ascii').lower()

        # Initialize the minor and revision to zero
        minor = 0
        revision = 0

        # Get the version number from the 'production' branch. Use the number of commits as revision
        out = _minimal_ext_cmd(['git', 'describe', PRODUCTION_BRANCH])
        major_minor_revision = out.strip().decode('ascii').split('-')
        major_minor = major_minor_revision[0].split('.')
        major = int(major_minor[0])
        if len(major_minor) > 1:
            minor = int(major_minor[1])
            # All the remaining numbers will be added together in the version number
            if len(major_minor) > 2:
                for i in range(2, len(major_minor)):
                    revision += int(major_minor[i])

        # The number of commits is added to the revision number
        if len(major_minor_revision) > 1:
            revision += int(major_minor_revision[1])

        # If not in the 'production' branch then extract the number of commits to 'development', not in 'production'
        if branch != 'production':
            out = _minimal_ext_cmd(['git', 'log', DEVELOPMENT_BRANCH, '^{}'.format(PRODUCTION_BRANCH), '--format="%h"'])
            commits = len(out.strip().decode('utf-8').split('\n'))

            revision = n_pairing(revision, commits)

        branch_commits = 0

        # If the branch is not the 'development' or 'production' branch then add the number of commits and the short
        # hash of the commit identifier of the branch
        if branch not in ['master', 'production']:
            out = _minimal_ext_cmd(['git', 'log', branch, '^master', '--format="%h"'])
            branch_commits = len(out.strip().decode('utf-8').split('\n'))

            # Convert the branch name into a four-digit hashed value. Use the hashlib for consistency
            branch = int(hashlib.sha1(branch.encode('utf-8')).hexdigest(), 16) % 10 ** 4

        if branch_commits > 0:
            version = '{}.{}.{}.{}-{}'.format(major, minor, revision, branch, branch_commits)
        elif revision > 0:
            version = '{}.{}.{}'.format(major, minor, revision)
        else:
            version = '{}.{}'.format(major, minor)

    except OSError:
        version = ''

    return version
