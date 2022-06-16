--CRYPTORIDE--
    A simulation of a BlockChain CarPooling app.

--SUBJECT--
    Cryptology

--TEAM--
    DAVID OMAR LASCURAIN DÍAZ
    KHERI SAÚL CHAVIRA LEAL
    JULIO CÉSAR CAMPOS ESPARZA

--INSTALLING REQUIREMENTS--

-Python 3.9 or 3.+
-Ganache
-Python libraries: web3, pickle, threading, tkinter, tktimepicker, os, time, tkcalendar, PIL
-Pycharm Community 2022 (strongly recommended): https://www.jetbrains.com/es-es/pycharm/download/#section=windows
    -To install libraries using Pycharm IDE just go to the top of the "main.py" and "BlockChainController.py" and right
    click on any red underlined library and click "Show Context Actions" > "Import library_name" you can also use
    >>>pip install x  to manually install the libraries needed.

--INSTRUCTIONS--

NOTE: For saving data we store our users and rides in "offer_rides.pickle" and "all_users.pickle".
        -To reset all data simply just wipe out the content of the two files mentioned above and
        restart Ganache for a fresh start.

1. We use Ganache for the blockchain application, you just need to open it and click QuickStart, then go to "main.py"
in PyCharm and right-click on the code and select "Run" to start the app. (or just run "main.py" with your preferred
method.
2. To create a new account we click "Sign Up" you will need to put:
    - Avatar image      (using buttons - 5 avatars to chose-)
    - Username
    - Password
    - Ethereum address  (retrieve any address from Ganache)
   Then click "Create User".
3. In the main window select "Login" and put in your username and password and your profile should
appear in the bottom right corner.
4. Now you can publish a ride by selecting all the parameters in the bottom left corner, and when
you are ready you can click on the "Publish ride" and it will be shown in the list in the top left corner.
    -Base cost  (ether)
    -From time  (use scroll wheel to change while hovering)
    -To time    (use scroll wheel to change while hovering)
    -Location
    -Available seats
5. After that as a user you can also bid for any ride shown in the offer list, you just need to select the ride
type in an amount (must be higher than the cost shown in the list) and then click on "Bid".
    -Note: You can only have one ride published at a time, also you cannot bid if you are the driver of the ride.
6. When the "From time" of the ride is met in real time the ride is closed and now the driver user can
publish another ride if he/she wants.
7. You can simulate this behaviour with multiple accounts that are stored using the pickle library.

--EXTRA--

+ Recommendation: Create multiple accounts like the ones seen in "example.txt", and change the ethereum
address corresponding to your Ganache instance, then publish rides and bid for offer rides to test the system,
you will be able to see the transactions in Ganache.

Link demo video with audio (spanish) - https://drive.google.com/file/d/1-oY3Lq0ldoPJMsQcyiZsTWQMa5DV-06D/view?usp=sharing




