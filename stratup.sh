#!/bin/bash
#startup run in bash shell
#
#__main__
while true
do
	clear
	echo "*************************"
	echo "* SPEED CONTROL FOR ODL *"
	echo "*************************"
	echo "1.show network speed"
	echo "2.speed control(mod1)"
	echo "3.speed control(mod2)"
	echo ">>q to quit<<"

	read achoice
	case $achoice in
	  1) python getspeed_only.py
		 read junk
	  ;;
	  2) python starupmod1.py
		 read junk
	  ;;
	  3) python startupmod2.py
		 read junk
	  ;;
	  q) clear
	     break
	  ;;
	  *) echo "wrong choice"
		 printf "try again, any key to continue >"
		 read junk
	  ;;
	esac
done
