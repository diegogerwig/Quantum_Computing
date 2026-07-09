from setuptools import setup, Extension
import qiskit.capi
import sys
import subprocess

def supports_no_warn_duplicate():
    try:
        result = subprocess.run(
            ["ld", "-no_warn_duplicate_libraries"],
            capture_output=True
        )
        return b"unknown option" not in result.stderr
    except Exception:
        return False

extra_link_args = []
if sys.platform == "darwin" and supports_no_warn_duplicate():
    extra_link_args = ["-Wl,-no_warn_duplicate_libraries"]

setup(
    name="qgss_circuit",
    ext_modules=[
        Extension(
            name="qgss_circuit",
            sources=["qgss_circuit.c"],
            include_dirs=[qiskit.capi.get_include()],
            define_macros=[("QISKIT_PYTHON_EXTENSION", "1")],
            extra_link_args=extra_link_args,
        )
    ],
)
