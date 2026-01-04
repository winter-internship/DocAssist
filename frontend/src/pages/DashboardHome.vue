<template>
  <AppLayout v-slot="{ toggleSidebar }">
    <!-- Top Bar -->
    <header class="topbar">
      <div class="tb-left">
        <!-- Mobile hamburger -->
        <button class="hamburger" @click="toggleSidebar" aria-label="Open menu">☰</button>
        <div class="tb-title-strong">DoQ · 문서 이해 보조 시스템</div>
      </div>

      <!-- Desktop Search -->
      <div class="tb-center">
        <input class="tb-search" placeholder="문서 검색" v-model="sidebarQ" />
      </div>

      <div class="tb-right">
        <button class="btn btn-ghost" @click="goDrive">내 드라이브</button>
      </div>
    </header>

    <!-- Content -->
    <main class="container">
      <!-- Hero -->
      <section class="hero">
        <div class="hero-left">
          <h1>
            전문 문서를 <span class="accent">원문 그대로</span> 두고,<br />
            이해를 돕는 설명 레이어를 제공합니다.
          </h1>
          <p>
            PDF/이미지 문서를 업로드하면 텍스트 추출 → 용어 설명 → 문장·문단별 이해 보조 결과를
            생성합니다.
          </p>
          <div class="hero-actions">
            <button class="btn btn-primary btn-lg" @click="goUpload">문서 업로드 시작</button>
          </div>
        </div>

        <div class="hero-right">
          <div class="hero-card">
            <div class="hero-card-title">오늘의 요약</div>
            <div class="stat-grid">
              <div class="stat">
                <div class="stat-label">총 문서</div>
                <div class="stat-value">{{ stats.totalDocs }}</div>
              </div>
              <div class="stat">
                <div class="stat-label">분석 완료</div>
                <div class="stat-value">{{ stats.done }}</div>
              </div>
              <div class="stat">
                <div class="stat-label">분석 중</div>
                <div class="stat-value">{{ stats.processing }}</div>
              </div>
              <div class="stat">
                <div class="stat-label">이번 주 Q&A</div>
                <div class="stat-value">{{ stats.weekQa }}</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Recent Docs -->
      <section class="grid">
        <article class="card card-large">
          <div class="card-head">
            <h2>최근 업로드 문서</h2>
            <button class="link" @click="goDrive">전체 보기 →</button>
          </div>

          <div v-if="recentDocs.length === 0" class="empty">
            아직 업로드된 문서가 없습니다.
            <button class="inline" @click="goUpload">업로드</button>
            해보세요.
          </div>

          <ul v-else class="list">
            <li v-for="doc in recentDocs" :key="doc.id" class="list-item">
              <div>
                <div class="doc-title">{{ doc.title }}</div>
                <div class="doc-meta">
                  <span class="chip">{{ doc.type }}</span>
                  <span class="muted">{{ formatDate(doc.createdAt) }}</span>
                </div>
              </div>

              <div class="doc-right">
                <span :class="['badge', badgeClass(doc.status)]">{{ statusLabel(doc.status) }}</span>
                <button class="btn btn-sm" :disabled="doc.status !== 'done'" @click="openDocument(doc.id)">
                  열기
                </button>
              </div>
            </li>
          </ul>
        </article>
      </section>

      <!-- Recent Activity -->
      <section class="card">
        <div class="card-head">
          <h2>최근 활동</h2>
        </div>

        <ul v-if="activities.length" class="activity">
          <li v-for="a in activities" :key="a.id" class="activity-item">
            <span class="dot" />
            <div>
              <div class="activity-title">{{ a.title }}</div>
              <div class="muted">{{ formatDateTime(a.at) }}</div>
            </div>
          </li>
        </ul>

        <div v-else class="empty">최근 활동이 없습니다.</div>
      </section>
    </main>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import documentService from "../api/document.service";
import AppLayout from "../components/layout/AppLayout.vue";

const router = useRouter();
const authStore = useAuthStore();

const sidebarQ = ref("");
const theme = ref<"light" | "dark">("light");

