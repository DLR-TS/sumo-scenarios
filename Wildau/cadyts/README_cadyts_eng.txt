cadyts 

The "cadyts" tool is an another option for route selection based on counting data and route alternatives.
Cadyts carries out 100 iteration steps in which the probabilities of the route selection from a route file are tried to match the counting data.
For this purpose, the results of the previous iteration are evaluated in each iteration step and the probabilities are adjusted if necessary in order to get close to the counting data.
In order to be able to execute cadyts, however, a batch file ("cadyts.bat") must first be created, where by duaIterate ("duaIterate.bat") must be executed first.
DuaIterate creates an alternative route file for each iteration (the number of iterations depends on the time slot), which is then passed on to cadyts.

Note: The path name in the cadyts.bat must be adapted to your own path.

Cadyts requires the counting data in the format of a measurements file ("measurements.xml").

An output file can then be created.