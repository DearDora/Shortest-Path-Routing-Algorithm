script:
	@echo "python router.py 1 ubuntu1804-008 7689 7681 &" >router 2>&1;
	@echo "python router.py 2 ubuntu1804-008 7689 7682 &" >>router 2>&1;
	@echo "python router.py 3 ubuntu1804-008 7689 7683 &" >>router 2>&1;
	@echo "python router.py 4 ubuntu1804-008 7689 7684 &" >>router 2>&1;
	@echo "python router.py 5 ubuntu1804-008 7689 7685"   >>router 2>&1;
	chmod a+x router
clean:
	$(RM) -f *.pyc
