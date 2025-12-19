<template>
  <div class="layout">
    <!-- Top Bar -->
    <header class="topbar">
      <div class="brand">
        <div class="logo">AI</div>
        <div class="brand-text">
          <div class="title">문서 이해 보조 시스템</div>
          <div class="subtitle">Dashboard</div>
        </div>
      </div>

      <div class="top-actions">
        <button class="btn btn-ghost" @click="goDrive">내 드라이브</button>
        <button class="btn btn-primary" @click="goUpload">+ 새 문서 업로드</button>
      </div>
    </header>

    <!-- Main -->
    <main class="container">
      <!-- Hero -->
      <section class="hero">
        <div class="hero-left">
          <h1>
            전문 문서를 <span class="accent">원문 그대로</span> 두고,<br />
            이해를 돕는 설명 레이어를 제공합니다.
          </h1>
          <p>
            PDF/이미지 문서를 업로드하면 텍스트 추출 → 용어 설명 → 문장/문단별 이해 보조 결과를
            생성합니다.
          </p>
          <div class="hero-actions">
            <button class="btn btn-primary" @click="goUpload">문서 업로드 시작</button>
            <button class="btn btn-outline" @click="goGuide">사용 가이드</button>
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

      <!-- Cards -->
      <section class="grid">
        <!-- Recent Docs -->
        <article class="card">
          <div class="card-head">
            <h2>최근 업로드 문서</h2>
            <button class="link" @click="goDrive">전체 보기 →</button>
          </div>

          <div v-if="recentDocs.length === 0" class="empty">
            아직 업로드된 문서가 없습니다. <button class="inline" @click="goUpload">업로드</button>
            해보세요.
          </div>

          <ul v-else class="list">
            <li v-for="doc in recentDocs" :key="doc.id" class="list-item">
              <div class="doc-left">
                <div class="doc-title">{{ doc.title }}</div>
                <div class="doc-meta">
                  <span class="chip">{{ doc.type }}</span>
                  <span class="muted">·</span>
                  <span class="muted">{{ formatDate(doc.createdAt) }}</span>
                </div>
              </div>

              <div class="doc-right">
                <span :class="['badge', badgeClass(doc.status)]">{{ statusLabel(doc.status) }}</span>
                <button
                  class="btn btn-sm"
                  :disabled="doc.status !== 'done'"
                  @click="openDocument(doc.id)"
                  title="분석 완료 문서만 열 수 있어요"
                >
                  열기
                </button>
              </div>
            </li>
          </ul>
        </article>

        <!-- Quick Actions -->
        <article class="card">
          <div class="card-head">
            <h2>빠른 작업</h2>
          </div>

          <div class="quick">
            <button class="quick-item" @click="goUpload">
              <div class="quick-icon">⬆️</div>
              <div>
                <div class="quick-title">문서 업로드</div>
                <div class="quick-desc">PDF/이미지 업로드 후 분석 시작</div>
              </div>
            </button>

            <button class="quick-item" @click="goQa">
              <div class="quick-icon">💬</div>
              <div>
                <div class="quick-title">문서 Q&A</div>
                <div class="quick-desc">문서 근거 기반으로 질문하기</div>
              </div>
            </button>

            <button class="quick-item" @click="goTerms">
              <div class="quick-icon">📚</div>
              <div>
                <div class="quick-title">용어집</div>
                <div class="quick-desc">추출된 전문 용어/정의 모아보기</div>
              </div>
            </button>

            <button class="quick-item" @click="goProfile">
              <div class="quick-icon">👤</div>
              <div>
                <div class="quick-title">프로필/설정</div>
                <div class="quick-desc">설명 깊이, 강조 표시 옵션</div>
              </div>
            </button>
          </div>
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
            <div class="activity-main">
              <div class="activity-title">{{ a.title }}</div>
              <div class="activity-sub muted">{{ formatDateTime(a.at) }}</div>
            </div>
          </li>
        </ul>

        <div v-else class="empty">최근 활동이 없습니다.</div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

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
function goGuide() {
  router.push({ name: "guide" }).catch(() => {
    console.log("가이드 페이지 준비 중...");
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
:root {
  color-scheme: light;
}

.layout {
  min-height: 100vh;
  background: #f6f7fb;
  color: #111827;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR", Arial;
}

.topbar {
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}
.logo {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: grid;
  place-items: center;
  background: #111827;
  color: #fff;
  font-weight: 800;
}
.brand-text .title {
  font-weight: 800;
  font-size: 14px;
}
.brand-text .subtitle {
  font-size: 12px;
  color: #6b7280;
  margin-top: 2px;
}

.top-actions {
  display: flex;
  gap: 10px;
  align-items: center;
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
</style>
