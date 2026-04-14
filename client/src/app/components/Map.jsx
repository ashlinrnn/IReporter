import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from "react-leaflet";
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

const getIcon = (status) => {
  const color = status === "red-flag" ? "red" : status === "investigating" ? "orange" : "green";
  return new L.Icon({
    iconUrl: `https://maps.google.com/mapfiles/ms/icons/${color}-dot.png`,
    iconSize: [32, 32],
  });
};

export default function Map({ incidents = [], onSelect, onLocationSelect, selectedLocation }) {
  const validIncidents = incidents.filter(
    i => i.latitude != null && i.longitude != null && !isNaN(i.latitude) && !isNaN(i.longitude)
  );

  // Validate selectedLocation similarly
  const isValidSelected = selectedLocation &&
    Array.isArray(selectedLocation) &&
    selectedLocation.length === 2 &&
    selectedLocation[0] != null &&
    selectedLocation[1] != null;
  return (
    <MapContainer center={[-1.286389, 36.817223]} zoom={13} className="h-full w-full">
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

      <LocationPicker onLocationSelect={onLocationSelect} />

      {isValidSelected && (
        <Marker position={selectedLocation} icon={pinIcon}>
          <Popup>📍 Incident location pinned</Popup>
        </Marker>
      )}

      {validIncidents.map((i) => (
        <Marker
          key={i.id}
          position={[i.latitude, i.longitude]}
          icon={getIcon(i.status)}
          eventHandlers={{ click: () => onSelect?.(i) }}
        >
          <Popup>
            <strong>{i.title}</strong><br />{i.status}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}