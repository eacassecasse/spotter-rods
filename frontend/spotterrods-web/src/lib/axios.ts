import axios from "axios";

export const api = axios.create({
  baseURL: "https://spotter-rods.onrender.com/",
  headers: {
    "Content-Type": "application/json",
  },
});