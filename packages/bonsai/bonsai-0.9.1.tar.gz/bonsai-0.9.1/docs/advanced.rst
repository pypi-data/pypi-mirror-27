Advanced Usage
**************

.. module:: bonsai

This document covers some of the more advanced features of Bonsai.

Authentication mechanisms
=========================

There are several authentication mechanisms, which can be used with Bonsai. The selected mechanism
with the necessary credentials can be set with the :meth:`LDAPClient.set_credentials` method.

Simple bind
-----------

The simplest way to authenticate with an LDAP server is using the SIMPLE mechanism which requires a
bind DN and a password::

    >>> import bonsai
    >>> client = bonsai.LDAPClient()
    >>> client.set_credentials("SIMPLE", ("cn=user,dc=bonsai,dc=test", "secret"))
    >>> client.connect()
    <bonsai.ldapconnection.LDAPConnection object at 0x7fed62b19828>

.. warning::
    Be aware that during the authentication the password is sent to the server in clear text form.
    It is ill-advised to use simple bind without secure channel (TLS/SSL) in production. 

Simple Authentication and Security Layer
----------------------------------------

The OpenLDAP library uses the Simple Authentication and Security Layer (`SASL`_) (while the WinLDAP
uses the similar `SSPI`_) to provide different authentication mechanisms. Of course to use a
certain mechanism it has to be supported both the client and the server. To learn which mechanisms
are accessible from the server, check the root DSE's `supportedSASLMechanisms` value::

    >>> client.get_rootDSE()['supportedSASLMechanisms']
    ['GSS-SPNEGO', 'GSSAPI', 'DIGEST-MD5', 'NTLM']

.. note::
    On Unix systems, make sure that the necessary libraries of the certain mechanism are also
    installed on the client. (E.g. `libsasl2-modules-gssapi-mit` or `cyrus-sasl-gssapi`)

.. _SASL: https://tools.ietf.org/html/rfc4422
.. _SSPI: https://msdn.microsoft.com/en-us/library/windows/desktop/aa380493%28v=vs.85%29.aspx


DIGEST-MD5 and NTLM
^^^^^^^^^^^^^^^^^^^

The DIGEST-MD5 and the NTLM mechanisms are challenge-response based authentications. Nowadays they
are considered as weak security protocols, but still popular ones. An example of using NTLM::

    >>> client.set_credentials("NTLM", ("user", "secret", None, None))
    >>> client.connect().whoami()
    "dn:cn=user,dc=bonsai,dc=test"

The credentials consist of a username, a password, an optional realm name and an optional
authorization ID. Using an authorization ID during the bind only useful for DIGEST-MD5, NTLM does
not support it.

    >>> client.set_credentials("DIGEST-MD5", ("user", "secret", None, "u:root"))
    >>> client.connect().whoami()
    "dn:cn=admin,dc=bonsai,dc=test"

GSSAPI and GSS-SPNEGO
^^^^^^^^^^^^^^^^^^^^^

GSSAPI uses Kerberos tickets to authenticate to the server. To use GSSAPI or GSS-SPNEGO the client
must be Kerberos-aware, which means the necessary Kerberos tools and libraries have to be
installed, and the proper configuration has to be set. (Typically, the configuration is in the
`/etc/krb5.conf` on a Unix system). GSS-SPNEGO mechanism can negotiate a common authentication
method between server and client.

Basically, to start a GSSAPI authentication a ticket granting ticket (TGT) needs to be already
acquired by the client with the help of the command-line `kinit` tool::

    [noirello@bonsai.test ~]$ kinit admin@BONSAI.TEST
    Password for admin@BONSAI.TEST:

The acquired TGT can be listed with `klist`::

    [noirello@bonsai.test ~]$ klist 
    Ticket cache: FILE:/tmp/krb5cc_1000
    Default principal: admin@BONSAI.TEST

    Valid starting     Expires            Service principal
    22/02/16 22:06:14  23/02/16 08:06:14  krbtgt/BONSAI.TEST@BONSAI.TEST
        renew until 23/02/16 22:06:12

After successfully acquire a TGT, the module can used it for authenticating:

    >>> import bonsai
    >>> client = bonsai.LDAPClient()
    >>> client.set_credentials("GSSAPI", (None, None, None, None))
    >>> client.connect().whoami()
    'dn:cn=admin,dc=bonsai,dc=test'

