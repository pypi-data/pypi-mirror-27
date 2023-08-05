#!/bin/bash
set -e -x

WORKSPACE=`pwd`
# Change into temporary directory since we want to be outside of git
cd /tmp

PROJECT="my_project"
# Delete old project if necessary
if [ -d ${PROJECT}  ]; then
    rm -rf ${PROJECT}
fi

function run_common_tasks {
    cd ${1}
    python setup.py test
    python setup.py doctest
    python setup.py docs
    python setup.py --version
    python setup.py sdist
    python setup.py bdist
    if [[ "${COVERAGE}" == "true" && "${2}" != "false" ]]; then
        echo "Checking code style with flake8..."
        flake8 --count
    fi
    cd ..
}

# Setup a test project
putup ${PROJECT}
# Run some common tasks
run_common_tasks ${PROJECT}
# Try updating
putup --update ${PROJECT}
cd ${PROJECT}
git_diff=`git diff`
test ! -n "$git_diff"
# Try different project name than package name
putup MY_COOL_PROJECT -p ${PROJECT}
run_common_tasks MY_COOL_PROJECT
rm -rf MY_COOL_PROJECT
# Try forcing overwrite
putup --force --tox ${PROJECT}
# Try running Tox
if [[ "${DISTRIB}" == "ubuntu" ]]; then
    cd ${PROJECT}
    tox -e ${TOX_PYTHON_VERSION}
    cd ..
fi
# Try all kinds of extensions
rm -rf ${PROJECT}
putup --django ${PROJECT}
run_common_tasks ${PROJECT} false
rm -rf ${PROJECT}
putup --pre-commit ${PROJECT}
run_common_tasks ${PROJECT}
rm -rf ${PROJECT}
putup --travis ${PROJECT}
run_common_tasks ${PROJECT}
rm -rf ${PROJECT}
putup --gitlab ${PROJECT}
run_common_tasks ${PROJECT}

# Test Makefile for sphinx
PROJECT="project_with_docs"
# Delete old project if necessary
if [ -d ${PROJECT}  ]; then
    rm -rf ${PROJECT}
fi
putup  ${PROJECT}
cd ${PROJECT}/docs
PYTHONPATH=.. make html

# Test update from PyScaffold version 2.0
if [[ "${DISTRIB}" == "conda" && "${PYTHON_VERSION}" == "2.7" ]]; then
    TMPDIR="update_test"
    mkdir ${TMPDIR}; cd ${TMPDIR}
    git clone --branch v0.2.1 https://github.com/blue-yonder/pydse.git pydse
    cp ${TRAVIS_BUILD_DIR}/tests/misc/pydse_setup.cfg pydse/setup.cfg
    putup --update pydse
    conda install --yes nomkl numpy scipy matplotlib libgfortran
    pip install -v -r pydse/requirements.txt
    run_common_tasks pydse
    cd ..
    rm -rf ${TMPDIR}
fi

# Test namespace package
PROJECT="nested_project"
# Delete old project if necessary
if [ -d ${PROJECT}  ]; then
    rm -rf ${PROJECT}
fi

putup ${PROJECT} -p my_package --namespace com.blue_yonder
run_common_tasks ${PROJECT}
rm -rf ${PROJECT}

# Test namespace + cookiecutter
COOKIECUTTER_URL="https://github.com/FlorianWilhelm/cookiecutter-pypackage.git"
PROJECT="project_with_cookiecutter_and_namespace"
# Delete old project if necessary
if [ -d ${PROJECT}  ]; then
    rm -rf ${PROJECT}
fi

echo ${COOKIECUTTER_URL}

putup ${PROJECT} --namespace nested.ns \
  --cookiecutter ${COOKIECUTTER_URL}

if [ -d "${PROJECT}/src/${PROJECT}" ]; then
  echo "Package should be nested, but it is not!"
  exit 1
fi

rm -rf ${PROJECT}

echo "System test successful!"
cd ${WORKSPACE}

if [[ "${COVERAGE}" == "true" ]]; then
    echo "Checking code style with flake8..."
    flake8 --count
fi
