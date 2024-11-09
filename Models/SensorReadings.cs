using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace GreenCommute.Models
{
    public class SensorReadings
    {
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public string Id { get; set; }

        [BsonElement("sensorId")]
        public string SensorId { get; set; }

        [BsonElement("location")]
        public Location Location { get; set; }

        [BsonElement("timestamp")]
        public DateTime Timestamp { get; set; }

        [BsonElement("temperature")]
        public double Temperature { get; set; }

        [BsonElement("humidity")]
        public int Humidity { get; set; }

        [BsonElement("airQualityIndex")]
        public int AirQualityIndex { get; set; }

        [BsonElement("CO2Level")]
        public int CO2Level { get; set; }

        [BsonElement("PM2_5")]
        public int PM2_5 { get; set; }

        [BsonElement("trafficDensity")]
        public int TrafficDensity { get; set; }

        [BsonElement("noiseLevel")]
        public int? NoiseLevel { get; set; }  // Optional field

        [BsonElement("batteryStatus")]
        public int? BatteryStatus { get; set; }  // Optional field

        [BsonElement("status")]
        public string Status { get; set; }

        [BsonElement("source")]
        public string Source { get; set; }

        [BsonElement("weatherConditions")]
        public string WeatherConditions { get; set; }
    }

    public class Location
    {
        [BsonElement("latitude")]
        public double Latitude { get; set; }

        [BsonElement("longitude")]
        public double Longitude { get; set; }

        [BsonElement("city")]
        public string City { get; set; }
    }
}