In normal case as you can see the passed credentials with the exception of the authorization ID are
irrelevant -- at least on a Unix system, the underlying SASL library figures it out on its own. The
module's client can only interfere with the authorization ID:

    >>> client.set_credentials("GSSAPI", (None, None, None, "u:chuck"))
    >>> client.connect().whoami()
    'dn:cn=chuck,ou=nerdherd,dc=bonsai,dc=test'

But on a Windows system (by default) or if Bonsai is built with the optional Kerberos headers, then
it is possible to requesting a TGT with the module's client if username, password and realm name
are all provided:

    >>> client = bonsai.LDAPClient()
    >>> client.set_credentials("GSSAPI", ("admin", "secret", "BONSAI.TEST", None))
    >>> client.connect().whoami()
    'dn:cn=admin,dc=bonsai,dc=test'

Please note that the Kerberos realm names are typically uppercase with few exceptions.

.. note::
    Automatic TGT requesting only accessible on Unix systems if the optional Kerberos headers are
    provided during the module's build.
  
EXTERNAL
^^^^^^^^

With EXTERNAL mechanism TLS certifications are used to authenticate the user. In certain cases (e.g
the remote server is an OpenLDAP directory) the EXTERNAL option is presented as an available SASL
mechanism only when the client have built up a TLS connection with the server and already set a
client cert.

    >>> client = bonsai.LDAPClient("ldap://bonsai.test", tls=True)
    >>> client.set_ca_cert_dir('/etc/openldap/certs')
    >>> client.set_ca_cert("RootCACert")
    >>> client.set_client_cert("BonsaiTestUser")
    >>> client.set_client_key("./key.txt")
    >>> client.get_rootDSE()['supportedSASLMechanisms']
    ['GSS-SPNEGO', 'GSSAPI', 'DIGEST-MD5', 'EXTERNAL', 'NTLM']   
    >>> client.set_credentials("EXTERNAL", (None,))
    >>> client.connect()
    <bonsai.ldapconnection.LDAPConnection object at 0x7f006ad3d888>

For EXTERNAL mechanism only one element -- the authorization ID -- is passed in a tuple as
credential.
    
    >>> client.set_credentials("EXTERNAL", ("u:chuck",))
    >>> client.connect()
    >>> client.connect().whoami()
    'dn:cn=chuck,ou=nerdherd,dc=bonsai,dc=test'


The proper way of setting the certifications is depend on the TLS implementation that the LDAP
library uses. Please for more information see :ref:`tls-settings`.

.. _tls-settings:

TLS settings
============

The TLS related methods -- :meth:`LDAPClient.set_ca_cert_dir`, :meth:`LDAPClient.set_ca_cert`,
:meth:`LDAPClient.set_client_cert` and :meth:`LDAPClient.set_client_key` -- are expecting different
inputs depending on which TLS library is used by the LDAP library.

To find out which TLS library is used call :func:`bonsai.get_tls_impl_name`.

.. rubric:: GnuTLS and OpenSSL

For GnuTLS and OpenSSL the :meth:`LDAPClient.set_ca_cert` and :meth:`LDAPClient.set_client_cert`
are expecting file paths that link to certification files in PEM-format.

The :meth:`LDAPClient.set_ca_cert_dir` works only for OpenSSL if the content of provided
directory is symbolic links of certifications that are generated by the `c_rehash` utility.

.. rubric:: Mozilla NSS

When using Mozilla NSS the input of :meth:`LDAPClient.set_ca_cert_dir` is the path of the directory
containing the NSS certificate database (that is created with the `certutil` command).

The :meth:`LDAPClient.set_ca_cert` and :meth:`LDAPClient.set_client_cert` can be used to select the
certificate with their names in the certificate database.

If the client certificate is password protected, then the input of
:meth:`LDAPClient.set_client_key` should be a path to the file that contains the password in clear
text format.

.. rubric:: Microsoft Schannel

Unfortunately, none of the listed TLS modules are effective on Microsoft Windows. The WinLDAP
library automatically searches for the corresponding certificates in the cert store. All of the
necessary certificates have to be loaded manually before the client tries to use them. 

.. _ldap-controls:

LDAP controls
=============

