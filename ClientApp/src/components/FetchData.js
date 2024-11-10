import React, { Component } from "react";

export class FetchData extends Component {
  static displayName = FetchData.name;

  constructor(props) {
    super(props);
    this.state = { forecasts: [], optimalRouteResults: [], loading: true };
  }

  componentDidMount() {
    this.populateWeatherData();
    this.populateOptimalRouteResultsData();
  }

  static renderForecastsTable(forecasts) {
    return (
      <table className="table table-striped" aria-labelledby="tabelLabel">
        <thead>
          <tr>
            <th>Date</th>
            <th>Temp. (C)</th>
            <th>Temp. (F)</th>
            <th>Summary</th>
          </tr>
        </thead>
        <tbody>
          {forecasts.map((forecast) => (
            <tr key={forecast.date}>
              <td>{forecast.date}</td>
              <td>{forecast.temperatureC}</td>
              <td>{forecast.temperatureF}</td>
              <td>{forecast.summary}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }

  static renderOptimalRouteResults(optimalRouteResults) {
    return (
      <table className="table table-striped" aria-labelledby="tabelLabel">
        <thead>
          <tr>
            <th>ID</th>
            <th>Route</th>
            <th>Total weight</th>
          </tr>
        </thead>
        <tbody>
          {optimalRouteResults.map((optimalRouteResult) => (
            <tr key={optimalRouteResult.id}>
              <td>{optimalRouteResult.id}</td>
              <td>
                {optimalRouteResult.optimalRoute &&
                optimalRouteResult.optimalRoute.length > 0 ? (
                  optimalRouteResult.optimalRoute.map((route, index) => (
                    <span key={index}>
                      {route}
                      {index < optimalRouteResult.optimalRoute.length - 1 &&
                        ", "}
                    </span>
                  ))
                ) : (
                  <span>No routes available</span>
                )}
              </td>
              <td>{optimalRouteResult.totalWeight}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }

  render() {
    // let contents = this.state.loading ? (
    //   <p>
    //     <em>Loading...</em>
    //   </p>
    // ) : (
    //   FetchData.renderForecastsTable(this.state.forecasts)
    // );

    let contents = this.state.loading ? (
      <p>
        <em>Loading...</em>
      </p>
    ) : (
      FetchData.renderOptimalRouteResults(this.state.optimalRouteResults)
    );

    return (
      <div>
        <h1 id="tabelLabel">Optimal Route Results</h1>
        <p>This are the optimal route results</p>
        {contents}
      </div>
    );
  }

  async populateWeatherData() {
    const response = await fetch("weatherforecast");
    console.log("Response from backend for weather forecast: ", response);
    const data = await response.json();
    this.setState({ forecasts: data, loading: false });
  }

  async populateOptimalRouteResultsData() {
    try {
      const response = await fetch("/api/optimalrouteresults");
      console.log(
        "Response from backend for optimal route results: ",
        response
      );
      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }
      const data = await response.json();
      this.setState({ optimalRouteResults: data, loading: false });
    } catch (error) {
      console.error("Error fetching optimal route results:", error);
      this.setState({ loading: false }); // Stop loading if an error occurs
    }
  }
}
