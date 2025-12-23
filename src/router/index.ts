import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";

import DashboardHome from "@/pages/DashboardHome.vue";
import UploadPage from "@/pages/UploadPage.vue";
import DocComparePage from "@/pages/DocComparePage.vue";
import DrivePage from "@/pages/DrivePage.vue"; // ✅ 추가
import LoginPage from "@/pages/LoginPage.vue";
import SignupPage from "@/pages/SignupPage.vue";
import ForgotPasswordPage from "@/pages/ForgotPasswordPage.vue";
import TermsPage from "@/pages/TermsPage.vue";
import QaPage from "@/pages/QaPage.vue";
import ProfilePage from "@/pages/ProfilePage.vue";
import AdminPage from "@/pages/AdminPage.vue";





const routes: RouteRecordRaw[] = [
  { path: "/", name: "home", component: DashboardHome },
  { path: "/upload", name: "upload", component: UploadPage },
  { path: "/drive", name: "drive", component: DrivePage }, // ✅ 추가
  { path: "/docs/:id", name: "documentView", component: DocComparePage },
  { path: "/login", name: "login", component: LoginPage },
  { path: "/signup", name: "signup", component: SignupPage },
  { path: "/forgot-password", name: "forgotPassword", component: ForgotPasswordPage },
  { path: "/terms", name: "terms", component: TermsPage },
  { path: "/qa", name: "qa", component: QaPage },
  { path: "/profile", name: "profile", component: ProfilePage },
  { path: "/admin", name: "admin", component: AdminPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
