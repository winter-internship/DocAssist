// src/router/index.ts
import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

import DashboardHome from "@/pages/DashboardHome.vue";
import UploadPage from "@/pages/UploadPage.vue";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "home",
    component: DashboardHome,
  },
  {
    path: "/upload",
    name: "upload",
    component: UploadPage,
  },

  // 나중에 페이지 만들면 여기 추가하면 됨
  // { path: "/drive", name: "drive", component: () => import("@/pages/DrivePage.vue") },
  // { path: "/qa", name: "qa", component: () => import("@/pages/QaPage.vue") },
  // { path: "/terms", name: "terms", component: () => import("@/pages/TermsPage.vue") },
  // { path: "/profile", name: "profile", component: () => import("@/pages/ProfilePage.vue") },
  // { path: "/guide", name: "guide", component: () => import("@/pages/GuidePage.vue") },
  // { path: "/docs/:id", name: "documentView", component: () => import("@/pages/DocComparePage.vue") },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
