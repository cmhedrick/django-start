#!/usr/bin/env python

import subprocess
import sys
import os


class Project(object):

    def __init__(self):
        self.project = raw_input('Project Name: ')
        self.project_site = 'site_' + self.project
        self.project_app = 'app_' + self.project
        self.python = self.set_python()
        self.host = raw_input('Username for webfaction: ')
        self.dir = './site_{pro_name}/'.format(pro_name=self.project)
        self.settings = self.dir + 'settings.py'
        self.settings_pro = self.dir + 'settings_pro.py'
        self.install()
        self.mod_settings()
        self.replace_settings()
        self.make_requirements()

    def set_python(self):
        python = raw_input('Python Version (python2 or python3): ')
        python = python.lower().replace(' ', '')[0:7]
        if python == 'python2' or python == 'python3':
            return python
        else:
            raise PythonVersionFail(python, 'Is not a valid version of python')

    def install(self):
        if self.python == 'python2':
            subprocess.call(['virtualenv', 'env'])
            subprocess.call(['env/bin/pip', 'install', 'django'])
        elif self.python == 'python3':
            subprocess.call(['virtualenv', '-p', 'python3', 'env'])
            subprocess.call(['env/bin/pip3', 'install', 'django'])
        subprocess.call(
            [
                'env/bin/django-admin',
                'startproject',
                self.project_site,
                '.'
            ]
        )
        subprocess.call(
            [
                'env/bin/django-admin',
                'startapp',
                self.project_app
            ]
        )

    def mod_settings(self):
        i = 0
        with open(self.settings, 'r') as f:
            with open((self.settings + '.back'), 'w') as f2:
                for line in f:
                    i += 1
                    if i == 58:
                        f2.write(
                            "        \'DIRS\':"
                            " [(os.path.join("
                            "BASE_DIR,"
                            "\'" + self.project_site +
                            "\', \'templates\'))],\n"
                        )
                    else:
                        f2.write(line)
                f2.write(
                    'STATIC_ROOT = os.path.join(BASE_DIR, \'static\')\n'
                )
                f2.write(
                    "STATICFILES_DIRS = [\n"
                    "    ("
                    "os.path.join(BASE_DIR, \'" +
                    self.project_site +
                    "\', \'static\'))\n"
                    "]\n"
                )
                f2.write('MEDIA_URL = \'/media/\'\n')
                f2.write('MEDIA_ROOT = os.path.join(BASE_DIR, \'media\')\n')
                f2.write(
                    'TEMPLATE_DIRS = [os.path.join(BASE_DIR, \'templates\')]\n'
                )
                f2.write('\n')
                f2.write('PRODUCTION = False\n')
                f2.write('\n')
                f2.write('if PRODUCTION:\n')
                f2.write(
                    (
                        "    sys.path.insert"
                        "(0, (BASE_DIR + \'/" +
                        self.project_site +
                        "/\'))\n"
                    )
                )
                f2.write('    from settings_pro import *')
                with open(self.settings_pro, 'w') as f3:
                    f3.write('import site\n')
                    f3.write('import os\n')
                    f3.write('# env site packages\n')
                    f3.write(
                        (
                            "site.addsitedir(\'/home/" + self.host +
                            "/webapps/" + self.project +
                            "/" + self.project +
                            "/env/lib/python2.7/site-packages\')"
                            "\n"
                        )
                    )
                    f3.write('\n')
                    f3.write('# env activate this\n')
                    f3.write(
                        (
                            "activate_this = os.path.expanduser(\'"
                            "/home/" + self.host +
                            "/webapps/" + self.project +
                            "/" + self.project +
                            "/env/bin/"
                            "activate_this.py\')\n"
                        )
                    )
                    f3.write(
                        (
                            "DATABASES = {\n"
                            "    \'default\': {\n"
                            "    \'ENGINE\': \'django.db.backends.postgresql"
                            "_psycopg2\',\n"
                            "    \'NAME\': \'\',\n"
                            "    \'USER\': \'\',\n"
                            "    \'PASSWORD\': \'\',\n"
                            "    \'HOST\': \'\',\n"
                            "    \'PORT\': \'\',\n"
                            "    }\n"
                            "}\n"
                        )
                    )
                    f3.write(
                        (
                            "MEDIA_ROOT = \'/home/" + self.host +
                            "/webapps/" + (self.project + "_media") + "/\'\n" +
                            "STATIC_ROOT = \'/home/" + self.host +
                            "/webapps/" + (self.project + "_static") + "/\'\n"
                        )
                    )

    def replace_settings(self):
        subprocess.call(['rm', self.settings])
        subprocess.call(['mv', (self.settings + '.back'), self.settings])

    def sync(self):
        subprocess.call(['rm', (self.project + '/project.db')])
        subprocess.call(
            [
                'env/bin/python',
                (self.project + '/manage.py'),
                'migrate'
            ]
        )
        print 'Migrated'
        subprocess.call(
            [
                'env/bin/python',
                (self.project + '/manage.py'),
                'createsuperuser'
            ]
        )

    def make_requirements(self):
        os.system('env/bin/pip freeze > ./requirements.txt')
        subprocess.call(
            [
                'cp',
                './requirements.txt',
                './requirements_pro.txt'
            ]
        )
        os.system(
            (
                'echo \'psycopg2\' >> ./requirements_pro.txt'
            )
        )
        print 'Requirement Files Made'


class BaseException(Exception):

    def __init__(self, message, errors):
        super(BaseException, self).__init__(message)
        self.errors = errors


class PythonVersionFail(BaseException):
    pass

Project()

