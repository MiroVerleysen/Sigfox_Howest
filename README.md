# IndustryProject_sigfox

## Wat is wat?

"AWS lambda function" is een Python programma met bijhorende dependencies om temperatuur, luchtvogtigheid en voltage van sigfox te versturen naar een online influxdb.

"Azure IoThub" is een C# programma met een iothubtrigger die temperatuur, luchtvogtigheid en voltage verstuurd naar influxdb. Er kan gewisseld worden tussen lokaal en online influxdb door de url, token en bucket aan te passen in Function1.

"Oefening laadpaal" is een oefening waarbij over sigfox wordt verstuurd wanneer een voertuig opgeladen heeft aan een laadpaal. Vervolgens wordt via teams over een webhook de kostprijs berekend. Deze map bevat python script + azure iothub trigger.

"Stuur data Pysense" is een Python programma om temperatuur, luchtvochtigheid en batterij info over het sigfox netwerk te sturen. Vervolgens kunnen er callback functies geconfigureerd worden via https://backend.sigfox.com/devicetype/list.
