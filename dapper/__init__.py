"""(Data Assimilation with Python: a Package for Experimental Research)

# documentation

## README

Make sure you've browsed these sections in the README:

- [Highlights](https://github.com/nansencenter/DAPPER#Highlights)
- [Installation](https://github.com/nansencenter/DAPPER#Installation)
- [Quickstart](https://github.com/nansencenter/DAPPER#Quickstart)
- [DA Methods](https://github.com/nansencenter/DAPPER#DA-Methods)
- [Test cases (models)](https://github.com/nansencenter/DAPPER#Test-cases-(models))

## Reference/API docs
The documentation contained in docstrings can be browsed
by clicking the links at the bottom (or on the left) of this page.

## Usage
Do you wish to illustrate and run benchmarks with your own
**models** and/or **methods**?

If these are complicated, you may be better off using DAPPER
merely as inspiration (but you should still
[cite it](https://github.com/nansencenter/DAPPER#Contributors))
rather than trying to squeeze everything into its templates.

If these are simple, however, you may well want to use DAPPER.
First, make sure you've got a good feel for all of `example_{1,2,3}.py`.
Then, read the documentation here

- `mods`
- `da_methods`

## Contributing

### Profiling

- Launch your python script using `kernprof -l -v my_script.py`
- *Functions* decorated with `profile` will be timed, line-by-line.
- If your script is launched regularly, then `profile` will not be
  present in the `builtins.` Instead of deleting your decorations,
  you could also define a pass-through fallback.

### Making a release

- ``cd DAPPER``
- Bump version number in ``__init__.py`` . Also in docs/conf.py ?
- Merge dev1 into master::

"""

__version__ = "0.9.6"

import sys

assert sys.version_info >= (3,8), "Need Python>=3.8"

from dapper.tools.series import UncertainQtty

from .admin import (HiddenMarkovModel, Operator, da_method, get_param_setter,
                    seed_and_simulate, xpList)
from .da_methods.baseline import Climatology, OptInterp, Var3D
# DA methods
from .da_methods.ensemble import LETKF, SL_EAKF, EnKF, EnKF_N, EnKS, EnRTS
from .da_methods.extended import ExtKF, ExtRTS
from .da_methods.other import LNETF, RHF
from .da_methods.particle import OptPF, PartFilt, PFa, PFxN, PFxN_EnKF
from .da_methods.variational import Var4D, iEnKS
from .data_management import (default_fig_adjustments, default_styles,
                              discretize_cmap, load_xps, make_label, rel_index,
                              xpSpace)
from .dpr_config import rc
from .stats import register_stat
from .tools.chronos import Chronology
from .tools.magic import magic_naming, spell_out
from .tools.math import (ens_compatible, linspace_int, Id_Obs, partial_Id_Obs, round2,
                         with_recursion, with_rk4)
from .tools.matrices import CovMat
from .tools.randvars import RV, GaussRV
from .tools.stoch import rand, randn, set_seed
from .tools.viz import freshfig


# Documentation management
# ---
# # 1. Generation:
# $ pdoc --force --html --template-dir docs -o ./docs dapper
# $ open docs/index.html
# # 2. Hosting:
# Push updated docs to github.
# In the main github settings of the repo,
# go to the "GitHub Pages" section,
# and set the source to the docs folder.
def _find_demos(as_path=False):
    "Find all model demo.py scripts."
    lst = []
    for d in (rc.dirs.dapper/"mods").iterdir():
        x = d/"demo.py"
        if x.is_file():
            x = x.relative_to(rc.dirs.DAPPER)
            if not as_path:
                x = str(x.with_suffix("")).replace("/", ".")
            lst.append(x)
    return lst

# This generates a lot of warnings:
# """UserWarning: __pdoc__-overriden key ... does not exist in module""".
# AFAICT that's fine. https://github.com/pdoc3/pdoc/issues/206
# Alternative: Insert this at top of each script to exclude
# >>> if __name__ != "__main__":
# >>>     raise RuntimeError("This module may only be run as script.")
# and run pdoc with --skip-errors.
__pdoc__ = {
    "tools.remote.autoscaler": False,
    **{demo:False for demo in _find_demos()},
    "dapper.mods.KS.compare_schemes": False,
    "dapper.mods.LorenzUV.illust_LorenzUV": False,
    "dapper.mods.LorenzUV.illust_parameterizations": False,
    "dapper.mods.explore_props": False,
    "dapper.mods.QG.f90": False,
}
