# IndustryProject_sigfox

## Wat is wat?

"iothubsigfox" is een C# programma met een iothubtrigger die data verstuurd naar (lokale) influxdb. Er kan gewisseld worden tussen lokaal en online influxdb door de url, token en bucket aan te passen in Function1.

"lambda funtion" is een Python programma met bijhorende dependencies om testdata te versturen naar een online influxdb.

"sendData" is een Python programma om temperatuur, luchtvochtigheid en batterij info over het sigfox netwerk te sturen. Vervolgens kunnen er callback functies geconfigureerd worden via https://backend.sigfox.com/devicetype/list.