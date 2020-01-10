This program is made by Python 3.7, compiled on MacOS Terminal. It tested on student server already. To compile the program, simply type "make" to makefile.

After compiled the code, run the following commands

On the host hostX:
            nse-linux386 <host_Y> <port_id_nse>

On the host hostY:
            ./router

It produce the log files for the five routers:
router1.log router2.log router3.log router4.log router5.log

Since there in makefile the routers already assigned port_id_nse and port_id_router because it is more convience. If you need to change the host_X, port_id_nse and port_id_router just modify the makefile.

It already test on school server with hostX is ubuntu1804-008 and hostY is ubuntu1804-004

The default values in makeflie:
<host_X> is ubuntu1804-008
<host_Y> is ubuntu1804-004
<port_id_nse> is 7689  
<port_id_router_1> is 7681
<port_id_router_2> is 7682
<port_id_router_3> is 7683
<port_id_router_4> is 7684
<port_id_router_5> is 7685

To exit the program, please use <Ctl+C>
