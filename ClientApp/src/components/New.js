import { useState } from "react";

export default function NewSensorReading(props) {
    const [reading, setReading] = useState({
        sensorId: "",
        location: {
            latitude: "",
            longitude: "",
            city: ""
        },
        timestamp: new Date().toISOString().split("T")[0],
        temperature: "",
        humidity: "",
        airQualityIndex: "",
        CO2Level: "",
        PM2_5: "",
        trafficDensity: "",
        noiseLevel: "",
        batteryStatus: "",
        status: "",
        source: "",
        weatherConditions: ""
    });

    const handleChange = (e) => {
        const { name, value } = e.target;

        if (name.includes("location.")) {
            const field = name.split(".")[1];
            setReading(prev => ({
                ...prev,
                location: {
                    ...prev.location,
                    [field]: value
                }
            }));
        } else {
            setReading(prev => ({
                ...prev,
                [name]: value
            }));
        }
    };

    const addNewReading = () => {
        console.log("The New Sensor Reading Is: ", reading);

        fetch("api/sensorreadings", {
            method: "POST",
            body: JSON.stringify(reading),
            headers: {
                "Content-Type": "application/json"
            }
        }).then(response => {
            console.log("Response from Backend for adding new sensor reading: ", response);
            window.location = "/";
        }).catch(error => console.log("Error adding new sensor reading: ", error));
    };

    return (
        <section className="m-20">
            <h1>Add New Sensor Reading</h1>

            <div className="mt-10">
                <label htmlFor="sensorId">Sensor ID</label>
                <input type="text" name="sensorId" id="sensorId" value={reading.sensorId} onChange={handleChange} />
            </div>

            <div className="mt-10">
                <label htmlFor="latitude">Latitude</label>
                <input type="number" step="0.0001" name="location.latitude" id="latitude" value={reading.location.latitude} onChange={handleChange} />
            </div>

            <div className="mt-10">
                <label htmlFor="longitude">Longitude</label>
                <input type="number" step="0.0001" name="location.longitude" id="longitude" value={reading.location.longitude} onChange={handleChange} />
            </div>

            <div className="mt-10">
                <label htmlFor="city">City</label>
                <input type="text" name="location.city" id="city" value={reading.location.city} onChange={handleChange} />
            </div>

            <div className="mt-10">
                <label htmlFor="timestamp">Timestamp</label>
                <input type="datetime-local" name="timestamp" id="timestamp" value={reading.timestamp} onChange={handleChange} />
            </div>

            <div className="mt-10">
                <label htmlFor="temperature">Temperature (°C)</label>
                <input type="number" step="0.1" name="temperature" id="temperature" value={reading.temperature} onChange={handleChange} />
            </div>

            <div className="mt-10">
                <label htmlFor="humidity">Humidity (%)</label>
                <input type="number" name="humidity" id="humidity" value={reading.humidity} onChange={handleChange} />
            </div>

            <div className="mt-10">
                <label htmlFor="airQualityIndex">Air Quality Index</label>
                <input type="number" name="airQualityIndex" id="airQualityIndex" value={reading.airQualityIndex} onChange={handleChange} />
            </div>

            <div className="mt-10">
                <label htmlFor="CO2Level">CO2 Level (ppm)</label>
                <input type="number" name="CO2Level" id="CO2Level" value={reading.CO2Level} onChange={handleChange} />
            </div>

            <div className="mt-10">
                <label htmlFor="PM2_5">PM2.5 (µg/m³)</label>
                <input type="number" name="PM2_5" id="PM2_5" value={reading.PM2_5} onChange={handleChange} />
            </div>

            <div className="mt-10">
                <label htmlFor="trafficDensity">Traffic Density</label>
                <input type="number" name="trafficDensity" id="trafficDensity" value={reading.trafficDensity} onChange={handleChange} />
            </div>

            <div className="mt-10">
                <label htmlFor="noiseLevel">Noise Level (dB)</label>
                <input type="number" name="noiseLevel" id="noiseLevel" value={reading.noiseLevel} onChange={handleChange} />
            </div>

            <div className="mt-10">
                <label htmlFor="batteryStatus">Battery Status (%)</label>
                <input type="number" name="batteryStatus" id="batteryStatus" value={reading.batteryStatus} onChange={handleChange} />
            </div>

            <div className="mt-10">
                <label htmlFor="status">Status</label>
                <input type="text" name="status" id="status" value={reading.status} onChange={handleChange} />
            </div>

            <div className="mt-10">
                <label htmlFor="source">Source</label>
                <input type="text" name="source" id="source" value={reading.source} onChange={handleChange} />
            </div>

            <div className="mt-10">
                <label htmlFor="weatherConditions">Weather Conditions</label>
                <input type="text" name="weatherConditions" id="weatherConditions" value={reading.weatherConditions} onChange={handleChange} />
            </div>

            <div className="mt-30 row p20 justify-btw">
                <div className="btn cancel" onClick={() => window.location = "/"}>Cancel</div>
                <div className="btn add" onClick={addNewReading}>Add</div>
            </div>
        </section>
    );
}
