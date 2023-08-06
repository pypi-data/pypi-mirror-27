prose-wc
========

|Build Status| |Coverage Status| |PyPI|

A prose- and Jekyll-aware wordcount utility.

About
-----

Given the proliferation of Markdown and the use of Jekyll as a blogging
platform, the builtin ``wc`` utility came up short.  Even for plain-text
prose, ``wc`` can leave much to be desired.  To that end, ``prose-wc`` will
calculate proper word, paragraph, and character counts for a given plaintext,
or markdown file or stream through STDIN.

Also, Madison wanted to learn how to package for PyPI.

Installing
----------

::

    pip install prose-wc

Running
-------

::

    usage: prose-wc [-h] [-S] [-u] [-f [{yaml,json,default}]] [-i [INDENT]] file

    Compute Jekyl- and prose-aware wordcounts

    positional arguments:
      file                  file to count (or - for STDIN)

    optional arguments:
      -h, --help            show this help message and exit
      -S, --split-hyphens   split hyphenated words rather than counting them as
                            one word ("non-trivial" counts as two words rather
                            than one)
      -u, --update          update the jekyll file in place with the counts. Does
                            nothing if the file is not a Jekyll markdown file.
                            Implies format=yaml, invalid with input from STDIN and
                            non-Jekyll files.
      -f [{yaml,json,default}], --format [{yaml,json,default}]
                            output format.
      -i [INDENT], --indent [INDENT]
                            indentation depth (default: 4).

    Accepted filetypes: plaintext, markdown, markdown (Jekyll)

Running ``prose-wc`` against a file will generate a series of counts
that might be of use. You can get these counts in a simple,
tab-separated format, JSON, or YAML. If you're working with a Jekyll
markdown file, you can also choose to have this data embedded in the
frontmatter as YAML.

Other filetypes
---------------

You can use `pandoc <http://pandoc.org>`__ to convert your file and pipe
it into prose-wc:

::

    pandoc -f latex -t plain my_great_story.tex | prose-wc -

In a Jekyll site
----------------

You can add wordcount information to your site by running ``prose-wc -u
<file>``, which will update the Jekyll frontmatter to include the results in
YAML format.  This data can then be included on the page in some place handy such as at the top of a post in ``_layouts/post.html`` with:

.. code:: liquid

    {% if page.counts %}
        <p class="text-muted small">
            {{ page.counts.paragraphs }} {% if page.counts.paragraphs == 1 %}paragraph{% else %}paragraphs{% endif %} &bullet;
            {{ page.counts.words }} words
        </p>
    {% endif %}

This would result in something like
`this <http://writing.drab-makyo.com/posts/tasting/2016/09/17/teas-of-late/>`__.

You can add wordcounts to posts with a find command like:

::

    find . \( -name '*.md' -or -name '*.markdown' \) -exec prose-wc -u "{}" \;

Further information
-------------------

Source, issues, and further information:
  `GitHub <https://github.com/makyo/prose-wc>`__
Author
  `Madison Scott-Clary <http://drab-makyo.com>`__

.. |Build Status| image:: https://travis-ci.org/makyo/prose-wc.svg?branch=master
   :target: https://travis-ci.org/makyo/prose-wc
.. |Coverage Status| image:: https://coveralls.io/repos/github/makyo/prose-wc/badge.svg?branch=master
   :target: https://coveralls.io/github/makyo/prose-wc?branch=master
.. |PyPI| image:: https://img.shields.io/pypi/v/prose-wc.svg
   :target: https://pypi.python.org/pypi/prose-wc/
