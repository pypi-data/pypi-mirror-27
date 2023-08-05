Web asset management for WSGI
=============================

Bitbucket repository: https://bitbucket.com/ollyc/assetbuilder/

Why use AssetBuilder?

- AssetBuilder delegates to your existing tool chain to build assets.
  **gulp**, **grunt**, **Make**, or pretty much anything else can be used.

- No more shoehorning javascript build tools into Python wrappers.

- Front end tech moves fast! No need to wait for a plugin to support
  that latest npm package you want to use.

- Framework agnostic! Works with any WSGI compatible framework. Flask,
  Fresco, Django, Pyramid and many others.


**In production mode**, AssetBuilder:

- Serves compiled asset files as static files
  (and for even better performance it's easy to delegate this to a dedicated
  frontend web server such as nginx too)

- Generates links to your assets that include cache busting version numbers
  to ensure stale assets are expired immediately.

**In development mode**, AssetBuilder:

- Rescans source files on each hit, to ensure all assets are rebuilt before
  they are served – so your webapp is never rendered with out of date asset
  files.

- Uses locking to ensure that asset builds are only triggered once –
  partially built asset files are never served up.


Configuration
--------------

::

    from assetbuilder import AssetBuilder

    # '/assets' is the base URL assets will be served from, and is used for
    # generating links to your asset files.
    # If you do not specify a fully qualified domain name, the base URL of the
    # parent application will be prepended.
    #
    # 'myproj/static/build' is the filesystem directory where compiled asset
    # files are placed.
    #
    # 'myproj/static/src' is where AssetBuilder should scan for dependency
    # files. You can add multiple sources here.
    #
    # autobuild=True tells it to rebuild assets whenever they change.
    # -- always turn this off in production!
    #
    assets = AssetBuilder('/assets',
                          'myproj/static/.build/',
                          depdirs=['myproj/static/src/],
                          autobuild=True)

    # This is the default shell command used to build asset files.
    assets.set_default_build_command('make assets', cwd='myproj/static')

    # Now we add paths to each asset files. Each asset file is tagged ('js',
    # 'css'), so that we can refer to groups of asset files at the same time
    assets.add_path('js', 'jquery/dist/jquery.min.js')
    assets.add_path('js', 'site.min.js')
    assets.add_path('css', 'site.min.css')

    # Additional arguments specify dependencies using glob syntax.
    # A prefix of ! can be used to exclude files.
    # If any dependencies change, a rebuild is triggered.
    assets.add_path('admin-js', 'admin.min.js', '**/*.js', '!**/exclude/**')

    # Individual assets can have custom build commands specified
    assets.add_path('images', 'img/logo.png', command='make images', cwd='img')


Once the AssetBuilder object is configured, you need to mount it in
your larger application. How you do this is framework specific – here's an
example using django-wsgi::

    from django.conf.urls import url
    from django_wsgi.embedded_wsgi import make_wsgi_view

    urlpatterns = [url(r'^assets(/.*)$', make_wsgi_view(assetbuilder)),
                   ...
                  ]

And here's an example for fresco::

    app = FrescoApp()
    app.route_wsgi('/assets', assetbuilder)

Finally, you'll want to add links to your assets. Make sure that the
assetbuilder object is available to your template namespace, then add code
similar to the following::

    {% for url in assetbuilder.urls('js', request.environ) %}
    <script src="{{ url }}"></script>
    {% end %}
    {% for url in assetbuilder.urls('css', request.environ) %}
    <link rel="stylesheet" href="{{ url }}" />
    {% end %}

Note the use of the tags we defined in the calls to ``add_path`` (above),
to link to js and css asset sets separately.
You can use whatever tags you want, for example to maintain separate
sets of assets for different sections of your website.


Rebuilding
----------

Asset files are only built if ``autobuild`` is set to True.

If you have configured build commands (globally through
``set_default_build_command``, and/or per-asset in ``add_path``), and
configured dependencies for each asset (also in ``add_path``), then rebuilding
will be automatic.

When ``autobuild`` is turned on,
you can manually trigger rebuilds by pinging the server.
For example, if AssetBuilder is mounted at ``http://localhost/assets``,
then to trigger a rebuild of all assets::

    curl http://localhost/assets/update

You can also trigger a 'clean' rebuild::

    curl http://localhost/assets/update?clean

A clean rebuild will **DELETE** all asset files configured
through ``add_path``, then call the configured build system to recreate them.
Only use AssetBuilder to serve compiled asset files that can
be completely reconstructed from sources! You have been warned!

Note that these urls are only available if ``autobuild`` is set to True.

I like to combine this with `entr <http://entrproject.org>`_, eg::

    find myproj/static -name '*.css' -o '*.js' | \
        entr -d sh -c 'curl http://localhost/assets/update'

Note that ``autobuild`` should only be set on development environments.
Do not use this option in production:

- With ``autobuild=True``, the web server would need access to write to files
  in the web root. This access should never be configured on a production
  server.
- With ``autobuild=True`` there is a performance overhead as assetbuilder
  rescans all dependencies on every hit.
- Setting ``autobuild=True`` would require you to have your development
  toolchain installed on the production server. For security and ease of
  maintenance it is better to avoid this.


Troubleshooting
---------------

AssetBuilder will complain if asset building fails for any reason.
You can turn up the logging verbosity with standard python logging
configuration.

The logger name is ``assetbuilder``. You can set this to log at
``INFO`` or ``DEBUG`` level in your logging configuration file,
or programmatically with::

  logging.getLogger('assetbuilder').setLevel(logging.DEBUG)

