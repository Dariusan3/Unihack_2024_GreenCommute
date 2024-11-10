const { createProxyMiddleware } = require("http-proxy-middleware");
const { env } = require("process");

// const target = env.ASPNETCORE_HTTPS_PORT
//   ? `https://localhost:${env.ASPNETCORE_HTTPS_PORT}`
//   : env.ASPNETCORE_URLS
//   ? env.ASPNETCORE_URLS.split(";")[0]
//   : "https://localhost:44428"; // Default port

const target = "https://localhost:7234"; // Ensure this matches your backend port

const context = [
  "/weatherforecast",
  "/api/sensorreadings", // Ensure this matches your backend route
  "/api/iot", // Example additional endpoint
  "/api/optimalrouteresults",
];

module.exports = function (app) {
  const appProxy = createProxyMiddleware(context, {
    target: target,
    secure: false, // Keep false for self-signed certificates in development
    changeOrigin: true,
    logLevel: "debug", // Enable detailed logging for debugging
    headers: {
      Connection: "Keep-Alive",
    },
  });

  app.use(appProxy);
};
