<template>
  <div class="app">
    <div class="overlay" v-if="sidebarOpen" @click="sidebarOpen = false" />
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ open: sidebarOpen }">
      <div class="sb-brand">
        <div class="sb-logo">
          <img src="/logo.png" alt="DoQ" />
        </div>
      </div>

      <div class="sb-search">
        <input class="sb-input" placeholder="Search" v-model="sidebarQ" />
      </div>

      <nav class="sb-nav">
        <button class="sb-item" @click="go('home')">
          <span class="ico">🏠</span><span class="txt">홈</span>
        </button>

        <button class="sb-item" @click="go('drive')">
          <span class="ico">🗂️</span><span class="txt">드라이브</span>
        </button>

        <button class="sb-item active">
          <span class="ico">📤</span><span class="txt">업로드</span>
        </button>

        <button class="sb-item" @click="go('qa')">
          <span class="ico">💬</span><span class="txt">Q&A</span>
        </button>
        <button class="sb-item" @click="go('terms')">
          <span class="ico">📚</span><span class="txt">용어집</span>
        </button>
        <div class="sb-sep"></div>

        <button class="sb-item" @click="go('profile')">
          <span class="ico">👤</span><span class="txt">프로필</span>
        </button>

        <button v-if="isAdmin" class="sb-item" @click="go('admin')">
          <span class="ico">🛡️</span><span class="txt">관리자</span>
        </button>
      </nav>

      <div class="sb-bottom">
        <button class="sb-logout" @click="logout">log out</button>
      </div>
    </aside>

    <!-- Main -->
    <div class="main">
      <!-- Topbar -->
      <header class="topbar">
        <div class="tb-left">
          <div class="tb-title">
            <button class="hamburger" @click="sidebarOpen = true" aria-label="Open menu">☰</button>
            <span class="tb-title-strong">문서 업로드</span>
            <span class="tb-sub">· PDF / JPG / PNG</span>
          </div>
        </div>
</header>

      <!-- Content -->
      <main class="content">
        <!-- Drop Zone -->
        <section class="card">
          <div
            class="dropzone"
            :class="{ dragging }"
            @dragenter.prevent="onDragEnter"
            @dragleave.prevent="onDragLeave"
            @dragover.prevent
            @drop.prevent="onDrop"
          >
            <div class="dz-icon">📄</div>
            <div class="dz-title">파일을 여기에 놓아 업로드하세요</div>
            <div class="dz-desc">
              또는 <button class="dz-link" type="button" @click="pickFile">파일 선택</button>
              으로 업로드할 수 있어요.
            </div>

            <input
              ref="fileInput"
              type="file"
              class="hidden"
              accept=".pdf,image/*"
              @change="onPick"
            />

            <div class="dz-actions">
              <button class="btn btn-primary" type="button" @click="pickFile">파일 선택</button>
              <button class="btn btn-ghost" type="button" :disabled="!selectedFile || uploading" @click="clearFile">
                선택 해제
              </button>
            </div>

            <div class="dz-meta">지원 포맷: PDF, JPG, PNG · 최대 20MB(예시)</div>
          </div>
        </section>

        <!-- Selected File -->
        <section class="card small" v-if="selectedFile">
          <div class="row">
            <div class="file">
              <div class="file-name">{{ selectedFile.name }}</div>
              <div class="file-sub">
                {{ humanSize(selectedFile.size) }} · {{ selectedFile.type || "unknown" }}
              </div>
            </div>

            <div class="actions">
              <button class="btn btn-primary" type="button" :disabled="uploading" @click="startUpload">
                {{ uploading ? "업로드/분석 중..." : "업로드 시작" }}
              </button>
              <button class="btn btn-outline" type="button" :disabled="uploading" @click="clearFile">
                취소
              </button>
            </div>
          </div>

          <div class="progress" v-if="uploading">
            <div class="bar" :style="{ width: progress + '%' }"></div>
          </div>

          <div class="hint" v-if="uploading">
            텍스트 추출 → 용어 분석 → 이해 보조 결과 생성 중...
          </div>
        </section>

        <!-- 안내 -->
        <section class="card small">
          <div class="next">
            <div class="next-title">업로드 후에는 무엇을 할 수 있나요?</div>
            <ul class="next-list">
              <li>원문과 “이해 보조 문서”를 나란히 비교</li>
              <li>전문 용어 클릭 시 정의/맥락 툴팁 제공</li>
              <li>문서 기반 Q&A로 추가 질문</li>
            </ul>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const sidebarQ = ref("");
const sidebarOpen = ref(false);
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
  sidebarOpen.value = false;
  localStorage.removeItem("access_token");
  localStorage.removeItem("role");
  localStorage.removeItem("user_name");
  localStorage.removeItem("user_email");
  localStorage.removeItem("remember_me");
  localStorage.removeItem("last_login_at");
  router.push({ name: "login" }).catch(() => {});
}

const fileInput = ref<HTMLInputElement | null>(null);
const selectedFile = ref<File | null>(null);

const dragging = ref(false);
const uploading = ref(false);
const progress = ref(0);

function go(name: string) {
  sidebarOpen.value = false;
  router.push({ name }).catch(() => {});
}

function pickFile() {
  fileInput.value?.click();
}

function onPick(e: Event) {
  const input = e.target as HTMLInputElement;
  const file = input.files?.[0] ?? null;
  selectedFile.value = file;
}

