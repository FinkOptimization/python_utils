import subprocess
import os
import hashlib

MAIN_BRANCHES = {'master', 'production'}
DEFAULT_VERSION = '0.1'


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

        if branch in MAIN_BRANCHES:
            # Get the last tag of the branch
            out = _minimal_ext_cmd(['git', 'describe', '--abbrev=0'])
            tag = out.strip().decode('utf-8')
            version = (tag
                       if tag != '' and not tag.startswith('fatal')
                       else DEFAULT_VERSION)
        else:
            out = _minimal_ext_cmd(['git', 'describe'])
            tag = out.strip().decode('utf-8')
            tag_commits_hash = tag.split('-')
            version = ((tag
                        if len(tag_commits_hash) < 1 or int(tag_commits_hash[1]) == 0
                        else tag_commits_hash[0])
                       if tag != '' and not tag.startswith('fatal')
                       else DEFAULT_VERSION)

    except OSError:
        version = ''

    return version
