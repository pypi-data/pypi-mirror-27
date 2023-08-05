
wikiexpand
==========

Expansion engine for pages written using MediaWiki syntax, based on
mwparserfromhell_.

*Wikiexpand* tries to mimic the expansion of transcluded text (templates) and
magic words (parser functions and variables).

.. _mwparserfromhell: https://github.com/earwig/mwparserfromhell

Usage
-----

First, we need to create an expansion context (``wikiexpand.expand.ExpansionContext``),
and provide a place where to look for our templates (``wikiexpand.expand.templates.TemplateStore``):

.. code-block:: python

    # expansion context
    from wikiexpand.expand import ExpansionContext
    # a template store using `dict` as storage
    from wikiexpand.expand.templates import TemplateDict

    tpl = TemplateDict()

    # define a simple template
    tpl["helloworld"] = "Hello World"

    # create the expansion context
    ctx = ExpansionContext(templates=tpl)

    # expand text transcluding our template
    ctx.expand("Lorem {{helloworld}}! Ipsum")
    'Lorem Hello World! Ipsum'


Parser functions and magic words
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most common used parser functions and magic words can also be expanded:

.. code-block:: python

    # expand text using a parser functions
    ctx.expand("{{#if:x|1|0}} {{#if:|1|0}}")
    '1 0'


Many magic words provide contextual data which are defined for a site (namespaces,
server time, etc.) or a given page (title, url, etc.). In order to be able to
expand those magic words, providing site (``wikiexpand.expand.context.SiteContext``)
and page context (``wikiexpand.expand.context.PageContext``) is required.

.. code-block:: python

    # implementation using pywikibot to retrieve info from a Wikimedia site
    import pywikibot as pw
    from wikiexpand.wiki.context import Wiki

    # site context for es.wiktionary.org
    eswikt = Wiki(pw.Site("es", "wiktionary"))

    # set page context for a page named "hello"
    ctx.set_context(eswikt.page_context("hello"))

    ctx.expand("Using page context: {{PAGENAME}}, {{TALKSPACE}}. Using site context: [{{fullurl:hello}}], {{NAMESPACE:Template:helloworld}}")
    'Using page context: hello, Discusión. Using site context: [https://es.wiktionary.org/wiki/hello], Plantilla'


Implemented parser functions
++++++++++++++++++++++++++++

``#expr``*, ``#if``, ``#ifeq``, ``#ifexist``, ``#rel2abs``, ``#switch``, ``#tag``,
``#time``*, ``#timel``, ``#titleparts``, ``anchorencode``, ``articlepagename``,
``articlepagenamee``, ``articlespace``, ``articlespacee``, ``basepagename``,
``basepagenamee``, ``defaultsort``, ``fullpagename``, ``fullpagenamee``, ``fullurl``,
``lc``, ``lcfirst``, ``namespace``, ``namespacee``, ``ns``, ``padleft``, ``padright``,
``pagename``, ``pagenamee``, ``rootpagename``, ``rootpagenamee``, ``subjectpagename``,
``subjectpagenamee``, ``subjectspace``, ``subjectspacee``, ``subpagename``,
``subpagenamee``, ``talkpagename``, ``talkpagenamee``, ``talkspace``, ``talkspacee``,
``uc``, ``ucfirst``, ``urlencode``.

Implemented behaviour of the functions marked with * differs from the reference.

Implemented variables
+++++++++++++++++++++

``!``, ``ARTICLEPAGENAME``, ``ARTICLEPAGENAMEE``, ``ARTICLESPACE``, ``ARTICLESPACEE``,
``BASEPAGENAME``, ``BASEPAGENAMEE``, ``CURRENTDAY``, ``CURRENTDAY2``,
``CURRENTDAYNAME``, ``CURRENTDOW``, ``CURRENTHOUR``, ``CURRENTMONTH``,
``CURRENTMONTH1``, ``CURRENTMONTHABBREV``, ``CURRENTMONTHNAME``, ``CURRENTTIME``,
``CURRENTTIMESTAMP``, ``CURRENTWEEK``, ``CURRENTYEAR``, ``FULLPAGENAME``,
``FULLPAGENAMEE``, ``LOCALDAY``, ``LOCALDAY2``, ``LOCALDAYNAME``, ``LOCALDOW``,
``LOCALHOUR``, ``LOCALMONTH``, ``LOCALMONTH1``, ``LOCALMONTHABBREV``,
``LOCALMONTHNAME``, ``LOCALTIME``, ``LOCALTIMESTAMP``, ``LOCALWEEK``, ``LOCALYEAR``,
``NAMESPACE``, ``NAMESPACEE``, ``PAGENAME``, ``PAGENAMEE``, ``ROOTPAGENAME``,
``ROOTPAGENAMEE``, ``SUBJECTPAGENAME``, ``SUBJECTPAGENAMEE``, ``SUBJECTSPACE``,
``SUBJECTSPACEE``, ``SUBPAGENAME``, ``SUBPAGENAMEE``, ``TALKPAGENAME``,
``TALKPAGENAMEE``, ``TALKSPACE``, ``TALKSPACEE``.

Lua modules
~~~~~~~~~~~

Modules written in Lua and executed using ``{{#invoke:}}`` are not recognised, but
can be replaced by implementing callable templates (that is, functions that
render Wikicode). See the doc in
``wikiexpand.expand.templates.TemplateStore.callable_templates``.


Changelog
---------

0.2
===

* new parser function & variable ARTICLEPAGENAME, ARTICLEPAGENAMEE
* new parser function & variable SUBPAGENAME, SUBPAGENAMEE
* new parser function & variable ROOTPAGENAME, ROOTPAGENAMEE
* new parser function & variable BASEPAGENAME, BASEPAGENAMEE
* new parser function #titleparts
* site context: clean and canonical title perform previous space cleaning and unescaping of html entities.


