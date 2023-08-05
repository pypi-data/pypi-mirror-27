NOTE: this fork of ccs-kerberos is currently on life support mode as Apple has resumed work on upstream. Please try to use https://pypi.python.org/pypi/kerberos instead of this fork if possible.


=========================================================
PyKerberos Package

Copyright (c) 2006-2013 Apple Inc. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

=========================================================

This Python package is a high-level wrapper for Kerberos (GSSAPI) operations.
The goal is to avoid having to build a module that wraps the entire Kerberos.framework,
and instead offer a limited set of functions that do what is needed for client/server
Kerberos authentication based on <http://www.ietf.org/rfc/rfc4559.txt>.

Much of the C-code here is adapted from Apache's mod_auth_kerb-5.0rc7.

========
CONTENTS
========

    src/               : directory in which C source code resides.
    setup.py           : Python distutils extension build script.
    config/            : directory of useful Kerberos config files.
      edu.mit.Kerberos : example Kerberos .ini file.
    README.txt         : this file!
    kerberos.py        : Python api documentation/stub implementation.

=====
BUILD
=====

In this directory, run:

    python setup.py build

=======
TESTING
=======

You must have a valid Kerberos setup on the test machine and you should ensure that you have valid
Kerberos tickets for any client authentication being done (run 'klist' on the command line).
Additionally, for the server: it must have been configured as a valid Kerberos service with the Kerbersos server
for its realm - this usually requires running kadmin on the server machine to add the principal and generate a keytab
entry for it (run 'sudo klist -k' to see the currently available keytab entries).

Make sure that PYTHONPATH includes the appropriate build/lib.xxxx directory.
Then run test.py with suitable command line arguments:

    python test.py -u userid -p password -s service
    
    -u : user id for basic authenticate
    -p : password for basic authenticate
    -s : service principal for GSSAPI authentication (defaults to 'http@host.example.com')

================
CHANNEL BINDINGS
================

You can use this library to authenticate with Channel Binding support. Channel
Bindings are tags that identify the particular data channel being used with the
authentication. You can use Channel bindings to offer more proof of a valid
identity. Some services like Microsoft's Extended Protection can enforce
Channel Binding support on authorisation and you can use this library to meet
those requirements.

More details on Channel Bindings as set through the GSSAPI can be found here
<https://docs.oracle.com/cd/E19455-01/806-3814/overview-52/index.html>. Using
TLS as a example this is how you would add Channel Binding support to your
authentication mechanism. The following code snippet is based on RFC5929
<https://tools.ietf.org/html/rfc5929> using the 'tls-server-endpoint-point'
type.

.. code-block:: python

   import hashlib

    def get_channel_bindings_application_data(socket):
        # This is a highly simplified example, there are other use cases
        # where you might need to use different hash types or get a socket
        # object somehow.
        server_certificate = socket.getpeercert(True)
        certificate_hash = hashlib.sha256(server_certificate).hexdigest().upper()
        certificate_digest = base64.b16decode(certificate_hash)
        application_data = b'tls-server-end-point:%s' % certificate_digest

        return application_data

    def main():
        # Code to setup a socket with the server
        # A lot of code to setup the handshake and start the auth process
        socket = getsocketsomehow()

        # Connect to the host and start the auth process

        # Build the channel bindings object
        application_data = get_channel_bindings_application_data(socket)
        channel_bindings = kerberos.channelBindings(application_data=application_data)

        # More work to get responses from the server

        result, context = kerberos.authGSSClientInit(kerb_spn, gssflags=gssflags, principal=principal)

        # Pass through the channel_bindings object as created in the kerberos.channelBindings method
        result = kerberos.authGSSClientStep(context, neg_resp_value, channel_bindings=channel_bindings)

        # Repeat as necessary

===========
Python APIs
===========

See kerberos.py.
