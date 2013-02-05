2a-graphs
=========

A [sunburst representation](http://bl.ocks.org/4063423) of the variety of 2A concentrations at MIT. [See it here](http://web.mit.edu/eburn/www/2a)

Requires [d3](https://github.com/mbostock/d3/) for the visualization, [poshytip](http://vadikom.com/demos/poshytip/) for the tooltips, and [jQuery](http://www.jquery.com) for some odds and ends.

toolchain
----------
Excel to CSV to python (where class numbers are confirmed by scraping MIT's online course catalog) to JSON to d3.js

still done by hand
-------------------
1. Chopping the .xlsx into the .csv
2. sorting the .csv by department popularity > class popularity

todo
-----
- cleanup and comment the css
- make it a meteor app, and show what the last twentyorso people moused over / searched
 	- should work well with animations?

notes
------
there's the potential for extending it to search by people (in particular tracks, who are taking a particular course, etc.)
for the tracks, it's currently sorta misleading as to what it's representing. I'm saying who belong to a given track, while those lokoing for classes are more interested in the above. Hmm.