Plone hotfix, 2017-11-28
========================

This hotfix fixes several security issues:

- An open redirection and reflected Cross Site Scripting attack (XSS) on the login form and possibly other places where redirects are done.
  The ``isURLInPortal`` check that is done to avoid linking to an external site could be tricked into accepting malicious links.

- An open redirection when calling a specific url.

- Cross Site Scripting using the ``home_page`` member property.

- Accessing private content via ``str.format`` in through-the-web templates and scripts.
  See this `blog post by Armin Ronacher <http://lucumr.pocoo.org/2016/12/29/careful-with-str-format/>`_ for the general idea.
  This improves an earlier hotfix.
  Since the ``format`` method was introduced in Python 2.6, this part of the hotfix is only relevant for Plone 4 and 5, not Plone 3.


Compatibility
=============

This hotfix should be applied to the following versions of Plone:

* Plone 5.0.9 and any earlier 5.x version
* Plone 4.3.15 and any earlier 4.x version

The hotfix is officially supported by the Plone security team on the
following versions of Plone in accordance with the Plone
`version support policy <https://plone.org/security/update-policy>`_: 4.0.10, 4.1.6, 4.2.7, 4.3.15 and 5.0.9.
However it has also received some testing on older versions of Plone, for example earlier 4.3 versions.
The fixes included here will be incorporated into subsequent releases of Plone,
so Plone 4.3.16, 5.0.10 and greater should not require this hotfix.

.. warning::

    Technically, the hotfix should work on Plone 3, although the ``str.format`` part is not necessary there.
    But it gets ever more difficult to test, because the outdated and unsupported Python version 2.4 is needed.
    More and more parts required during installation of Plone (buildout, setuptools) just don't work anymore with Python 2.4.
    Getting compatible versions installed and running is tough, and may be impossible unless you are an expert.
    **If you are using Plone 3 and Python 2.4 you need to upgrade soon.**
    Plone 3 was already officially unsupported, but now the Plone Security Team is really giving up.

Installation
============

Installation instructions can be found at
https://plone.org/security/hotfix/20171128

.. note::

  You may get an error when running buildout::

    Error: Couldn't find a distribution for 'Products.PloneHotfix20171128==1.0'.

  The most likely cause is that your buildout is trying to download the hotfix via http.
  You should use the https PyPI index.
  In the buildout section of your buildout, make sure you use the correct index::

    [buildout]
    index = https://pypi.python.org/simple/


Q&A
===

Q: How can I confirm that the hotfix is installed correctly and my site is protected?
  A: On startup, the hotfix will log a number of messages to the Zope event log
  that look like this::

      2017-11-28 08:42:11 INFO Products.PloneHotfix20171128 Applied in_portal patch
      2017-11-28 08:42:11 INFO Products.PloneHotfix20171128 Hotfix installed

  The exact number of patches applied, will differ depending on what packages you are using.
  If a patch is attempted but fails, it will be logged as a warning that says
  "Could not apply". This may indicate that you have a non-standard Plone
  installation.

Q: How can I report problems installing the patch?
  A: Contact the Plone security team at security@plone.org, or visit the
  #plone channel on freenode IRC.

Q: How can I report other potential security vulnerabilities?
  A: Please email the security team at security@plone.org rather than discussing
  potential security issues publicly.
