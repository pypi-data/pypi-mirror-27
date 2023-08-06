===============================
 Ideas for Additional Features
===============================

Actually CodeReview has a limited number of features.  The followings list gives some ideas to extend its
features:

 * Add Mercurial support. (Git and Mercurial are actually the most cool VCS)

 * Add a graphical representation of the branches.  I don't understand the crappy code of qlog and I
   don't know any algorithm on this topic (graphviz, qgit ?).  To summarize I don't what and how to do.

 * Implement the detection of code translocations.  Sometimes we move code within a file or a
   project.  Such changes are related as deletion and addition in the code, which don't help to
   review code.  We can do something clever by computing a distance between all the added and
   deleted chuncks.  The distance could be computed using a Levenshtein, Damerau–Levenshtein,
   Needleman–Wunsch or Smith–Waterman algorithm (DNA alignment algorithms).

 * Implement code analyser/validator as language plugins.  The idea is to annotate change as
   cosmetic or dangerous modifications.  For example a deleted or added space is a cosmetic change
   in C, but it can be a regression in Python where the indentation is part of the grammar.

 * Implement blame wich is another important feature.

 * Implement comments and maybe as a client-server architecture.

 * look https://docs.python.org/3.4/library/difflib.html
