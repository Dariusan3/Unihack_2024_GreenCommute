import { useEffect, useState } from "react";

export default function Home() {
  const [sensorReadings, setSensorReadings] = useState([]);
  const [sid, setSid] = useState("");

  const handleModal = (hide) => {
    const deleteModal = document.querySelector(".delete-modal");
    if (deleteModal) {
      if (hide) {
        deleteModal.classList.add("hidden");
      } else {
        deleteModal.classList.remove("hidden");
      }
    }
  };

  const openDeleteModal = (id) => {
    setSid(id);
    handleModal(false);
  };

  const deleteSensorReading = () => {
    fetch("api/sensorreadings/" + sid, {
      method: "DELETE",
    })
      .then((r) => {
        console.log("Response for deleting a sensor reading: ", r);
        handleModal(true);
        setSensorReadings(sensorReadings.filter(reading => reading.id !== sid));
      })
      .catch((e) => console.log("Error deleting a sensor reading: ", e));
  };

  useEffect(() => {
    fetch("api/sensorreadings")
      .then((r) => r.json())
      .then((d) => {
        console.log("The sensor readings are: ", d);
        setSensorReadings(d);
      })
      .catch((e) => console.log("Error fetching sensor readings: ", e));
  }, []);

  return (
    <main>
      <h1>Sensor Readings Management</h1>
      <div className="add-btn">
        <a href="/new">+</a>
      </div>

      <table>
        <thead>
          <tr>
            <th>Sensor ID</th>
            <th>Latitude</th>
            <th>Longitude</th>
            <th>City</th>
            <th>Timestamp</th>
            <th>Temperature (°C)</th>
            <th>Humidity (%)</th>
            <th>Air Quality Index</th>
            <th>CO2 Level (ppm)</th>
            <th>PM2.5 (µg/m³)</th>
            <th>Traffic Density</th>
            <th>Delete</th>
          </tr>
        </thead>
        <tbody>
          {sensorReadings.length === 0 ? (
            <tr className="row waiting">
              <td colSpan="12" className="row">Loading<span className="loading">...</span></td>
            </tr>
          ) : (
            sensorReadings.map((reading) => (
              <tr key={reading.id}>
                <td>{reading.sensorId}</td>
                <td>{reading.location.latitude}</td>
                <td>{reading.location.longitude}</td>
                <td>{reading.location.city}</td>
                <td>{new Date(reading.timestamp).toLocaleString()}</td>
                <td>{reading.temperature}</td>
                <td>{reading.humidity}</td>
                <td>{reading.airQualityIndex}</td>
                <td>{reading.CO2Level}</td>
                <td>{reading.PM2_5}</td>
                <td>{reading.trafficDensity}</td>
                <td onClick={() => openDeleteModal(reading.id)}>Delete</td>
              </tr>
            ))
          )}
        </tbody>
      </table>

      <section className="delete-modal hidden">
        <div className="modal-item">
          <h3>Delete Sensor Reading</h3>
          <p>Are you sure you want to delete this sensor reading?</p>
          <div className="row mt-20 justify-btw">
            <div className="btn cancel" onClick={() => handleModal(true)}>Cancel</div>
            <div className="btn add" onClick={deleteSensorReading}>Delete</div>
          </div>
        </div>
      </section>
    </main>
  );
}
