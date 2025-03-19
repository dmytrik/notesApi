import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import Home from "@/views/Home.vue";
import Auth from "@/views/Auth.vue";
import Analytics from "@/views/Analytics.vue";

const routes = [
  { path: "/", name: "Home", component: Home, meta: { requiresAuth: true } },
  { path: "/auth", name: "Auth", component: Auth },
  { path: "/analytics", name: "Analytics", component: Analytics, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next("/auth");
  } else {
    next();
  }
});

export default router;