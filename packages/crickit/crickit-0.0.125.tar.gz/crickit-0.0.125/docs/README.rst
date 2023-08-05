Crick-It
========

|Build Status| |codecov| |Maintainability| |contributions welcome|
|GitHub version| |Open Source Love| |MIT Licence| |GitHub issues|

Crickit is a text-based cricket simulator.

Available teams
~~~~~~~~~~~~~~~

-  India
-  Pakistan

Team Data Contributions welcome

API
~~~

Play a single Match between two specific teams


.. code:: python

    playMatch(team1, team2)

Simulate n Matches between two specific teams


.. code:: python

    simulateMatches(team1, team2, n)

n(default = 100)

Roadmap
~~~~~~~

1. Refactor based on actual cricket data stats (Strike rate, economy
   rate etc)

   1. Currently its modelled on the probability of wide ball, no ball,
      wicket Ball etc, which are not standard cricket stats

Future Releases


1. Simulate game based on current player of the team
2. Simulate an entire T20 tournament

   1. Create directory/dictionary/file of teams and their stats
   2. Create directory of teams for each team with individual stats

3. Bug fixes, tuning

.. 11th-november-2017:

11th november 2017


Initial Commit working two team cricket game

Author Information
~~~~~~~~~~~~~~~~~~

Created by `Akshay Agrawal`_ at ArtCenter College of Design

License Information
'''''''''''''''''''

The MIT License

.. _Akshay Agrawal: https://en.wikipedia.org/wiki/Akshay_Agrawal

.. |Build Status| image:: https://travis-ci.org/oficiallyAkshayEdu/crickit.svg?branch=master
   :target: https://travis-ci.org/oficiallyAkshayEdu/crickit
.. |codecov| image:: https://codecov.io/gh/oficiallyAkshayEdu/crickit/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/oficiallyAkshayEdu/crickit
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/28613489cf646368e3cd/maintainability
   :target: https://codeclimate.com/github/oficiallyAkshayEdu/crickit/maintainability
.. |contributions welcome| image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
   :target: https://github.com/dwyl/esta/issues
.. |GitHub version| image:: https://badge.fury.io/gh/oficiallyAkshayEdu%2Fcrickit.svg
   :target: https://badge.fury.io/gh/oficiallyAkshayEdu%2Fcrickit
.. |Open Source Love| image:: https://badges.frapsoft.com/os/v2/open-source.svg?v=103
   :target: https://github.com/ellerbrock/open-source-badges/
.. |MIT Licence| image:: https://badges.frapsoft.com/os/mit/mit.svg?v=103
   :target: https://opensource.org/licenses/mit-license.php
.. |GitHub issues| image:: https://img.shields.io/github/issues/oficiallyAkshayEdu/crickit.svg
   :target: https://github.com/oficiallyAkshayEdu/crickit/issues