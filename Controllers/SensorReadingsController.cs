using GreenCommute.Models;
using GreenCommute.Services;
using Microsoft.AspNetCore.Mvc;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace GreenCommuteAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class SensorReadingsController : ControllerBase
    {
        private readonly SensorReadingsService _sensorReadingsService;
        public SensorReadingsController(SensorReadingsService sensorReadingsService) 
        {
            _sensorReadingsService = sensorReadingsService;
        }

        // GET: api/<SensorReadingsController>
        [HttpGet]
        public async Task<List<SensorReadings>> Get() => await _sensorReadingsService.GetAsync();

        // GET api/<SensorReadingsController>/6473f1e9a98d7fbd29c234ef
        [HttpGet("{id:length(24)}")]
        public async Task<ActionResult<SensorReadings>> Get(string id)
        {
            SensorReadings sensorReadings = await _sensorReadingsService.GetAsync(id);
            if(sensorReadings == null)
            {
                return NotFound();
            }

            return sensorReadings;
        }

        // POST api/<SensorReadingsController>
        [HttpPost]
        public async Task<ActionResult<SensorReadings>> Post(SensorReadings newSensorReadings)
        {
            await _sensorReadingsService.CreateAsync(newSensorReadings);
            return CreatedAtAction(nameof(Get), new {id = newSensorReadings.Id}, newSensorReadings);

        }

        // PUT api/<SensorReadingsController>/6473f1e9a98d7fbd29c234ef
        [HttpPut("{id:length(24)}")]
        public async Task<ActionResult<SensorReadings>> Put(string id, SensorReadings updateSensorReadings)
        {
            SensorReadings sensorReadings = await _sensorReadingsService.GetAsync(id);
            if(sensorReadings == null)
            {
                return NotFound("There is no sensor readings with this id: " + id);
            }

            updateSensorReadings.Id = sensorReadings.Id;

            await _sensorReadingsService.UpdateAsync(id, updateSensorReadings);

            return Ok("Updated Successfully");
        }

        // DELETE api/<SensorReadingsController>/6473f1e9a98d7fbd29c234ef
        [HttpDelete("{id}")]
        public async Task<ActionResult> Delete(string id)
        {
            SensorReadings sensorReadings = await _sensorReadingsService.GetAsync(id);
            if (sensorReadings == null)
            {
                return NotFound("There is no sensor readings with this id: " + id);
            }

            await _sensorReadingsService.DeleteAsync(id);

            return Ok("Deleted Successfully");
        }
    }
}
