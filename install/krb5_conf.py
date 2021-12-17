from __future__ import (
    print_function,
    absolute_import,
)

import classes
import logging
import dns

from classes import format_netloc

NoneType = type(None)

logger = logging.getLogger(__name__)

SUCCESS = 0
CLIENT_INSTALL_ERROR = 1
CLIENT_NOT_CONFIGURED = 2
CLIENT_ALREADY_CONFIGURED = 3
CLIENT_UNINSTALL_ERROR = 4  # error after restoring files/state

SECURE_PATH = (
    "/bin:/sbin:/usr/kerberos/bin:/usr/kerberos/sbin:/usr/bin:/usr/sbin"
)

# global variables
hostname = None
hostname_source = None
nosssd_files = None
dnsok = False
cli_domain = None
cli_server = None
subject_base = None
cli_realm = None
cli_kdc = None
client_domain = None
cli_basedn = None
# end of global variables





def configure_krb5_conf(
        cli_realm, cli_domain, cli_server, cli_kdc, dnsok,
        filename, client_domain, client_hostname, force=False,
        configure_sssd=True):
    # First, write a snippet to krb5.conf.d.
    configure_krb5_snippet()

    # Then, perform the rest of our configuration into krb5.conf itself.
    krbconf = SambaChangeConf("Samba Installer")
    krbconf.setOptionAssignment((" = ", " "))
    krbconf.setSectionNameDelimiters(("[", "]"))
    krbconf.setSubSectionDelimiters(("{", "}"))
    krbconf.setIndent(("", "  ", "    "))

    opts = [
        {
            'name': 'comment',
            'type': 'comment',
            'value': 'File modified by samba-client-install'
        },
        krbconf.emptyLine(),
    ]

    if os.path.exists(paths.COMMON_KRB5_CONF_DIR):
        opts.extend([
            {
                'name': 'includedir',
                'type': 'option',
                'value': paths.COMMON_KRB5_CONF_DIR,
                'delim': ' '
            }
        ])

    # SSSD include dir
    if configure_sssd:
        opts.extend([
            {
                'name': 'includedir',
                'type': 'option',
                'value': paths.SSSD_PUBCONF_KRB5_INCLUDE_D_DIR,
                'delim': ' '
            },
            krbconf.emptyLine()])

    # [libdefaults]
    libopts = [
        krbconf.setOption('default_realm', cli_realm)
    ]
    if not dnsok or not cli_kdc or force:
        libopts.extend([
            krbconf.setOption('dns_lookup_realm', 'false'),
        ])
    else:
        libopts.extend([
            krbconf.setOption('dns_lookup_realm', 'true'),
        ])
    libopts.extend([
        krbconf.setOption('rdns', 'false'),
        krbconf.setOption('dns_canonicalize_hostname', 'false'),
        krbconf.setOption('dns_lookup_kdc', 'true'),
        krbconf.setOption('ticket_lifetime', '24h'),
        krbconf.setOption('forwardable', 'true'),
        krbconf.setOption('udp_preference_limit', '0')
    ])

    # Configure KEYRING CCACHE if supported
    if kernel_keyring.is_persistent_keyring_supported():
        logger.debug("Enabling persistent keyring CCACHE")
        libopts.append(krbconf.setOption('default_ccache_name',
                                         'KEYRING:persistent:%{uid}'))

    opts.extend([
        krbconf.setSection('libdefaults', libopts),
        krbconf.emptyLine()
    ])

    # the following are necessary only if DNS discovery does not work
    kropts = []
    if not dnsok or not cli_kdc or force:
        # [realms]
        for server in cli_server:
            kropts.extend([
                krbconf.setOption('kdc', classes.format_netloc(server, 88)),
                krbconf.setOption('master_kdc',
                                  ipautil.format_netloc(server, 88)),
                krbconf.setOption('admin_server',
                                  ipautil.format_netloc(server, 749)),
                krbconf.setOption('kpasswd_server',
                                  ipautil.format_netloc(server, 464))
            ])
        kropts.append(krbconf.setOption('default_domain', cli_domain))

    kropts.append(
        krbconf.setOption('pkinit_anchors',
                          'FILE:%s' % paths.KDC_CA_BUNDLE_PEM))
    kropts.append(
        krbconf.setOption('pkinit_pool',
                          'FILE:%s' % paths.CA_BUNDLE_PEM))
    ropts = [{
        'name': cli_realm,
        'type': 'subsection',
        'value': kropts
    }]

    opts.append(krbconf.setSection('realms', ropts))
    opts.append(krbconf.emptyLine())

    # [domain_realm]
    dropts = [
        krbconf.setOption('.{}'.format(cli_domain), cli_realm),
        krbconf.setOption(cli_domain, cli_realm),
        krbconf.setOption(client_hostname, cli_realm)
    ]

    # add client domain mapping if different from server domain
    if cli_domain != client_domain:
        dropts.extend([
            krbconf.setOption('.{}'.format(client_domain), cli_realm),
            krbconf.setOption(client_domain, cli_realm)
        ])

    opts.extend([
        krbconf.setSection('domain_realm', dropts),
        krbconf.emptyLine()
    ])

    logger.debug("Writing Kerberos configuration to %s:", filename)
    logger.debug("%s", krbconf.dump(opts))

    krbconf.newConf(filename, opts)
    # umask applies when creating a new file but we want 0o644 here
    os.chmod(filename, 0o644)
