Sphinx Sitemap Generator Extension
==================================

*`Sphinx <http://sphinx-doc.org/>`__ extension to silently generate a
sitemaps.org compliant sitemap for the HTML version of your Sphinx
Documentation.*

|Build Status|

Installing
----------

1. Add/set the value of **base\_url** in your Sphinx **conf.py** to the
   current base URL of your documentation. For example,
   ``https://my-site.com/docs/``.

2. Copy the **sphinx\_sitemap** directory into your extensions directory
   or **sys.path**, then add ``sphinx_sitemap`` to the **extensions**
   array in your Sphinx **conf.py**.

    **Note:** sphinx-sitemap supports Sphinx 1.2 and later, and Python
    2.7, 3.3, and 3.4.

License
-------

sphinx-sitemap is made available under a MIT license; see LICENSE for
details.

Originally based on the sitemap generator in the
`guzzle\_sphinx\_theme <https://github.com/guzzle/guzzle_sphinx_theme>`__
project licensed under the MIT license.

.. |Build Status| image:: https://travis-ci.org/jdillard/sphinx-sitemap.svg?branch=master
   :target: https://travis-ci.org/jdillard/sphinx-sitemap
