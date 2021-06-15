using IoTHubTrigger = Microsoft.Azure.WebJobs.EventHubTriggerAttribute;

using Microsoft.Azure.WebJobs;
using Microsoft.Azure.EventHubs;
using System.Text;
using Microsoft.Extensions.Logging;
using System.Threading.Tasks;
using Newtonsoft.Json;
using System;
using iothubsigfox.Models;
using System.Globalization;
using InfluxDB.Client;
using InfluxDB.Client.Api.Domain;
using InfluxDB.Client.Core;

namespace iothubsigfox
{
    public class Function1
    {
        SnowBallRecordInfluxDb recordInflux = new SnowBallRecordInfluxDb();
        private static InfluxDBClient influxDBClient = null;
        private static WriteApiAsync writeApi = null;
        public Function1()
        {

            if (influxDBClient == null)
                influxDBClient = InfluxDBClientFactory.Create("<influxdb_url>", "<influxdb_token>".ToCharArray());
            if (writeApi == null)
                writeApi = influxDBClient.GetWriteApiAsync();
        }

        [FunctionName("IoTHubListener")]
        public async void Run([IoTHubTrigger("messages/events", Connection = "connectionString")] EventData message, ILogger log)
        {
            log.LogInformation($"message: {Encoding.UTF8.GetString(message.Body.Array)}");
            string bericht = Encoding.UTF8.GetString(message.Body.Array);
            Console.WriteLine("------------------");
            Sigfoxlukasmiro sigfoxlukasmiro = JsonConvert.DeserializeObject<Sigfoxlukasmiro>(bericht);
            Console.WriteLine(sigfoxlukasmiro.data);
            Console.WriteLine("------------------");
            int aantalkeer = 0;
            float temp = 0;
            float humidity = 0;
            float bat = 0;
            foreach (var i in sigfoxlukasmiro.data.ChunkString(8))
            {
                switch (aantalkeer)
                {
                    case 0:
                        temp = ConvertHexToFloat(i);
                        recordInflux.temperatuur = temp;
                        break;
                    case 1:
                        humidity = ConvertHexToFloat(i);
                        recordInflux.humidity = humidity;
                        break;
                    case 2:
                        bat = ConvertHexToFloat(i);
                        recordInflux.batterij = bat;
                        break;
                    default:
                        break;
                }
                aantalkeer++;
            }
            recordInflux.devicename = sigfoxlukasmiro.device;
            Console.WriteLine("Device: " + sigfoxlukasmiro.device);
            Console.WriteLine("Temp: " + Convert.ToString(temp) + " �C");
            Console.WriteLine("Humidity: " + humidity.ToString() + " %");
            Console.WriteLine("Batterij: " + bat.ToString());
            await Stuurdata();
        }

        private float ConvertHexToFloat(string hexString)
        {
            // Converting to integer
            Int32 IntRep = Int32.Parse(hexString, NumberStyles.AllowHexSpecifier);
            // Integer to Byte[] and presenting it for float conversion
            float f = BitConverter.ToSingle(BitConverter.GetBytes(IntRep), 0);
            return f;
        }

        public string ConvertHexToString(string hexString)
        {
            try
            {
                string ascii = string.Empty;
                for (int i = 0; i < hexString.Length; i += 2)
                {
                    string hs = string.Empty;

                    hs = hexString.Substring(i, 2);
                    ulong decval = Convert.ToUInt64(hs, 16);
                    long deccc = Convert.ToInt64(hs, 16);
                    char character = Convert.ToChar(deccc);
                    ascii += character;
                }
                return ascii;
            }
            catch (Exception ex) { Console.WriteLine(ex.Message); }
            return string.Empty;
        }

        public async Task Stuurdata()
        {
            try
            {
                Console.WriteLine("Start");

                await writeApi.WriteMeasurementAsync("<bucket>", "<Organisation>", WritePrecision.Ns, recordInflux);


            }
            catch (Exception ex)
            {

                throw ex;
            }

        }
    }

    [InfluxDB.Client.Core.Measurement("SigfoxData")]
    public class SnowBallRecordInfluxDb
    {
        [Column("devicename", IsTag = true)]
        public string devicename { get; set; }

        [Column("temp")]
        public float temperatuur { get; set; }

        [Column("humidity")]
        public float humidity { get; set; }

        [Column("batterij")]
        public float batterij { get; set; }

        [Column(IsTimestamp = true)]
        public DateTime Time;
    }
}