flowRouter
Another tool for generating routes or generating traffic flows is the flowRouter. This is called in a batch file ("flowRouter.bat").

The network file and a detector file are transferred to the flowRouter. The detector file ("detectors.xml") contains defined loops, where by the number of vehicles that have passed this loop is indicated.

The type indicates whether it is an edge within the network or an edge where traffic flows going in or out.

The routes and flows are generated as output files after the batch file has been executed.
An output file can then be created again (see above) in order to compare input and output (transferred to an Excel table).
It is important for the (output) batch file that the flow file with the route file is also transferred with a "," in between.