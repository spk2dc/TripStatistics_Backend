import React, { useState } from "react";

export default function Map() {
  const createMap = () => {
    // Create the script tag, set the appropriate attributes
    var script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.REACT_APP_API_KEY_1}&callback=initMap`;
    script.defer = true;

    // Attach your callback function to the `window` object
    window.initMap = function () {
      // JS API is loaded and available
    };

    // Append the 'script' element to 'head'
    document.head.appendChild(script);
  };

  return (
    <div>
      <h1>Map</h1>
      <div id='map'></div>
      {createMap()}
    </div>
  );
}
