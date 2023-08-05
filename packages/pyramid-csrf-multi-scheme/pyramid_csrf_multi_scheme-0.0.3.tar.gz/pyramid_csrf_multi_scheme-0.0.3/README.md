pyramid_csrf_multi_scheme
=========================

This script enables two separate cookie tokens on each request, bound to the scheme: a SECURE HTTPS only cookie and a mixed-use insecure http token (that is also available on https).

If the current scheme is HTTPS:
	only the SECURE HTTPS token will be considered
	HOWEVER calls to generate a new token will reset both the SECURE HTTPS and the insecure http tokens.

If the current scheme is insecure http:
	the SECURE HTTPS tokens are ignored as they are not even available, and only the insecure http token is considered.


Why?
----

If an app supports both HTTP and HTTPS endpoints in parts, there may be a desire to shield the SECURE HTTPS token from the insecure http traffic.


Is this necessary?
------------------

I'm not sure, but have decided to err on the side of caution.  HTTP traffic is sent in plaintext and capable of being intercepted by a man-in-the-middle or network packet sniffing.  It seems plausible that someone might read a csrf token via HTTP and use that in attempts to compromise HTTPS endpoints.  A better option would be only using HTTPS tokens and forms - but that is not always an option.


debugtoolbar support!
---------------------

just add to your development.ini

	debugtoolbar.includes = pyramid_csrf_multi_scheme.debugtoolbar

the debugtoolbar will now have a `CSRFMultiScheme` panel that has the following info:

* configuration info on the cookie names
* incoming request csrf values
* outgoing response csrf values


License
-------

Most of this is just code lightly edited from Pyramid, and therefore available under Pyramid's licensing terms.
