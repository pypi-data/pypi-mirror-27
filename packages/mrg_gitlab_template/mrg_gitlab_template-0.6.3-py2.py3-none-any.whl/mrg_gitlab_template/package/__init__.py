""" The {{package}} short description. """

from ._version import get_versions

__version__ = get_versions()['version']
# __status__ = 'Release'
__status__ = '+++ Testing +++'

__pkgname__ = '{{package}}'
__author__ = '{{author}}'
__email__ = '{{email}}'
__docurl__ = 'http://{{group}}.{{pages_domain}}/{{package}}/'
__giturl__ = 'https://{{gitlab_url}}/{{group}}/{{package}}'

del get_versions
