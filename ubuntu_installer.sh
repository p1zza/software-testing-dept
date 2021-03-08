RED='\e[31m'
BLUE='\e[34m'

echo -e "${RED}                                   [!] This Tool Must Run As ROOT [!]${NC}"
echo -e ${CYAN}              "Select Best Option : "
echo ""
echo -e "${WHITE}              [1] Installation "
echo -e "${WHITE}              [0] Exit "
echo -n -e "Z4nzu >> "
read choice
INSTALL_DIR="/usr/share/doc/software_testing_dept"
BIN_DIR="/usr/bin/"

if [ $choice == 1 ]; then 
	echo "[*] Checking Internet Connection .."
	wget -q --tries=10 --timeout=20 --spider https://google.com
	if [[ $? -eq 0 ]]; then
	    echo -e ${BLUE}"[?] Loading ... "
	    sudo apt-get update && apt-get upgrade 
	    sudo apt-get install python-pip
	    echo "[?] Checking directories..."
	    if [ -d "$INSTALL_DIR" ]; then
	        echo "[!] A Directory SoftTestingDept Was Found.. Do You Want To Replace It ? [y/n]:" ;
	        read input
	        if [ "$input" = "y" ]; then
	            rm -R "$INSTALL_DIR"
	        else
	            exit
	        fi
	    fi
    		echo "[?] Installing ...";
		echo "";
		git clone https://github.com/p1zza/software-testing-dept.git -b master "$INSTALL_DIR";
		echo "#!/bin/bash
		python3 $INSTALL_DIR/software_testing_dept.py" '${1+"$@"}' > software_testing_dept;
		sudo chmod +x software_testing_dept;
		sudo cp software_testing_dept /usr/bin/;
		rm software_testing_dept;
		echo ""; 
		echo "[?] Trying to installing Requirements ..."
		sudo apt-get install python3-pip
		sudo pip3 install PyQt5
		echo "[?] Turning off Ubuntu firewall ..."
		sudo uwf disable
		echo "[?] Current firewall status: "
		sudo uwf status
		
	else 
		echo -e $RED "Please Check Your Internet Connection ..!!"
	fi

if [ -d "$INSTALL_DIR" ]; then
    echo "";
    echo "[?] Successfuly Installed !!! ";
    echo "";
    echo "";
    echo -e $ORANGE "		[+]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[+]"
    echo 	"		[+]						      		[+]"
    echo -e $ORANGE "		[+]     		SoftTestingDept installed		[+]"
    echo	"		[+]						 		[+]"
    echo -e $ORANGE "		[+]+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++[+]"
    else
        echo "[?] Installation Failed !!! [?]";
        exit
    fi
elif [ $choice -eq 0 ];
then
    echo -e $RED "[?] THank Y0u !! [?] "
    exit
else 
    echo -e $RED "[!] Select Valid Option [!]"
fi
