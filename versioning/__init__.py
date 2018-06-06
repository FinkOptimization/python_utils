import subprocess
import os
import hashlib

DEVELOPMENT_BRANCH = 'master'
PRODUCTION_BRANCH = 'production'


def last(x: int, offset=0):
    return int(x * (x + 2 * offset + 1) / 2)


def n_pairing(x: int, y: int, c=50):
    start = last(x, 1)
    step = last(int(y/c), x)
    return (start + step) * c + (y % c)


def reverse_n_pairing(z: int, c=50):
    x = 0
    y = 0
    current_value = n_pairing(x, y, c)

    while current_value < z:
        while current_value < z:
            y += c
            current_value = n_pairing(x, y, c)

        if current_value > z:
            y -= c
            current_value = n_pairing(x, y, c)

        while current_value < z and y > 0:
            x += 1
            y -= c
            current_value = n_pairing(x, y, c)

        if current_value > z:
            x -= 1
            y += c
            current_value = n_pairing(x, y, c)

        if n_pairing(x, y + c, c) > z:
            while current_value < z:
                y += 1
                current_value = n_pairing(x, y, c)
    return x, y


def hash_branch_name(branch):
    """Convert the branch name into a four-digit hashed value"""

    # Use the hashlib for consistency
    return int(hashlib.sha1(branch.encode('utf-8')).hexdigest(), 16) % 10 ** 4


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
        major = 0
        minor = 1
        revision = 0
        branch_id = 0
        branch_commits = 0

        # Get the last tag of the branch
        out = _minimal_ext_cmd(['git', 'describe', '--abbrev=0', branch])
        tag = out.strip().decode('utf-8')

        production_commits = 0

        if tag != '' and not tag.startswith('fatal'):
            out = _minimal_ext_cmd(['git', 'merge-base', branch, tag])
            first_hash = out.strip().decode('utf-8')
            tag_components = tag.split('.')
            major = int(tag_components[0])
            minor = 0
            if len(tag_components) > 1:
                minor = int(tag_components[1])
            if len(tag_components) > 2:
                for i in range(2, len(tag_components)):
                    production_commits += int(tag_components[i])
        else:
            out = _minimal_ext_cmd(['git', 'rev-list', '--max-parents=0', '--date-order', '--reverse', 'HEAD'])
            first_hash = out.strip().decode('utf-8').split('\n')[0]

        production_and_branch_ancestor = _minimal_ext_cmd(['git', 'merge-base',
                                                           PRODUCTION_BRANCH, branch]).strip().decode('utf-8')

        for commit in _minimal_ext_cmd(['git', 'log', '--format="%h"',
                                        '{}..{}'.format(first_hash,
                                                        production_and_branch_ancestor)
                                        ]).strip().decode('utf-8').split('\n'):
            if commit.strip() != '':
                production_commits += 1

        revision += production_commits
        if revision > 0:
            version = "{}.{}.{}".format(major, minor, revision)
        else:
            version = "{}.{}".format(major, minor)

        if branch != PRODUCTION_BRANCH:
            development_and_branch_ancestor = _minimal_ext_cmd(['git', 'merge-base',
                                                                DEVELOPMENT_BRANCH, branch]).strip().decode('utf-8')

            development_commits = 0
            for commit in _minimal_ext_cmd(['git', 'log', '--format="%h"',
                                            '{}..{}'.format(production_and_branch_ancestor,
                                                            development_and_branch_ancestor)
                                            ]).strip().decode('utf-8').split('\n'):
                if commit.strip() != '':
                    development_commits += 1

            if development_commits > 0:
                version = "{}.{}".format(version, development_commits)
            if branch != DEVELOPMENT_BRANCH:
                branch_commits = 0
                branch_id = hash_branch_name(branch)
                current_hash = _minimal_ext_cmd(['git', 'rev-parse', branch]).strip().decode('utf-8')
                for commit in _minimal_ext_cmd(['git', 'log', '--format="%h"',
                                                '{}..{}'.format(production_and_branch_ancestor
                                                                if development_commits == 0
                                                                else development_and_branch_ancestor,
                                                                current_hash)
                                                ]).strip().decode('utf-8').split('\n'):
                    if commit.strip() != '':
                        branch_commits += 1
                if branch_commits > 0:
                    version = "{}-{}".format(version, n_pairing(branch_commits, branch_id))

    except OSError:
        version = ''

    return version
