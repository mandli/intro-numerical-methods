#!/usr/bin/env
"""Basic test script that runs all notebooks."""

import os
import subprocess
import tempfile
import sys
import nbformat
import doctest

if sys.version_info >= (3,0):
    kernel = 'python3'
else:
    kernel = 'python2'

# Note we leave out the python intro as there are purposeful exceptions
notebooks = ["00_intro_numerical_methods.ipynb",
             # "01_intro_to_python.ipynb",
             "02_NumPy.ipynb",
             "03_matplotlib.ipynb",
             "04_error.ipynb",
             "05_root_finding_optimization.ipynb",
             "06_interpolation.ipynb",
             "07_differentiation.ipynb",
             "08_quadrature.ipynb",
             "09_ODE_ivp_part2.ipynb",
             "09_ODE_ivp_part1.ipynb",
             "10_LA_intro.ipynb",
             "11_LA_QR.ipynb",
             "12_LA_conditioning_stability.ipynb",
             "13_LA_eigen.ipynb",
             "14_LA_iterative.ipynb",
             "15_LA_gaussian.ipynb",
             "16_ODE_BVP.ipynb",]

def _notebook_run(path):
    """Execute a notebook via nbconvert and collect output.
       :returns (parsed nb object, execution errors)
    """
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=60",
                "--ExecutePreprocessor.kernel_name="+kernel,
                "--output", fout.name, path]
        subprocess.check_call(args)

        fout.seek(0)
        nb = nbformat.reads(fout.read().decode('utf-8'), nbformat.current_nbformat)

    errors = [output for cell in nb.cells if "outputs" in cell
              for output in cell["outputs"]
              if output.output_type == "error"]

    return nb, errors

def run_tests():

    for filename in notebooks:
        if (filename.split('.')[-1] == 'ipynb'):
            nb, errors = _notebook_run(filename)
            if errors != []:
                raise(Exception)


if __name__ == '__main__':
    run_tests()