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
using JNogueira.Discord.Webhook.Client;
using Teams.Notifications;
using System.Collections.Generic;
using InfluxDB.Client.Core;
using InfluxDB.Client;
using InfluxDB.Client.Api.Domain;
using SendGrid;
using SendGrid.Helpers.Mail;

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

        public static string nummerplaat = "not_known";
        [FunctionName("IoTHubListener")]
        public async void Run([IoTHubTrigger("messages/events", Connection = "IotConnection")] EventData message, ILogger log)
        {
        log.LogInformation($"message: {Encoding.UTF8.GetString(message.Body.Array)}");
            string bericht = Encoding.UTF8.GetString(message.Body.Array);
            Console.WriteLine("------------------");
            Data data = JsonConvert.DeserializeObject<Data>(bericht);
            string hex_data = data.data;
            string id = data.device;
            int lengte = hex_data.Length;
            if (lengte == 14)
            {
                nummerplaat = ConvertHexToString(hex_data);
                nummerplaat = nummerplaat.Insert(1, "-");
                nummerplaat = nummerplaat.Insert(5, "-");
                Console.WriteLine("Voertuig met kenteken: " + nummerplaat + " begon met opladen aan een laadpaal met ID: " + id + ".");
            }
            else if (lengte == 8)
            {
                float seconden = ConvertHexToFloat(hex_data);
                float kwh = 0.22f;
                float kws = kwh / 3600;
                float kostprijs = kws * seconden;
                double prijs = Math.Round(kostprijs, 2);
                TimeSpan t = TimeSpan.FromSeconds(seconden);
                string tijd = string.Format("{0:D2}h:{1:D2}m:{2:D2}s",t.Hours,t.Minutes,t.Seconds);
                Console.WriteLine("Voertuig met kenteken: " + nummerplaat + " heeft: " + tijd + " opgeladen. \nDe kostprijs hiervan bedraagt: " + prijs + " euro.");
                SendTeamsMessage(tijd, kostprijs, nummerplaat, id);
                recordInflux.devicename = id;
                recordInflux.kostrprijs = prijs;
                recordInflux.nummerplaat = nummerplaat;
                recordInflux.oplaadtijd = seconden;
                await Stuurdata();
            }
            else if (lengte == 12)
            {
                await SendMail(id);
            }

        }
        static async Task SendMail(string id)
        {
            var apiKey = "<sendgrid_api_key>";
            var client = new SendGridClient(apiKey);
            var from = new EmailAddress("miro123@hotmail.be", "example user");
            var subject = "Laadpaal is nog steeds beschikbaar";
            var to = new EmailAddress("miroverleysen@gmail.com", "example user");
            var plainTextContent = "De laadpaal met id " + id + " is nog steeds beschikbaar.";
            var htmlContent = "<strong>De laadpaal met id " + id + " is nog steeds beschikbaar." + "</strong>";
            var msg = MailHelper.CreateSingleEmail(from, to, subject, plainTextContent, htmlContent);
            var response = await client.SendEmailAsync(msg);
        }
        private static float ConvertHexToFloat(string hexString)
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

                await writeApi.WriteMeasurementAsync("<bucket>", "<influxdb_organisation>", WritePrecision.Ns, recordInflux);


            }
            catch (Exception ex)
            {

                throw ex;
            }

        }

        private static void SendTeamsMessage(string tijd, float kostprijs, string nummerplaat, string id)
        {
            // Teams message
            var teamsclient = new TeamsNotificationClient("<teams_webhook>");
            var teamsmessage = new MessageCard();
            teamsmessage.Title = "Laadpaal";
            teamsmessage.Text = "U heeft zojuist uw voertuig met kenteken: "+ nummerplaat + " opgeladen aan een laadpaal met ID: " + id + ".";
            teamsmessage.Color = "4490b2";
            teamsmessage.Sections = new List<MessageSection>();
            teamsmessage.Sections.Add(new MessageSection()
            {
                Title = "Details:",
                Facts = new List<MessageFact>()
                                    {
                                        new MessageFact()
                                        {
                                            Name = "Duur van oplaadbeurt: ",
                                            Value = tijd
                                        },
                                        new MessageFact()
                                        {
                                            Name = "Kostprijs: ",
                                            Value = "€ " + Convert.ToString(kostprijs)
                                        },
                                        new MessageFact()
                                        {
                                            Name = "ID van laadpaal: ",
                                            Value = id
                                        },
                                    }
            });
            teamsclient.PostMessage(teamsmessage).GetAwaiter().GetResult();
            return;
        }
    }

    [InfluxDB.Client.Core.Measurement("SigfoxData")]
    public class SnowBallRecordInfluxDb
    {
        [Column("devicename", IsTag = true)]
        public string devicename { get; set; }

        [Column("nummerplaat", IsTag = true)]
        public string nummerplaat { get; set; }

        [Column("kostprijs")]
        public double kostrprijs { get; set; }

        [Column("oplaadtijd")]
        public float oplaadtijd { get; set; }

        [Column(IsTimestamp = true)]
        public DateTime Time;
    }
}