"""
Common Authentication settings

"""

from django_auth_ldap.config import LDAPSearch, PosixGroupType
import ldap

# Authentication settings
AUTH_LDAP_SERVER_URI = "ldap://data.sns.gov/"
AUTH_LDAP_BIND_DN = ''
AUTH_LDAP_BIND_PASSWORD = ''

AUTH_LDAP_GLOBAL_OPTIONS = { ldap.OPT_X_TLS_REQUIRE_CERT : ldap.OPT_X_TLS_NEVER,}

## User:
AUTH_LDAP_USER_DN_TEMPLATE = 'uid=%(user)s,ou=Users,dc=sns,dc=ornl,dc=gov'
AUTH_LDAP_ALWAYS_UPDATE_USER = True

## Groups

AUTH_LDAP_GROUP_SEARCH = LDAPSearch( 'ou=Groups,dc=sns,dc=ornl,dc=gov',
                                     ldap.SCOPE_SUBTREE, '(objectClass=posixGroup)')
#AUTH_LDAP_GROUP_TYPE = PosixGroupType()
AUTH_LDAP_GROUP_TYPE = PosixGroupType(name_attr='cn')

# Populates table groups!
AUTH_LDAP_MIRROR_GROUPS = True
# AUTH_LDAP_CACHE_GROUPS = True
# AUTH_LDAP_GROUP_CACHE_TIMEOUT = 300


# TODO : Those are permission for the admin interface! Need to understand the types of users
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    # Has access to portal
    "is_active": "cn=SNS_Neutron,ou=Groups,dc=sns,dc=ornl,dc=gov",
    # Has access to Admin
    "is_staff": "cn=SNS_Neutron_dev,ou=Groups,dc=sns,dc=ornl,dc=gov",
    # Has access to Admin and can change permissions
    "is_superuser": "cn=SNS_Neutron_dev,ou=Groups,dc=sns,dc=ornl,dc=gov"
}

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
   "first_name": "cn",
   "email":  "description",
   "last_name":      "gecos"
}

# Populate group permissions based on the LDAP
AUTH_LDAP_FIND_GROUP_PERMS = True

LOGIN_URL = 'users:login'
