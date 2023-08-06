==============
dummy-env-prep
==============

It can be hard to manage shell-script style python in a build or automated environment.  Wrap up requirements easily in one ``pip install`` and place it at the front of a Bamboo, Jenkins, or Ansible script.

This is meant as a demo.  Please fork for your own needs.

Getting Started
===============

1. Fork this project
2. ``pip install cookiecutter``
3. ``cookiecutter cookiecutter_template/``
4. Answer the questions
5. Fill out ``requirements.txt`` and ``README.rst`` appropriately
6. ``python setup.py sdist bdist_wheel clean --all upload``
7. ``pip install [my project]`` where needed <3
