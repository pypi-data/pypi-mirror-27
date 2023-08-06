"""Sets up the environment variables for fixie credentials."""
import os

from xonsh.tools import is_string, ensure_string, always_false

from fixie.environ import ENV, ENVVARS, expand_and_make_dir


def fixie_creds_dir():
    """Ensures and returns the $FIXIE_CREDS_DIR"""
    fcd = os.path.join(ENV.get('XDG_DATA_HOME'), 'fixie', 'creds')
    os.makedirs(fcd, exist_ok=True)
    return fcd


ENVVARS.update({
    'FIXIE_CREDS_DIR': (fixie_creds_dir, always_false, expand_and_make_dir,
                        ensure_string, 'Path to fixie credentials directory'),
})
