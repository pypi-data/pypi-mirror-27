#-*- coding: utf-8 -*-
"""
@file
@brief Defines a set of module for teaching purpose.
"""
from ..installhelper.module_install import ModuleInstall


def teachings_set():
    """
    modules implemented for my teachings, it requires the modules in set *ml*
    """
    mod = [
        ModuleInstall(
            "jyquickhelper", "pip", purpose="Helpers for Jupyter notebooks.", usage="TEACH"),
        ModuleInstall(
            "pyquickhelper", "pip", purpose="helpers to generation documentation", usage="TEACH"),
        ModuleInstall(
            "tkinterquickhelper", "pip", purpose="windows on the top of tkinter", usage="TEACH"),
        ModuleInstall(
            "pymyinstall", "pip", purpose="easy installation of modules including Windows", usage="TEACH"),
        ModuleInstall("pymmails", "pip",
                      purpose="read/send emails", usage="TEACH"),
        ModuleInstall(
            "pyensae", "pip", purpose="helpers, Hadoop, SQL, financial times series, ...", usage="TEACH"),
        ModuleInstall("pyrsslocal", "pip",
                      purpose="RSS readers", usage="TEACH"),
        ModuleInstall(
            "code_beatrix", "pip", purpose="teaching programming to kids, lesenfantscodaient.fr", usage="TEACH"),
        ModuleInstall(
            "actuariat_python", "pip", purpose="teachings, insurance examples", usage="TEACH"),
        ModuleInstall("ensae_teaching_cs", "pip",
                      purpose="teachings, introduction to programming, machine learning, map/reduce", usage="TEACH"),
        ModuleInstall("jupytalk", "pip",
                      purpose="materials for presentations", usage="TEACH"),
        ModuleInstall("mlstatpy", "pip",
                      purpose="materials for machine learning", usage="TEACH"),
        ModuleInstall("teachpyx", "pip",
                      purpose="materials for teachings", usage="TEACH"),
        ModuleInstall("ensae_projects", "pip",
                      purpose="single use code", usage="TEACH"),
    ]
    #
    return [_ for _ in mod if _ is not None]