function onDragEnter() {
  dragging.value = true;
}
function onDragLeave() {
  dragging.value = false;
}
function onDrop(e: DragEvent) {
  dragging.value = false;
  const file = e.dataTransfer?.files?.[0] ?? null;
  if (!file) return;
  selectedFile.value = file;
}

function clearFile() {
  if (uploading.value) return;
  selectedFile.value = null;
  if (fileInput.value) fileInput.value.value = "";
}

function humanSize(bytes: number) {
  const units = ["B", "KB", "MB", "GB"];
  let v = bytes;
  let i = 0;
  while (v >= 1024 && i < units.length - 1) {
    v /= 1024;
    i++;
  }
  return `${v.toFixed(i === 0 ? 0 : 1)} ${units[i]}`;
}

/**
 * ✅ 업로드 완료 후 문서 비교 화면으로 이동:
 * router name: "documentView"
 * path: /docs/:id
 *
 * TODO(FastAPI 연결):
 * - POST /api/documents/upload  (multipart/form-data)
 * - 응답으로 document_id 받고 → documentView로 이동
 */
async function startUpload() {
  if (!selectedFile.value) return;

  uploading.value = true;
  progress.value = 0;

  // 가짜 진행률
  const timer = window.setInterval(() => {
    progress.value = Math.min(progress.value + Math.random() * 16, 96);
  }, 220);

  try {
    // ✅ 실제 업로드 연결 시(예시)
    // const form = new FormData();
    // form.append("file", selectedFile.value);
    // const res = await fetch("http://localhost:8000/api/documents/upload", {
    //   method: "POST",
    //   body: form,
    // });
    // if (!res.ok) throw new Error("Upload failed");
    // const data = await res.json(); // { document_id: "..." }
    // const docId = data.document_id;

    // ✅ 지금은  1.8초 후 성공 처리
    await new Promise((r) => setTimeout(r, 1800));
    progress.value = 100;

    await new Promise((r) => setTimeout(r, 250));

    // ✅ 핵심: 업로드 완료 → 문서 비교 화면 이동
    const docId = "doc_demo"; // 나중엔 백엔드 응답값으로 바꾸기
    router.push({ name: "documentView", params: { id: docId } }).catch(() => {});
  } catch (e) {
    alert("업로드에 실패했어요. 다시 시도해주세요.");
  } finally {
    window.clearInterval(timer);
    uploading.value = false;
  }
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
/* ? Mobile overlay (default hidden) */
.overlay {
  display: none;
}
.hamburger {
  display: none;
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

/* Topbar */
.topbar {
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 18px;
min-height: 76px; }
.tb-title {
  display: flex;
  align-items: baseline;
  gap: 8px;
}
.tb-title-strong {
  font-weight: 900;
  font-size: 16px;
}
.tb-sub {
  color: #6b7280;
  font-size: 12px;
}
/* Content */
.content {
  max-width: 1480px;
  width: 100%;
  margin: 0 auto;
  padding: 16px 12px 32px;
  display: grid;
  gap: 16px;
  justify-items: stretch;
}

.card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 16px;
}
.card.small {
  padding: 14px 16px;
}

/* Dropzone */
.dropzone {
  border: 2px dashed #d1d5db;
  border-radius: 18px;
  padding: 16px;
  text-align: center;
  background: #fafbff;
  margin-bottom: 24px;
  min-height: 360px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
}
.dropzone.dragging {
  border-color: #2563eb;
  background: #eff6ff;
}
.dz-icon {
  font-size: 34px;
  margin-bottom: 10px;
}
.dz-title {
  font-weight: 900;
  font-size: 18px;
  margin-bottom: 8px;
}
.dz-desc {
  color: #6b7280;
  font-size: 13px;
}
.dz-link {
  border: none;
  background: transparent;
  color: #2563eb;
  font-weight: 900;
  cursor: pointer;
  padding: 0 2px;
}
.dz-actions {
  margin-top: 16px;
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}
.dz-meta {
  margin-top: 14px;
  color: #9ca3af;
  font-size: 12px;
}

.hidden {
  display: none;
}

/* File row */
.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.file-name {
  font-weight: 900;
}
.file-sub {
  color: #6b7280;
  font-size: 12px;
  margin-top: 4px;
}
.actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* Progress */
.progress {
  margin-top: 12px;
  height: 10px;
  background: #eef2ff;
  border-radius: 999px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
}
.bar {
  height: 100%;
  background: #2563eb;
  width: 0%;
  transition: width 140ms linear;
}
.hint {
  margin-top: 10px;
  color: #6b7280;
  font-size: 12px;
}

/* Next */
.next-title {
  font-weight: 900;
  margin-bottom: 8px;
}
.next-list {
  margin: 0;
  padding-left: 18px;
  color: #4b5563;
  line-height: 1.7;
  font-size: 13px;
}

/* Buttons */
.btn {
  border: 1px solid #e5e7eb;
  background: #fff;
  padding: 10px 14px;
  border-radius: 12px;
  font-weight: 900;
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
  border-color: #cbd5e1;
}
.btn-ghost {
  border-color: #e5e7eb;
}
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 720px) {
  .app {
    grid-template-columns: 1fr;
  }
  .overlay {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    z-index: 900;
  }
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 260px;
    transform: translateX(-100%);
    transition: transform 0.25s ease;
    z-index: 1000;
    background: #fff;
  }
  .sidebar.open {
    transform: translateX(0);
  }
  .hamburger {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    background: transparent;
    border: none;
    cursor: pointer;
  }
  .content {
    padding: 18px 14px 30px;
  }
}
</style>















