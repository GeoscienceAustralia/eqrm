Steps for running benchmark tests with virtualenv 

1. python eqrm/trunk/sw_development_tools/virtualenv.py EQRM_test
2. source EQRM_test/bin/activate
3. pip install -r eqrm/trunk/sw_development_tools/requirements-1.txt
4. pip install -r eqrm/trunk/sw_development_tools/requirements-2.txt
5. cd eqrm/trunk
6. python test_all.py --bench