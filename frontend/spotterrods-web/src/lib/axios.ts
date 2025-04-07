import axios from "axios";

export const api = axios.create({
  baseURL: "https://spotter-rods.onrender.com/api/v1/",
  headers: {
    "Content-Type": "application/json",
  },
});