Several LDAP controls can be used to extend and improved the basic LDAP operations. Bonsai is
supporting the following controls. Always check (the root DSE's `supportedControls`) that the
server also supports the selected control.  

Server side sort
----------------

Using the server side sort control the result of the search is ordered based on the selected
attributes. To invoke the control simply set the `sort_order` parameter of the
:meth:`LDAPConnection.search` method:

    >>> conn = client.connect()
    >>> conn.search("ou=nerdherd,dc=bonsai,dc=test", 2, sort_order=["-cn", "gn"])

Attributes that start with `-` are used for descending order.

.. warning::
    Even if the server side sort control is supported by the server there is no guarantee that the
    results will be sorted for multiple attributes.

.. note::
    The OID of server side sort control is: 1.2.840.113556.1.4.473.

Paged search result
-------------------

Paged search can be used to reduce large search result into smaller pages. Page result can be used
if the `page_size` is set for the :meth:`LDAPConnection.search` method:
    
    >>> conn = client.connect()
    >>> conn.search("ou=nerdherd,dc=bonsai,dc=test", 2, page_size=3)
    <_bonsai.ldapsearchiter object at 0x7f006ad455d0>

Please note that the return value is changed from list to :class:`ldapsearchiter`. This object can
be iterated over the entries of the page. By default the next page of results is acquired automatically
during the iteration. This behaviour can be changed by setting the :attr:`LDAPClient.auto_page_acquire`
to `False` and using the :meth:`ldapsearchiter.acquire_next_page` method which explicitly initiates
a new search request to get the next page.

Paged search result cannot be used with virtual list view.

.. note::
    The OID of paged search control is: 1.2.840.113556.1.4.319.

Virtual list view
-----------------

Virtual list view (VLV) is also for reducing large search result, but with a more specific manner.
Virtual list view mimics the scrolling view of an application: it can select a target entry of a 
large list (ordered search result) with an offset or an attribute value and receiving only a
given number of entries before and after it as a partial result of the entire search.

The :meth:`LDAPConnection.search` method's `offset` or `attrvalue` can be used to select the
target, the `before_count` and `after_count` for specifying the number of entries before and after
the target.

Also need to set the `est_list_count` parameter: the estimated size of the entire list by the
client. The server will adjust the position of the target entry based on the real list size,
estimated size and the offset.  

Virtual list view control cannot be used without a server side sort control. 

    >>> conn.search("ou=nerdherd,dc=bonsai,dc=test", 2, attrlist=['cn', 'uidNumber'], sort_order=['-uidNumber'], offset=4, before_count=1, after_count=1, est_list_count=6)
    ([{'cn': ['sam'], 'uidNumber': [4]}, {'cn': ['skip'], 'uidNumber': [3]}, {'cn': ['jeff'],
    'uidNumber': [2]}], {'target_position': 4, 'oid': '2.16.840.1.113730.3.4.10', 'list_count': 7})

The return value of the search is a tuple of the list and a dictionary. The dictionary contains
the VLV server response: the target position and the real list size.

.. note::
    The OID of virtual list view control is: 2.16.840.1.113730.3.4.9.

Password policy
---------------

Password policy defines a set of rules about accounts and modification of passwords. It allows
for the system administrator to set expiration time for passwords and a maximal number of failed
login attempts before the account become locked. Is also specifies rules about the quality of
password.

Enabling the password policy control with :meth:`LDAPClient.set_password_policy` method, the client
can receive additional information during connecting to a server or modifying a user's password.
Setting this control will change the return value of :meth:`LDAPClient.connect` and
:meth:`LDAPConnection.open` to a tuple of :class:`LDAPConnection` and a dictionary that contains
the remaining seconds until the password's expiration and the remaining grace logins. The client
can also receive new exceptions related to password modifications.

    >>> import bonsai
    >>> client = bonsai.LDAPClient()
    >>> client.set_credentials("SIMPLE", ("cn=user,dc=bonsai,dc=test", "secret"))
    >>> client.set_password_policy(True)
    >>> conn, ctrl = client.connect()
    >>> conn
    <bonsai.ldapconnection.LDAPConnection object at 0x7fa552ab4e28>
    >>> ctrl
    {'grace': 1, 'expire': 3612, 'oid': '1.3.6.1.4.1.42.2.27.8.5.1'})

If the server does not support password policy control or the given credentials does not have
policies (like anonym or administrator user) the second item in the tuple will be `None`.

.. note::
    Because the password policy is not standardized, it is not listed by the server among
    the `supportedControls` even if it is available.

.. note::
    Password policy control cannot be used on MS Windows with WinLDAP. In this case after 
    opening a connection the control dictionary will always be `None`.

Extended DN
-----------

