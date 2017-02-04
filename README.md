# worm-ssh
Create a worm that bruteforces SSH and "infect" the system.

This repo has three different type of worms which was created for a controlled environment with preknown username and passwords.
The worms find an IP with an open 22 port and infects the system and leaves a mark so it is not infected again. It does not infect
itself either.

# Replicator_worm.py
This worm simply replicates itself and leaves a mark that it "infeted" the system

# extortor_worm.py
This worm mimics a ransomware style worm. It encrypts the contents of the Documents folder and deletes the original.

# passwordthief_worm.py	
This worm steals the passwd file and sends it to the attacker.