function applyTheme(next: "light" | "dark") {
  theme.value = next;
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("theme", next);
}

type DocStatus = "processing" | "done" | "failed";

interface DocItem {
  id: string;
  title: string;
  type: "PDF" | "JPG" | "PNG";
  status: DocStatus;
  createdAt: string; // ISO
}

interface ActivityItem {
  id: string;
  title: string;
  at: string; // ISO
}

/* API Data */
const recentDocs = ref<DocItem[]>([]);
const activities = ref<ActivityItem[]>([]); 
const stats = ref({
    totalDocs: 0,
    done: 0,
    processing: 0,
    weekQa: 0 
});

onMounted(async () => {
  const savedTheme = (localStorage.getItem("theme") as "light" | "dark") || "light";
  applyTheme(savedTheme);
  
  if (authStore.token && !authStore.user) {
      await authStore.fetchUser();
  }
  
  await fetchDashboardData();
});

async function fetchDashboardData() {
    try {
        const res = await documentService.getDocuments(0, 5);
        const docs = res.data;
        
        recentDocs.value = docs.map((d: any) => ({
            id: d.id,
            title: d.title,
            type: d.file_type || "UNK",
            status: d.status.toLowerCase(),
            createdAt: d.created_at
        }));

        const allRes = await documentService.getDocuments(0, 100);
        const allDocs = allRes.data;
        
        stats.value.totalDocs = allDocs.length;
        stats.value.done = allDocs.filter((d: any) => d.status === "DONE").length;
        stats.value.processing = allDocs.filter((d: any) => d.status === "PROCESSING" || d.status === "QUEUED").length;
        stats.value.weekQa = 0; 

    } catch (e) {
        console.error("Dashboard data fetch failed", e);
    }
}

