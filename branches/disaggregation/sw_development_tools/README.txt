
	
	DEPENDENCY GRAPH
	
	Do this sort of thing to produce a dependency graph;
python py2depgraph.py ..\demo\demo_batchrun.py | python
depgraph2dot.py | c:\Python24\Enthought\Graphviz\bin\dot.exe -T jpg -o
dependency.jpg

or run the dependency.bat

It depends on graphviz being installed.
see http://www.tarind.com/depgraph.html

The graph is based on following the imports in the code.  It will not
show dynamic behaviour