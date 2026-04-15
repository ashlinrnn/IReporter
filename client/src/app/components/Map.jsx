import { forwardRef, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, useMap, useMapEvents } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
});

const pinIcon = new L.Icon({
  iconUrl: "https://maps.google.com/mapfiles/ms/icons/blue-dot.png",
  iconSize: [32, 32],
});

function LocationPicker({ onLocationSelect }) {
  useMapEvents({
    click(e) {
      if (onLocationSelect) {
        onLocationSelect([e.latlng.lat, e.latlng.lng]);
      }
    },
  });
  return null;
}

const getMarkerIcon = (type) => {
  const color = type === "red flag" ? "red" : "blue";
  return new L.Icon({
    iconUrl: `https://maps.google.com/mapfiles/ms/icons/${color}-dot.png`,
    iconSize: [32, 32],
  });
};

// Helper component to fit map to Kenya bounds after loading
function FitToKenya() {
  const map = useMap();
  useEffect(() => {
    // Kenya bounding box: southwest to northeast
    const kenyaBounds = L.latLngBounds([-4.7, 33.9], [5.2, 41.9]);
    map.fitBounds(kenyaBounds);
  }, [map]);
  return null;
}

const Map = forwardRef(({ incidents = [], onSelect, onLocationSelect, selectedLocation }, ref) => {
  const validIncidents = incidents.filter(
    i => i.latitude != null && i.longitude != null && !isNaN(i.latitude) && !isNaN(i.longitude)
  );

  const isValidSelected = selectedLocation &&
    Array.isArray(selectedLocation) &&
    selectedLocation.length === 2 &&
    selectedLocation[0] != null &&
    selectedLocation[1] != null;

  return (
    <MapContainer
      center={[-1.286389, 36.817223]} // fallback center, will be overridden by FitToKenya
      zoom={6}                        // fallback zoom
      className="h-full w-full"
      ref={ref}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <LocationPicker onLocationSelect={onLocationSelect} />
      <FitToKenya />  {/* 👈 this ensures the map shows all of Kenya on load */}
      {isValidSelected && (
        <Marker position={selectedLocation} icon={pinIcon}>
          <Popup>📍 Incident location pinned</Popup>
        </Marker>
      )}
      {validIncidents.map((i) => (
        <Marker
          key={i.id}
          position={[i.latitude, i.longitude]}
          icon={getMarkerIcon(i.type)}
          eventHandlers={{ click: () => onSelect?.(i) }}
        >
          <Popup>
            <strong>{i.title}</strong><br />
            Type: {i.type}<br />
            Status: {i.status}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
});

export default Map;