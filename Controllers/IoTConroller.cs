using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.Devices.Client;
using System.Threading.Tasks;

[ApiController]
[Route("api/iot")]
public class IoTController : ControllerBase
{
    private readonly DeviceClient _deviceClient;

    public IoTController(IConfiguration configuration)
    {
        string connectionString = configuration["Azure:ConnectionString"];
        _deviceClient = DeviceClient.CreateFromConnectionString(connectionString, TransportType.Mqtt);
    }

    [HttpPost("send-test-message")]
    public async Task<IActionResult> SendTestMessage()
    {
        var message = new Message(System.Text.Encoding.ASCII.GetBytes("Test message from API"));
        await _deviceClient.SendEventAsync(message);
        return Ok("Test message sent to IoT Hub.");
    }
}
