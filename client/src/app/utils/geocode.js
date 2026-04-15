const cache = {};

export const reverseGeocode = async (lat, lng) => {
    const key = `${lat},${lng}`;
    if (cache[key]) return cache[key];
    if (!lat || !lng) return "Unknown location";
    try {
        const res = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=14&addressdetails=1&countrycodes=ke`
        );
        const data = await res.json();
        let name = "";
        
        if (data.address) {
            // Prefer suburb, city, town, or village
            name = data.address.suburb || data.address.city || data.address.town || data.address.village || data.address.state_district;
            if (!name && data.address.road) name = data.address.road;
        }
        
        if (!name) name = "Location unavailable";
        cache[key] = name;
        return name;
    } catch (err) {
        console.error("Reverse geocoding error:", err);
        return "Location unavailable";
    }
};