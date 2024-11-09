using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Azure.Devices.Client;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace GreenCommuteAPI.BackgroundServices
{
    public class BackgroundIoTService : BackgroundService
    {
        private readonly IConfiguration _configuration;
        private readonly DeviceClient _deviceClient;

        public BackgroundIoTService(IConfiguration configuration)
        {
            _configuration = configuration;
            string connectionString = _configuration["Azure:ConnectionString"];
            _deviceClient = DeviceClient.CreateFromConnectionString(connectionString, TransportType.Mqtt);
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            Console.WriteLine("Receiving messages from Azure IoT Hub...");
            while (!stoppingToken.IsCancellationRequested)
            {
                var receivedMessage = await _deviceClient.ReceiveAsync();
                if (receivedMessage != null)
                {
                    string messageData = Encoding.ASCII.GetString(receivedMessage.GetBytes());
                    Console.WriteLine($"Received message: {messageData}");
                    await _deviceClient.CompleteAsync(receivedMessage);
                }
                await Task.Delay(1000, stoppingToken);
            }
        }
    }
}
