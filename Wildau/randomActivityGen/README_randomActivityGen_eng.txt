randomActivityGen

The tool must first be installed additionally. To do this, "pip install -r testing / requirements.txt" and "pipwin install noise" must then be installed.

With the help of randomActivityGen the demand or the route selection can be generated within a network based on the number of inhabitants.
The network file ("Netzmodell2.net.xml") is particularly important here. This is transferred to the tool with the population of the city being defined in a separate file ("stats.xml").

After the batch file ("randombatch.bat") has been executed, an output file is created, which in the second step is assigned to the ActivityGen ("activitygenbatch.bat").
A route file is now created which can be carried on  with the duaRouter ("duarouter.bat").
The results can then be evaluated by the duaRouter using an output file.