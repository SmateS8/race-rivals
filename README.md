# Race-Rivals
 * Pygame 2D top-down racing game
## Goal features vision
* Car Upgrades
    * You could upgrade your engine mainly for better top speed, gearbox for better acceleration or tires for better grip!
* Online Multiplayer
    * You could create a virtual party and than send its code to your friends, so they can connect and play with you.
* Online Account
    * You could create your in-game account, which you could use than for logging-in to the game. You could save your progress or directly invite your friends to a party.  

## Actual features
* Car upgrades
    * You can upgrade your engine for better top speed and your gearbox for better acceleration.
* Online Multiplayer
    * When you choose multiplayer from the menu, you will be joined into existing lobby or into new one if there is nobody already waiting. Then you independently race. Only your times count, who has better time - wins, and recieve coins, the one that lost will lost few coins as well.
* Online Account
    * You are forced to create a account with username and password by clicking the register button, then you can use the login for using your created account. Your account stores your balance and the performance of your car, so you can acces it anywhere (expecting you have your own public server)


# How to run the game
* Make sure you have python3 and pip installed on your machine.

* Install all dependencies
    * Navigate to the games directory and run `pip3 install requirements.txt`
* Run PLAY.py from the repository's root directory
    * The program will not run and notify you, that you need to run it correctly.
    ## How to run the server
    * In the server folder run api.py with python 3 interpreter.
        * For local use, use 127.0.0.1, for online, use server ip adress.
        * The port is 5000 by default
 
