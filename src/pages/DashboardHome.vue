<template>
  <div class="app">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sb-brand">
        <div class="sb-logo">
          <img src="/logo.png" alt="DoQ" />
        </div>
      </div>

      <nav class="sb-nav">
        <button class="sb-item active">
          <span class="ico">🏠</span><span class="txt">홈</span>
        </button>

        <button class="sb-item" @click="goDrive">
          <span class="ico">🗂️</span><span class="txt">드라이브</span>
        </button>

        <button class="sb-item" @click="goUpload">
          <span class="ico">📤</span><span class="txt">업로드</span>
        </button>

        <button class="sb-item" @click="goQa">
          <span class="ico">💬</span><span class="txt">Q&A</span>
        </button>

        <!-- ✅ 용어집 추가 -->
        <button class="sb-item" @click="goTerms">
          <span class="ico">📚</span><span class="txt">용어집</span>
        </button>

        <div class="sb-sep"></div>

        <button class="sb-item" @click="goProfile">
          <span class="ico">👤</span><span class="txt">프로필</span>
        </button>

        <button v-if="isAdmin" class="sb-item" @click="goAdmin">
          <span class="ico">🛡️</span><span class="txt">관리자</span>
        </button>
      </nav>

      <div class="sb-bottom">
        <button class="sb-logout" @click="logout">log out</button>
      </div>
    </aside>

    <!-- Main -->
    <div class="main">
      <!-- Top Bar -->
      <header class="topbar">
        <div class="tb-left">
          <div class="tb-title-strong">DoQ · 문서 이해 보조 시스템 </div>
        </div>

        <!-- ✅ 중앙 Search -->
        <div class="tb-center">
          <input
            class="tb-search"
            placeholder="문서 검색"
            v-model="sidebarQ"
          />
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
              PDF/이미지 문서를 업로드하면 텍스트 추출 → 용어 설명 →
              문장·문단별 이해 보조 결과를 생성합니다.
            </p>
            <div class="hero-actions">
              <button class="btn btn-primary btn-lg" @click="goUpload">
                문서 업로드 시작
              </button>
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
                  <span :class="['badge', badgeClass(doc.status)]">
                    {{ statusLabel(doc.status) }}
                  </span>
                  <button
                    class="btn btn-sm"
                    :disabled="doc.status !== 'done'"
                    @click="openDocument(doc.id)"
                  >
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
    </div>
  </div>
</template>


<script setup lang="ts">
import { computed, ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const sidebarQ = ref("");
const theme = ref<"light" | "dark">("light");
const role = ref<"ADMIN" | "USER" | "">("");
const isAdmin = computed(() => role.value === "ADMIN");

function applyTheme(next: "light" | "dark") {
  theme.value = next;
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("theme", next);
}
function toggleTheme() {
  applyTheme(theme.value === "dark" ? "light" : "dark");
}

onMounted(() => {
  const savedTheme = (localStorage.getItem("theme") as "light" | "dark") || "light";
  applyTheme(savedTheme);
  role.value = (localStorage.getItem("role") as "ADMIN" | "USER") || "";
});

function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("role");
  localStorage.removeItem("user_name");
  localStorage.removeItem("user_email");
  localStorage.removeItem("remember_me");
  localStorage.removeItem("last_login_at");
  router.push({ name: "login" }).catch(() => {});
}

function goAdmin() {
  router.push({ name: "admin" }).catch(() => {});
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

const router = useRouter();

/**
 * TODO: FastAPI 연결 시 여기 데이터를 API로 교체
 * - GET /api/dashboard (stats, recent_docs, activities)
 */
const recentDocs = ref<DocItem[]>([
  {
    id: "doc_001",
    title: "사내 보안 정책 개정 안내",
    type: "PDF",
    status: "done",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 6).toISOString(),
  },
  {
    id: "doc_002",
    title: "고객 대상 서비스 이용약관 변경 공지",
    type: "PDF",
    status: "processing",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 20).toISOString(),
  },
  {
    id: "doc_003",
    title: "공공기관 민원 안내문(이미지)",
    type: "PNG",
    status: "failed",
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 30).toISOString(),
  },
]);

const activities = ref<ActivityItem[]>([
  {
    id: "a1",
    title: "'사내 보안 정책 개정 안내' 분석 완료",
    at: new Date(Date.now() - 1000 * 60 * 25).toISOString(),
  },
  {
    id: "a2",
    title: "문서 Q&A 질문 3건 생성",
    at: new Date(Date.now() - 1000 * 60 * 80).toISOString(),
  },
]);

const stats = computed(() => {
  const total = recentDocs.value.length;
  const done = recentDocs.value.filter((d) => d.status === "done").length;
  const processing = recentDocs.value.filter((d) => d.status === "processing").length;
  return {
    totalDocs: total,
    done,
    processing,
    weekQa: 7, // TODO: API 연동
  };
});

function badgeClass(status: DocStatus) {
  switch (status) {
    case "done":
      return "badge-ok";
    case "processing":
      return "badge-warn";
    case "failed":
      return "badge-bad";
  }
}

function statusLabel(status: DocStatus) {
  switch (status) {
    case "done":
      return "분석 완료";
    case "processing":
      return "분석 중";
    case "failed":
      return "실패";
  }
}

function formatDate(iso: string) {
  const d = new Date(iso);
  return d.toLocaleDateString("ko-KR", { year: "numeric", month: "2-digit", day: "2-digit" });
}

