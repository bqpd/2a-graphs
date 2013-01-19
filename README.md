2a-graphs
=========

A [sunburst representation](http://bl.ocks.org/4063423) of the variety of 2A concentrations at MIT. [See it here](http://web.mit.edu/eburn/www/2a)

Requires [BeautifulSoup](www.crummy.com/software/BeautifulSoup/) for scraping and [d3](https://github.com/mbostock/d3/wiki) for the visualization.

toolchain
----------
Excel to CSV to python (where class numbers are confirmed by scraping MIT's online course catalog) to JSON to d3.js

still done by hand
-------------------
1. Chopping the .xlsx into the .csv
2. sorting the .csv by department popularity > class popularity

todo
-----
- cleanup and comment the javascript
- add a multiple select widget to let people choose which departments they want to see 
	- useful for 2A students
	- d.value = d.pop * d.weight
	- jQuery multiple select resources: [get selection](http://stackoverflow.com/questions/2290181/jquery-multiple-select-options) | [quite functional widget](http://www.erichynds.com/jquery/jquery-ui-multiselect-widget)
- make it a meteor app, and show what the last twentyorso people moused over
 	- should work well with animations?

notes
------
there are two basic sorts:
- by number of people in a class
- by department