2a-graphs
=========

A sunburst representation of the variety of 2A concentrations at MIT, made using [d3](https://github.com/mbostock/d3/wiki). [See it here](http://web.mit.edu/eburn/www/2a)
Requires [BeautifulSoup](www.crummy.com/software/BeautifulSoup/).

toolchain
----------
Excel to CSV to python (where class numbers are confirmed by scraping MIT's online course catalog) to JSON to d3.js

still done by hand
-------------------
1. Chopping the .xlsx into the .csv
2. sorting the .csv by department popularity

extensions
-----------
- cleanup and comment javascript
- using jQuery, 
  - clean up tooltips with [Poshy Tip](http://vadikom.com/demos/poshytip/#download)
  - use a multiple select widget to let people choose which departments they want to see 
    - useful for 2A students
    - d.value = d.pop * d.weight
    - jQuery multiple select resources: [get selection](http://stackoverflow.com/questions/2290181/jquery-multiple-select-options) | [quite functional widget](http://www.erichynds.com/jquery/jquery-ui-multiselect-widget)
- make it a meteor app, and show the last fiveorso people's views
  - if d.value != 0