function badgeClass(status: DocStatus) {
  switch (status) {
    case "done": return "badge-ok";
    case "processing": return "badge-warn";
    case "failed": return "badge-bad";
    default: return "";
  }
}
function statusLabel(status: DocStatus) {
  switch (status) {
    case "done": return "분석 완료";
    case "processing": return "분석 중";
    case "failed": return "실패";
    default: return status;
  }
}
function formatDate(iso: string) {
  const d = new Date(iso);
  return d.toLocaleDateString("ko-KR", { year: "numeric", month: "2-digit", day: "2-digit" });
}
function formatDateTime(iso: string) {
  const d = new Date(iso);
  return d.toLocaleString("ko-KR", { year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" });
}

/* Routes */
function goUpload() {
  router.push({ name: "upload" }).catch(() => console.log("업로드 페이지 준비 중..."));
}
function goDrive() {
  router.push({ name: "drive" }).catch(() => console.log("드라이브 페이지 준비 중..."));
}

function openDocument(docId: string) {
  router.push({ name: "documentView", params: { id: docId } }).catch(() => console.log("문서 보기 페이지 준비 중..."));
}
</script>

<style scoped>
/* Only Dashboard Specific Styles */
.topbar {
  background: var(--topbar-bg);
  border-bottom: 1px solid #e5e7eb;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
  align-items: center;
  padding: 0 18px;
  gap: 12px;
}

.tb-left {
  display: flex;
  align-items: center;
  gap: 10px;
  justify-self: start;
}
.tb-title-strong {
  font-weight: 1000;
  font-size: 16px;
  letter-spacing: -0.2px;
}

.tb-center {
  display: flex;
  justify-content: center;
  justify-self: center;
}
.tb-search {
  width: min(720px, 88vw);
  padding: 10px 14px;
  border-radius: 14px;
  border: 1px solid #e5e7eb;
  background: #f9fafb;
  font-weight: 800;
}

.tb-right {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
  justify-self: end;
}

.container {
  max-width: 1120px;
  margin: 0 auto;
  padding: 22px 16px 40px;
}

/* Hero */
.hero {
  display: grid;
  grid-template-columns: 1.35fr 0.65fr;
  gap: 16px;
  margin-bottom: 16px;
}

.hero-left {
  background: var(--card);
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 26px;
}
.hero-left h1 {
  margin: 0;
  font-size: 24px;
  line-height: 1.35;
}
.accent {
  background: #e0f2fe;
  padding: 2px 6px;
  border-radius: 8px;
}
.hero-left p {
  margin: 10px 0 0;
  color: #4b5563;
  line-height: 1.6;
}
.hero-actions {
  margin-top: 14px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.btn-lg {
  padding: 10px 18px;
  font-size: 15px;
}

.hero-right .hero-card {
  background: linear-gradient(180deg, #ffffff, #f9fafb);
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 18px;
  height: 100%;
}
.hero-card-title {
  font-weight: 800;
  margin-bottom: 10px;
}

.stat-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.stat {
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 12px;
  background: var(--card);
}
.stat-label {
  color: #6b7280;
  font-size: 12px;
}
.stat-value {
  font-weight: 900;
  font-size: 20px;
  margin-top: 6px;
}

/* Cards */
.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
  margin-bottom: 16px;
}
.card {
  background: var(--card);
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 16px;
}
.card-large {
  min-height: 328px;
}
.card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}
.card-head h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 900;
}

/* Lists */
.list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.list-item {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 12px;
  border: 1px solid #eef2f7;
  border-radius: 14px;
  margin-bottom: 10px;
}
.doc-title {
  font-weight: 800;
}
.doc-meta {
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.chip {
  font-size: 12px;
  border: 1px solid #e5e7eb;
  padding: 2px 8px;
  border-radius: 999px;
  background: #f9fafb;
}
.muted {
  color: #6b7280;
  font-size: 12px;
}
.doc-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.badge {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid transparent;
  white-space: nowrap;
}
.badge-ok {
  background: #ecfdf5;
  border-color: #a7f3d0;
  color: #065f46;
}
.badge-warn {
  background: #fffbeb;
  border-color: #fde68a;
  color: #92400e;
}
.badge-bad {
  background: #fef2f2;
  border-color: #fecaca;
  color: #991b1b;
}

/* Activity */
.activity {
  list-style: none;
  padding: 0;
  margin: 0;
}
.activity-item {
  display: flex;
  gap: 10px;
  padding: 10px 8px;
  border-bottom: 1px solid #f1f5f9;
}
.activity-item:last-child {
  border-bottom: none;
}
.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #3b82f6;
  margin-top: 6px;
}
.activity-title {
  font-weight: 700;
}

/* Empty / Buttons */
.empty {
  padding: 16px;
  border: 1px dashed #e5e7eb;
  border-radius: 14px;
  color: #6b7280;
  background: #fafafa;
}
.inline {
  border: none;
  background: transparent;
  color: #2563eb;
  font-weight: 800;
  cursor: pointer;
  padding: 0 2px;
}

.btn {
  border: 1px solid #e5e7eb;
  background: var(--card);
  padding: 10px 12px;
  border-radius: 12px;
  font-weight: 800;
  cursor: pointer;
}
.btn:hover {
  background: #f9fafb;
}
.btn-primary {
  background: #2563eb;
  border-color: #2563eb;
  color: #fff;
}
.btn-primary:hover {
  background: #1d4ed8;
}
.btn-ghost {
  background: #fff;
  border-color: transparent;
}
.btn-sm {
  padding: 8px 10px;
  border-radius: 10px;
  font-weight: 800;
}
.btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.link {
  border: none;
  background: transparent;
  color: #2563eb;
  font-weight: 900;
  cursor: pointer;
  padding: 6px 8px;
  border-radius: 10px;
}
.link:hover {
  background: #eff6ff;
}

/* Hamburger button styling */
.hamburger {
  display: none;
  font-size: 20px;
  background: transparent;
  border: none;
  cursor: pointer;
}

@media (max-width: 768px) {
  /* topbar simplify */
  .topbar {
    grid-template-columns: auto 1fr auto;
  }
  .tb-center {
    display: none;
  }

  .container {
    padding: 16px 12px 32px;
  }

  .hero {
    grid-template-columns: 1fr;
  }

  .hamburger {
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
