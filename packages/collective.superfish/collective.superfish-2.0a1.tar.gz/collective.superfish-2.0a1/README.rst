====================
collective.superfish
====================

What is it?
===========

collective.superfish integrates the `jQuery Superfish plugin`_ into Plone.

Superfish is a really nice solution for dropdown menus using css, valid xhtml
and JavaScript which degrades gracefully if JavaScript is not available.

.. _`jQuery Superfish plugin`: https://superfish.joelbirch.co/


Which Version is for me?
========================

Since Version 2.0 ``collective.superfish`` targets Plone 5 only.

If you want to use it on Plone < 5 then stay to the 1.x versions.


How do you use it?
==================

This package behaves as a "drop-in" replacement for ``plone.global_sections``.
Just install it :)


Customization
=============

Use Plone's Configuration Registry to change Superfish settings.
Filter for prefix ``ISuperfishSettings`` to see available options.

For integrators you can set the following records in ``registry.xml`` of your theme profile::

    <records interface='collective.superfish.interfaces.ISuperfishSettings' prefix='superfish'>
        <value key="add_portal_tabs">True</value>
        <value key="menu_depth">2</value>
        <value key="superfish_options">{ "delay": 800, "cssArrows": true }</value>
    </records>

See https://superfish.joelbirch.co/options/ for a complete
list of available ``superfish_options``.

