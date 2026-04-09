const BASE = import.meta.env.VITE_API_URL;

const headers = (isFormData = false) => {
  const token = localStorage.getItem("token");
  const h = { Authorization: `Bearer ${token}` };
  if (!isFormData) h["Content-Type"] = "application/json";
  return h;
};

export const api = {
  // AUTH
  login: (email, password) =>
    fetch(`${BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    }),

  register: (username, email, password) =>
    fetch(`${BASE}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    }),

  me: () =>
    fetch(`${BASE}/auth/me`, { headers: headers() }),

  logout: () =>
    fetch(`${BASE}/auth/logout`, {
      method: "POST",
      headers: headers(),
    }),

  // RECORDS
  getRecords: () =>
    fetch(`${BASE}/records`, { headers: headers() }),

  getRecord: (id) =>
    fetch(`${BASE}/records/${id}`, { headers: headers() }),

  createRecord: (body) =>
    fetch(`${BASE}/records`, {
      method: "POST",
      headers: headers(),
      body: JSON.stringify(body),
    }),

  updateRecord: (id, body) =>
    fetch(`${BASE}/records/me/${id}`, {
      method: "PATCH",
      headers: headers(),
      body: JSON.stringify(body),
    }),

  deleteRecord: (id) =>
    fetch(`${BASE}/records/me/${id}`, {
      method: "DELETE",
      headers: headers(),
    }),

  // ADMIN
  updateStatus: (id, status) =>
    fetch(`${BASE}/admin/records/${id}/status`, {
      method: "PATCH",
      headers: headers(),
      body: JSON.stringify({ status }),
    }),

  // IMAGES & VIDEOS
  uploadImage: (record_id, imageFile) => {
    const form = new FormData();
    form.append("record_id", record_id);
    form.append("image", imageFile);
    return fetch(`${BASE}/images`, {
      method: "POST",
      headers: headers(true),
      body: form,
    });
  },

  deleteImage: (id) =>
    fetch(`${BASE}/images/${id}`, {
      method: "DELETE",
      headers: headers(),
    }),

  uploadVideo: (record_id, videoFile) => {
    const form = new FormData();
    form.append("record_id", record_id);
    form.append("video", videoFile);
    return fetch(`${BASE}/videos`, {
      method: "POST",
      headers: headers(true),
      body: form,
    });
  },

  deleteVideo: (id) =>
    fetch(`${BASE}/videos/${id}`, {
      method: "DELETE",
      headers: headers(),
    }),
};