Setting LDAP_SERVER_EXTENDED_DN control with :meth:`LDAPClient.set_extended_dn` will extend the
standard DN format with the SID and GUID attributes to `<GUID=xxxxxxxx>;<SID=yyyyyyyyy>;distinguishedName`
during the LDAP search. The method's parameter can be either 0 which means that the GUID and SID
strings will be in a hexadecimal string format or 1 for receiving the extended dn in a standard
string format. This control is only supported by Microsoft's Active Directory.

Regardless of setting the control, the :attr:`LDAPEntry.dn` still remains a simple :class:`LDAPDN`
object without the SID or GUID extensions. The extended DN will be set to the :attr:`LDAPEntry.extended_dn`
as a string. The extended DN control also affects other LDAP attributes that use distinguished names
(e.g. `memberOf` attribute).

    >>> client = bonsai.LDAPClient()
    >>> client.set_extended_dn(1)
    >>> result = conn.search("ou=nerdherd,dc=bonsai,dc=test", 1)
    >>> result[0].extended_dn
    <GUID=899e4e01-e88d-4dea-ba64-119ed386b61c>;<SID=S-1-5-21-101232111302-1767724339-724445543-12345>;cn=chuck,ou=nerdherd,dc=bonsai,dc=test
    >>> result[0].dn
    <LDAPDN cn=chuck,ou=nerdherd,dc=bonsai,dc=test>

.. note::
    The OID of extended DN control is: 1.2.840.113556.1.4.529.

Server tree delete
------------------

Server tree delete control allows the client to remove entire subtree with a single request if
the user has appropriate permissions to remove every corresponding entries. Setting the `recursive` 
parameter of :meth:`LDAPConnection.delete` and :meth:`LDAPEntry.delete` to `True` will send 
the control with the delete request automatically, no further settings are required.

.. note::
    The OID of server tree delete control is: 1.2.840.113556.1.4.805

ManageDsaIT
-----------

The ManageDsaIT control can be used to work with LDAP referrals as simple LDAP entries. After 
setting it with the :meth:`LDAPClient.set_managedsait` method, the referrals can be added
removed, and modified just like entries.

    >>> client = bonsai.LDAPClient()
    >>> client.set_managedsait(True)
    >>> conn = client.connect()
    >>> ref = conn.search("o=admin-ref,ou=nerdherd,dc=bonsai,dc=test", 0)[0]
    >>> ref
    {'objectClass': ['referral', 'extensibleObject'], 'o': ['admin-ref']}
    >>> type(ref)
    <class 'bonsai.ldapentry.LDAPEntry'>

.. note::
    The OID of ManageDsaIT control is: 2.16.840.1.113730.3.4.2

Asynchronous operations
=======================

It is possible to start asynchronous operations, if the :meth:`LDAPClient.connect` method's async
parameter is set to True. By default the returned connection object can be used with Python's
`asyncio` library. For further details about how to use the asyncio library see the
`official documentation`_.

An example for asynchronous search and modify with `asyncio`:

.. _official documentation: https://docs.python.org/3/library/asyncio.html

.. code-block:: python
    
    import asyncio
    import bonsai

    @asyncio.coroutine
    def do():
        cli = bonsai.LDAPClient("ldap://localhost")
        with (yield from cli.connect(async=True)) as conn:
            results = yield from conn.search("ou=nerdherd,dc=bonsai,dc=test", 1)
            for res in results:
                print(res['givenName'][0])
            search = yield from conn.search("cn=chuck,ou=nerdherd,dc=bonsai,dc=test", 0)
            entry = search[0]
            entry['mail'] = "chuck@nerdherd.com"
            yield from entry.modify()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(do())

It is also possible to change this class to a different one with
:meth:`LDAPClient.set_async_connection_class` that is able to work with other non-blocking
I/O modules like `Gevent`_ or `Tornado`_.

For example using the module with Gevent:

.. code-block:: python

    import gevent

    import bonsai
    from bonsai.gevent import GeventLDAPConnection

    def do():
        cli = bonsai.LDAPClient("ldap://localhost")
        # Change the default async conn class.
        cli.set_async_connection_class(GeventLDAPConnection)
        with cli.connect(True) as conn:
            results = conn.search("ou=nerdherd,dc=bonsai,dc=test", 1)
            for res in results:
                print(res['givenName'][0])
            search = conn.search("cn=chuck,ou=nerdherd,dc=bonsai,dc=test", 0)
            entry = search[0]
            entry['mail'] = "chuck@nerdherd.com"
            entry.modify()

    gevent.joinall([gevent.spawn(do)])

.. _Gevent: http://www.gevent.org/
.. _Tornado: http://www.tornadoweb.org/en/stable/  
