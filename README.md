ChronAm-Bookworm
================

Build a bookworm from the openly available Chronicling America data


This is a repo that contains code for building a Bookworm specifically on the [Chronicling America](chroniclingamerica.loc.gov)
set from the library of congress. (Once it's fully complete), running `make` will download gigabytes of data,
install a bookworm instance, and parse and load it in. This will take a very long term: maybe, like, a week or so?

It will also work with the LOC data to build in test suites.

This could be considered the largest bookworm test suite: 6 million documents of fairly significant length.
But it's not polite to download all those LOC data dumps more than once, everyone.

