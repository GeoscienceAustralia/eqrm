# Makefile to build everything

all:		nga_gm_tmr general.ctl general.out bigtest_Abrahamson08.py \
			bigtest_Boore08.py bigtest_Campbell08.py \
			bigtest_Chiou08.py

run:		all
		python bigtest_Abrahamson08.py
		python bigtest_Boore08.py
		python bigtest_Campbell08.py
		python bigtest_Chiou08.py

nga_gm_tmr:	nga_gm_tmr_subs.for nga_gm_tmr.for Makefile
		gfortran nga_gm_tmr.for -o nga_gm_tmr

general.ctl:	make_general_ctl.py Makefile
		python make_general_ctl.py > xyzzy
		cat general.skel xyzzy > general.ctl
		rm -f xyzzy

general.out:	general.ctl nga_gm_tmr Makefile
		echo "general.ctl" | nga_gm_tmr

bigtest_Abrahamson08.py:make_Abrahamson08_unittest.py general.out Makefile
		python make_Abrahamson08_unittest.py general.out > bigtest_Abrahamson08.py
		
bigtest_Boore08.py:	make_Boore08_unittest.py general.out Makefile
		python make_Boore08_unittest.py general.out > bigtest_Boore08.py
		
bigtest_Campbell08.py:	make_Campbell08_unittest.py general.out Makefile
		python make_Campbell08_unittest.py general.out > bigtest_Campbell08.py
		
bigtest_Chiou08.py:	make_Chiou08_unittest.py general.out Makefile
		python make_Chiou08_unittest.py general.out > bigtest_Chiou08.py
		
clean:	
		rm -f *.o *.pyc xyzzy

reallyclean:	clean
		rm -f nga_gm_tmr general.ctl general.out bigtest_Abrahamson08.py \
			bigtest_Boore08.py bigtest_Campbell08.py bigtest_Chiou08.py
