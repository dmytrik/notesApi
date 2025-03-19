import { defineStore } from "pinia";
import axios from "axios";

const api = axios.create({ baseURL: "http://localhost:8001/api/v1" });

const accessToken = localStorage.getItem("access_token");
if (accessToken) {
  api.defaults.headers.common["Authorization"] = "Bearer ${accessToken}";
}

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  user: { email: string } | null;
}

export const useAuthStore = defineStore("auth", {
  state: (): AuthState => ({
    accessToken: localStorage.getItem("access_token") as string | null,
    refreshToken: localStorage.getItem("refresh_token") as string | null,
    user: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },
  actions: {
    async login(credentials: { email: string; password: string }) {
      const response = await api.post("/auth/login/", credentials);
      this.setTokens(response.data);
      this.user = { email: credentials.email };
    },
    async register(credentials: { email: string; password: string }) {
      const response = await api.post("/auth/register/", credentials);
      this.user = response.data;
    },
    async refreshAccessToken() { 
      const response = await api.post("/auth/refresh/", { refresh_token: this.refreshToken });
      this.setTokens(response.data);
    },
    async logout() {
      this.accessToken = null;
      this.refreshToken = null;
      this.user = null;
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      delete api.defaults.headers.common["Authorization"];
    },
    setTokens({ access_token, refresh_token }: { access_token: string; refresh_token: string }) {
      this.accessToken = access_token;
      this.refreshToken = refresh_token;
      localStorage.setItem("access_token", access_token);
      localStorage.setItem("refresh_token", refresh_token);
      api.defaults.headers.common["Authorization"] = "Bearer ${access_token}";
    },
    async fetchNotes(): Promise<any[]> {
      console.log("Sending request with Authorization:", api.defaults.headers.common["Authorization"]);
      const response = await api.get('/notes/');
      return response.data;
    },
    async createNote(text: string): Promise<any> {
      console.log("Sending request with Authorization:", api.defaults.headers.common["Authorization"]);
      const response = await api.post("/notes/", { text });
      return response.data;
    },
    async fetchAnalytics(): Promise<any> {
      const response = await api.get("/notes/analytics/");
      return response.data;
    },
  },
});