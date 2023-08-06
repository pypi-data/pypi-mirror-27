#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'afp-cli',
        version = '370.315',
        description = 'Command line client for AWS federation proxy api',
        long_description = '=======\nAFP CLI\n=======\n\n.. image:: https://travis-ci.org/ImmobilienScout24/afp-cli.png?branch=master\n   :alt: Travis build status image\n   :target: https://travis-ci.org/ImmobilienScout24/afp-cli\n\n.. image:: https://coveralls.io/repos/ImmobilienScout24/afp-cli/badge.png?branch=master\n    :alt: Coverage status\n    :target: https://coveralls.io/r/ImmobilienScout24/afp-cli?branch=master\n\n.. image:: https://landscape.io/github/ImmobilienScout24/afp-cli/master/landscape.svg?style=flat\n   :target: https://landscape.io/github/ImmobilienScout24/afp-cli/master\n   :alt: Code Health\n\n.. image:: https://img.shields.io/pypi/v/afp-cli.svg\n   :alt: Version\n   :target: https://pypi.python.org/pypi/afp-cli\n\nOverview\n========\n\nThe AFP CLI is the command line interface to access the\nAWS Federation Proxy (AFP).\n\nIts main use case is starting a new shell where your temporary\nAWS credentials have been exported into the environment.\n\nInstallation\n============\n\nThe tool is `hosted on PyPi <https://pypi.python.org/pypi/afp-cli>`_ and can be\ninstalled using the usual Python specific mechanisms, e.g.:\n\n.. code-block:: console\n\n   $ pip install afp-cli\n\nConfiguration\n=============\n\nThe ``afp`` command can be configured through yaml files in\nthe following directories:\n\n* ``/etc/afp-cli/*.yaml`` (global configuration)\n* ``$HOME/.afp-cli/*.yaml`` (per-user configuration)\n\nThe yaml files are read in lexical order and merged via\n`yamlreader <https://github.com/ImmobilienScout24/yamlreader>`_.\nThe following configuration options are supported:\n\n* ``api_url: <api-url>``\n  Defaults to lookup a FQDN of a host named ``afp`` via DNS and construct\n  the server url from it: ``https://{FQDN}/afp-api/latest``\n  The specified url must contain full server url (not just the FQDN).\n  This option always takes precedence over ``server``\n* ``server: <server>``\n  The AFP server to use. No default value.\n  If not overridden by ``api_url`` (see above), ``api_url`` will\n  become ``http://<server>//afp-api/latest``\n* ``user: <username>``\n  Defaults to the currently logged in user-name\n* ``password-provider: <provider>``\n  Viable options are: ``prompt`` (default) to prompt for the password during\n  every interaction with the AFP server or ``keyring`` to use the Python\n  ``keyring`` module. For more info about using the ``keyring`` module, see\n  below.\n\nExample:\n\n.. code-block:: yaml\n\n    user: myuser\n    api_url: https://afp-server.my.domain/afp-api/latest\n    password-provider: keyring\n\n\nUsage\n=====\n\nGet Help Text\n-------------\n\n.. code-block:: console\n\n    $ afp [-h | --help]\n\nList Available Account Names and Roles\n--------------------------------------\n\nFor the currently logged-in user:\n\n.. code-block:: console\n\n    $ afp\n\nThe same for another user:\n\n.. code-block:: console\n\n    $ afp --user=username\n\nOutput format:\n\n::\n\n    <accountname>    <role1>,<role2>,...,<roleN>\n\nExample output:\n\n::\n\n    abc_account    some_role_in_abc_account\n    xyz_account    some_role_in_yxz_account,another_role_in_xyz\n\nObtain AWS Credentials\n----------------------\n\nThis starts a subshell in which the credentials have been exported into the\nenvironment. Use the ``exit`` command or press **CTRL+D** to terminate the\nsubshell.\n\nUse credentials for currently logged in user and specified account and role:\n\n.. code-block:: console\n\n    $ afp accountname rolename\n\nUse credentials for the currently logged in user for the *first* role:\n\n.. code-block:: console\n\n    $ afp accountname\n\nAs above, but specifying a different user:\n\n.. code-block:: console\n\n    $ afp --user=username accountname rolename\n\nSpecify the URL of the AFP server, overriding any config file:\n\n.. code-block:: console\n\n    $ afp --api-url=https://afp-server.my.domain/afp-api/latest\n\nShow and Export\n---------------\n\nIn case you don\'t want to start a subshell or are using something other than\nbash, you can use ``--show`` or ``--export`` to display the credentials. You\ncan use the usual UNIX tools to add/remove them from your environment.\n``--show`` will just show them and ``--export`` will show them in a format\nsuitable for an export into your environment, i.e. prefixed with ``export`` for\nUNIX and ``set`` for Windows.\n\n\n.. code-block:: console\n\n   $ afp --show <myaccount> [<myrole>]\n   Password for myuser:\n   AWS_VALID_SECONDS=\'600\'\n   AWS_SESSION_TOKEN=\'XXX\'\n   AWS_SECURITY_TOKEN=\'XXX\'\n   AWS_SECRET_ACCESS_KEY=\'XXX\'\n   AWS_EXPIRATION_DATE=\'1970-01-01T01:00:00Z\'\n   AWS_ACCESS_KEY_ID=\'XXX\'\n\n.. code-block:: console\n\n   $ afp --export <myaccount> [<myrole>]\n   Password for myuser:\n   export AWS_VALID_SECONDS=\'600\'\n   export AWS_SESSION_TOKEN=\'XXX\'\n   export AWS_SECURITY_TOKEN=\'XXX\'\n   export AWS_SECRET_ACCESS_KEY=\'XXX\'\n   export AWS_EXPIRATION_DATE=\'1970-01-01T01:00:00Z\'\n   export AWS_ACCESS_KEY_ID=\'XXX\'\n\n\nThe following examples work in zsh, to add and remove them from your\nenvironment:\n\nAdding credentials:\n\n.. code-block:: console\n\n   $ eval $(afp --export <accountname>)\n\nRemoving them again:\n\n.. code-block:: console\n\n    $ env | grep AWS | cut -f 1 -d\'=\' | while read line ; do ; unset $line ; done ;\n\nWrite to AWS Credentials File\n-----------------------------\n\nThe AWS tools read credentials specified with ``aws configure`` from a local\nfile named ``credentials`` in a folder named ``.aws`` in your home directory.\nThe afp-cli tool can write your temporary credentials to this file.\n\n.. code-block:: console\n\n   $ afp --write <myaccount> [<myrole>]\n\nConfiguration Settings and Precedence\n-------------------------------------\n\nPlease read the section on `Configuration Settings and Precedence\n<https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#config-settings-and-precedence>`_\nfrom the AWS documentation.\n\nInterface with the System Keyring\n---------------------------------\n\nStarting with version ``1.3.0``, experimental support for the `Python keyring\nmodule <https://pypi.python.org/pypi/keyring>`_ has been implemented. This has\nbeen tested with the Gnome Keyring and Max OS X Keychain but supposedly also\nworks with Windows Credential Vault. You can configure this feature using the\nconfig file as shown above or with a command-line switch.\n\nExample command-line:\n\n.. code-block:: console\n\n   $ afp --password-provider keyring\n   No password found in keychain, please enter it now to store it.\n   Password for user:\n\nYou will be prompted for your password the first time. Note\nthat if you fail to enter the password correctly, the incorrect version will be\nstored. Note further that if you are using the Gnome-Keychain you can use the\ntool ``seahorse`` to update and delete saved passwords, in this case for the\nservice ``afp``.\n\nKeyring on MacOS X\n~~~~~~~~~~~~~~~~~~\nOn some MacOS systems, storing the password works fine, but fetching it fails with `Can\'t fetch password from system <https://github.com/ImmobilienScout24/afp-cli/issues/65>`_. This is due to a `change in the \'keyring\' module <https://github.com/jaraco/keyring/issues/219>`_, introduced in version 9.0. As a workaround, downgrade to the previous version with ``pip install keyring==8.7``\n\nKeyring with Gnome-Keychain\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\nThere is an intricate caveat when using the ``keyring`` module with\nGnome-Keychain. But before discussing this, it is important to mention that\nthe keyring module uses another module, namely ``secretstorage`` under the\nhood.\n\nIn order for the ``keyring`` module to correctly use the Gnome Keychain the\nPython module `PyGObject aka gi\n<https://wiki.gnome.org/action/show/Projects/PyGObject?action=show&redirect=PyGObject>`_\nis required. As stated on the project website: "PyGObject is a Python extension\nmodule that gives clean and consistent access to the entire GNOME software\nplatform through the use of GObject Introspection." Now, unfortunately, even\nthough this project is `available on PyPi\n<https://pypi.python.org/pypi/PyGObject>`_ it can not be installed from there\nusing ``pip`` due to issues with the build system. It is however available as a\nsystem package for Ubuntu distributions as ``python-gi``.\n\nLong story short, in order to use the ``keyring`` module from ``afp-cli`` you need to have\nthe ``gi`` module available to your Python interpreter. You can achieve this,\nfor example, by doing a global install of ``afp-cli`` using something like\n``sudo pip install afp-cli`` or install it into a virtual environment that uses\nthe system site packages because it has been created with the\n``--system-site-packages`` flag. In case the ``gi`` module is not available and\nyou try to use the ``keyring`` module anyway, ``afp-cli`` will exit with an\nappropriate error message.  Lastly, if in doubt, you can use the ``--debug``\nswitch to check at runtime which backend was selected.\n\n\nLicense\n=======\n\nCopyright 2015,2016 Immobilien Scout GmbH\n\nLicensed under the Apache License, Version 2.0 (the "License"); you may not use\nthis file except in compliance with the License. You may obtain a copy of the\nLicense at\n\nhttp://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software distributed\nunder the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR\nCONDITIONS OF ANY KIND, either express or implied. See the License for the\nspecific language governing permissions and limitations under the License.\n\nSee Also\n========\n\nSee Hologram_ for another solution that brings temporary AWS credentials onto\ndeveloper desktops.\n\n.. _Hologram: https://github.com/AdRoll/hologram\n',
        author = 'Stefan Neben, Tobias Vollmer, Stefan Nordhausen, Enrico Heine, Valentin Haenel',
        author_email = 'stefan.neben@immobilienscout24.de, tobias.vollmer@immobilienscout24.de, stefan.nordhausen@immobilienscout24.de, enrico.heine@immobilienscout24.de, valentin.haenel@immobilienscout24.de',
        license = 'Apache License 2.0',
        url = 'https://github.com/ImmobilienScout24/afp-cli',
        scripts = [
            'scripts/afpv2',
            'scripts/afp'
        ],
        packages = ['afp_cli'],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6'
        ],
        entry_points = {
            'console_scripts': ['afpv2=afp_cli.cliv2:main']
        },
        data_files = [],
        package_data = {},
        install_requires = [
            'docopt',
            'keyring',
            'requests',
            'secretstorage!=2.2.0',
            'yamlreader>=3.0.1'
        ],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = [],
    )
