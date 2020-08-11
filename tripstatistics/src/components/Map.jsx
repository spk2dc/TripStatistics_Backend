import React, { useState } from "react";

export default function Map() {
  let map;

  const createMap = () => {
    // Create the script tag, set the appropriate attributes
    var script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.REACT_APP_API_KEY_1}&callback=initMap`;
    script.defer = true;

    console.log(`window.initMap -> map`, map);

    // Attach your callback function to the `window` object
    window.initMap = function () {
      map = new window.google.maps.Map(document.getElementById("map"), {
        center: { lat: -34.397, lng: 150.644 },
        zoom: 8,
      });
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

/* 
Sources: 

https://engineering.universe.com/building-a-google-map-in-react-b103b4ee97f1

https://developers.google.com/maps/documentation/javascript/overview#all

*/
