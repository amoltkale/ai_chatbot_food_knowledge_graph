import React from 'react';
import { MapContainer as Map, TileLayer } from 'react-leaflet';
import { loadModules } from 'esri-loader';

class ArcGISMap extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      map: null,
      view: null,
    };
  }

  componentDidMount() {
    loadModules(['esri/Map', 'esri/views/MapView'], {
      css: true,
    }).then(([Map, MapView]) => {
      const map = new Map({
        basemap: 'streets',
      });

      const view = new MapView({
        container: 'map-container',
        map: map,
        zoom: 12,
        center: [-118.244, 34.052],
      });

      this.setState({ map, view });
    });
  }

  render() {
    return (
      <div id="map-container">
        <Map center={[34.052, -118.244]} zoom={12}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        </Map>
      </div>
    );
  }
}

export default ArcGISMap;
