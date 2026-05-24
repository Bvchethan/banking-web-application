import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8080/api"
});

api.interceptors.request.use((config) => {
  const stored = localStorage.getItem("banking_auth");
  if (stored) {
    const auth = JSON.parse(stored);
    config.headers.Authorization = `Bearer ${auth.token}`;
  }
  return config;
});

export default api;