function formatDateTime(iso: string) {
  const d = new Date(iso);
  return d.toLocaleString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

/**
 * 라우팅: 너희 프로젝트 라우트 이름에 맞게 바꿔도 됨
 */
function goUpload() {
  router.push({ name: "upload" }).catch(() => {
    // 라우트가 없으면 홈으로 유지 (임시 처리)
    console.log("업로드 페이지 준비 중...");
  });
}
function goDrive() {
  router.push({ name: "drive" }).catch(() => {
    console.log("드라이브 페이지 준비 중...");
  });
}
function goQa() {
  router.push({ name: "qa" }).catch(() => {
    console.log("Q&A 페이지 준비 중...");
  });
}
function goProfile() {
  router.push({ name: "profile" }).catch(() => {
    console.log("프로필 페이지 준비 중...");
  });
}
function goTerms() {
  router.push({ name: "terms" }).catch(() => {
    console.log("용어집 페이지 준비 중...");
  });
}

function openDocument(docId: string) {
  // 비교/이해 화면으로 이동
  router.push({ name: "documentView", params: { id: docId } }).catch(() => {
    console.log("문서 보기 페이지 준비 중...");
  });
}
</script>

<style scoped>
:global(:root) {
  --b1: #1d4ed8;
  --b2: #0ea5e9;
  --ring: rgba(29, 78, 216, 0.18);
}

.app {  --ink: #111827;
  --bg: #f4f6fb;
  --line: #e5e7eb;
  --card: #ffffff;
  --card-solid: #ffffff;
  --muted: #6b7280;

  min-height: 100vh;
  display: grid;
  grid-template-columns: 280px 1fr;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR", Arial;
  color: var(--ink);
  background: var(--bg);
}
/* Sidebar */
.sidebar {
  background: rgba(255, 255, 255, 0.65);
  border-right: 1px solid #e5e7eb;
  backdrop-filter: blur(10px);
  padding: 16px 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.sb-brand {
  display: flex;
  align-items: center;
  gap: 0;
  padding: 10px 12px 12px;
}
.sb-logo {
  width: 84px;
  height: 84px;
  border-radius: 22px;
  display: grid;
  place-items: center;
  overflow: hidden;
  margin-left: 0;
}
.sb-logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
.sb-name {
  font-weight: 1000;
  letter-spacing: -0.2px;
}

.sb-search {
  padding: 0 6px 6px;
}
.sb-input {
  width: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.7);
  outline: none;
  font-weight: 900;
}
.sb-input:focus {
  box-shadow: 0 0 0 3px var(--ring);
}

.sb-nav {
  display: grid;
  gap: 6px;
  padding: 0 6px;
}
.sb-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 14px;
  border: 1px solid transparent;
  background: transparent;
  cursor: pointer;
  color: inherit;
  font-weight: 950;
  text-align: left;
}
.sb-item:hover {
  background: rgba(29, 78, 216, 0.08);
  border-color: rgba(29, 78, 216, 0.14);
}
.sb-item.active {
  background: rgba(29, 78, 216, 0.12);
  border-color: rgba(29, 78, 216, 0.18);
}
.ico {
  width: 18px;
  display: grid;
  place-items: center;
}
.txt {
  font-size: 13px;
}
.sb-sep {
  height: 1px;
  background: #e5e7eb;
  margin: 6px 0;
}
.sb-bottom {
  margin-top: auto;
  display: flex;
  gap: 8px;
  padding: 8px 6px 0;
}

  .sb-logout {
    width: 100%;
    border-radius: 14px;
    border: 1px solid #2563eb;
    background: #2563eb;
    color: #fff;
    cursor: pointer;
    font-weight: 900;
    padding: 10px 12px;
    text-align: center;
  }
.sb-mini {
  width: 40px;
  height: 40px;
  border-radius: 14px;
  border: 1px solid #e5e7eb;
  background: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  font-size: 16px;
}

/* Main */
.main {
  display: grid;
  grid-template-rows: 76px 1fr;
}

.topbar {
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
  align-items: center;
  padding: 0 18px;
  gap: 12px;
}
.tb-left {
  display: grid;
  gap: 6px;
  justify-self: start;
}
.tb-title {
  display: flex;
  align-items: baseline;
  gap: 8px;
}
.tb-title-strong {
  font-weight: 1000;
  font-size: 16px;
  letter-spacing: -0.2px;
}
.tb-sub {
  color: #6b7280;
  font-size: 12px;
  font-weight: 700;
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

.hero {
  display: grid;
  grid-template-columns: 1.35fr 0.65fr;
  gap: 16px;
  margin-bottom: 16px;
}

.hero-left {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 18px;
}
.hero-left h1 {
  margin: 0;
  font-size: 22px;
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
  background: #fff;
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

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 16px;
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

.quick {
  display: grid;
  gap: 10px;
}
.quick-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 14px;
  border: 1px solid #eef2f7;
  background: #fff;
  cursor: pointer;
  text-align: left;
}
.quick-item:hover {
  border-color: #dbeafe;
  background: #f8fbff;
}
.quick-icon {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  background: #eff6ff;
}
.quick-title {
  font-weight: 900;
}
.quick-desc {
  color: #6b7280;
  font-size: 12px;
  margin-top: 2px;
}

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
  background: #fff;
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
.btn-outline {
  background: #fff;
  border-color: #cbd5e1;
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

@media (max-width: 940px) {
  .hero {
    grid-template-columns: 1fr;
  }
  .grid {
    grid-template-columns: 1fr;
  }
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

.btn-lg {
  padding: 10px 18px;
  font-size: 15px;
}

.card-large {
  min-height: 328px;
}

.grid {
  grid-template-columns: 1fr;
}

.hero-left {
  padding: 26px;
}

.hero-left h1 {
  font-size: 24px;
}

</style>















