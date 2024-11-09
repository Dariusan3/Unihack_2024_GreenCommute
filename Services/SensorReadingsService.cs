using Microsoft.Extensions.Options;
using MongoDB.Driver;
using GreenCommuteAPI.Data;
using GreenCommute.Models;

namespace GreenCommute.Services
{
    public class SensorReadingsService
    {
        private readonly IMongoCollection<SensorReadings> _sensorReadingsCollection;

        public SensorReadingsService(IOptions<DatabaseSettings> settings)
        {
            var mongoClient = new MongoClient(settings.Value.Connection);
            var mongoDb = mongoClient.GetDatabase(settings.Value.DatabaseName);
            _sensorReadingsCollection = mongoDb.GetCollection<SensorReadings>(settings.Value.CollectionName);
        }

        //get all sensorReadings
        public async Task<List<SensorReadings>> GetAsync() => await _sensorReadingsCollection.Find(_ => true).ToListAsync();

        //get sensorReadings by id
        public async Task<SensorReadings> GetAsync(string id) =>
            await _sensorReadingsCollection.Find(x => x.Id == id).FirstOrDefaultAsync();

        //add new sensorReadings 
        public async Task CreateAsync(SensorReadings newSensorReadings) =>
            await _sensorReadingsCollection.InsertOneAsync(newSensorReadings);

        //update sensorReadings
        public async Task UpdateAsync(string id, SensorReadings updateSensorReadings) =>
            await _sensorReadingsCollection.ReplaceOneAsync(x => x.Id == id, updateSensorReadings);

        //delte sensorReadings
        public async Task DeleteAsync(string id) =>
            await _sensorReadingsCollection.DeleteOneAsync(x => x.Id == id);
    }
}
