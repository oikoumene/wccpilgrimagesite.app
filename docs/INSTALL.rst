wccpilgrimagesite.app Installation
----------------------------------

To install wccpilgrimagesite.app using zc.buildout and the plone.recipe.zope2instance
recipe to manage your project, you can do this:

* Add ``wccpilgrimagesite.app`` to the list of eggs to install, e.g.:

    [buildout]
    ...
    eggs =
        ...
        wccpilgrimagesite.app

* Re-run buildout, e.g. with:

    $ ./bin/buildout

