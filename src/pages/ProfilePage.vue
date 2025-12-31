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

        <button class="sb-item" @click="go('upload')">
          <span class="ico">📤</span><span class="txt">업로드</span>
        </button>

        <button class="sb-item" @click="go('qa')">
          <span class="ico">💬</span><span class="txt">Q&A</span>
        </button>
        <button class="sb-item" @click="go('terms')">
          <span class="ico">📚</span><span class="txt">용어집</span>
        </button>
        <div class="sb-sep"></div>

        <button class="sb-item active">
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
      <header class="topbar">
        <div class="tb-left">
          <div class="tb-title">
            <button class="hamburger" @click="sidebarOpen = true" aria-label="Open menu">☰</button>
            <span class="tb-title-strong">프로필/설정</span>
            <span class="tb-sub">· 계정 정보와 환경 설정</span>
          </div>
        </div>
        <div class="tb-right">
          <button class="btn btn-save" @click="save">저장</button>
        </div>
      </header>

      <main class="content">
        <!-- Profile Card -->
        <section class="card profile-card">
          <div class="pc-left">
            <div class="avatar">
              <div class="avatar-ring"></div>
              <div class="avatar-img">{{ initials(user.name) }}</div>
            </div>

            <div class="pc-meta">
              <div class="email muted">{{ user.email }}</div>

              <div class="meta-line">
                <span class="tag">Last login</span>
                <span class="muted">{{ formatDateTime(user.lastLoginAt) }}</span>
                <span class="sep">·</span>
                <span class="tag">Joined</span>
                <span class="muted">{{ formatDate(user.joinedAt) }}</span>
              </div>
            </div>
          </div>
        </section>

        <!-- ✅ 3 Cards Grid -->
        <section class="grid">
          <!-- 이해 보조 설정 -->
          <article class="card card-eq">
            <div class="card-head">
              <h2>이해 보조 설정</h2>
              <div class="badge">AI Assist</div>
            </div>

            <div class="form form-eq">
              <div class="field">
                <div class="label">쉬운말 변환 강도</div>
                <div class="seg">
                  <button
                    :class="['seg-btn', assist.level === 'low' && 'on']"
                    @click="assist.level = 'low'"
                  >
                    약
                  </button>
                  <button
                    :class="['seg-btn', assist.level === 'mid' && 'on']"
                    @click="assist.level = 'mid'"
                  >
                    중
                  </button>
                  <button
                    :class="['seg-btn', assist.level === 'high' && 'on']"
                    @click="assist.level = 'high'"
                  >
                    강
                  </button>
                </div>
                <div class="help muted">
                  강도를 높일수록 단순화/용어 풀어쓰기가 적극 적용됩니다.
                </div>
              </div>

              <div class="field">
                <div class="label">용어 설명 깊이</div>
                <input class="range" type="range" min="1" max="5" v-model="assist.termDepth" />
                <div class="range-row">
                  <span class="muted">간단</span>
                  <span class="mono">Lv. {{ assist.termDepth }}</span>
                  <span class="muted">자세히</span>
                </div>
              </div>

              <div class="field">
                <div class="label">근거 표시 방식</div>
                <select class="select" v-model="assist.evidenceMode">
                  <option value="inline">문장 옆(Inline)</option>
                  <option value="panel">오른쪽 패널(Panel)</option>
                  <option value="hover">하이라이트 + 호버(Hover)</option>
                </select>
              </div>
            </div>

            <div class="card-foot">
              <span class="foot-muted muted">AI 동작 옵션을 설정합니다.</span>
            </div>
          </article>

          <!-- 화면 표시 -->
          <article class="card card-eq">
            <div class="card-head">
              <h2>화면 표시</h2>
              <div class="badge">UI</div>
            </div>

            <div class="form form-eq">
              <div class="field">
                <div class="label">테마</div>
                <div class="row">
                  <button
                    class="btn btn-outline theme-btn"
                    :class="{ on: theme === 'light' }"
                    @click="setTheme('light')"
                  >
                    라이트
                  </button>
                  <button
                    class="btn btn-outline theme-btn"
                    :class="{ on: theme === 'dark' }"
                    @click="setTheme('dark')"
                  >
                    다크
                  </button>
                </div>
                <div class="help muted">전 페이지 공통으로 적용됩니다.</div>
              </div>

              <div class="field">
                <div class="label">글자 크기</div>
                <div class="seg">
                  <button
                    :class="['seg-btn', ui.fontSize === 'sm' && 'on']"
                    @click="ui.fontSize = 'sm'"
                  >
                    작게
                  </button>
                  <button
                    :class="['seg-btn', ui.fontSize === 'md' && 'on']"
                    @click="ui.fontSize = 'md'"
                  >
                    보통
                  </button>
                  <button
                    :class="['seg-btn', ui.fontSize === 'lg' && 'on']"
                    @click="ui.fontSize = 'lg'"
                  >
                    크게
                  </button>
                </div>
              </div>

              <div class="field">
                <div class="label">문장 단위 표시</div>
                <label class="toggle">
                  <input type="checkbox" v-model="ui.sentenceMode" />
                  <span class="knob"></span>
                  <span class="toggle-text muted">문장별 구분선/번호 표시</span>
                </label>
              </div>
            </div>

            <div class="card-foot">
              <span class="foot-muted muted">가독성과 표시 스타일을 설정합니다.</span>
            </div>
          </article>

          <!-- 계정 관리 -->
          <article class="card card-eq">
            <div class="card-head">
              <h2>계정 관리</h2>
              <div class="right-badges">
                <span class="badge">Account</span>
                <span v-if="isAdmin" class="admin-badge">🛡️ Admin</span>
              </div>
            </div>

            <div class="form form-eq">
              <div class="field">
                <div class="label">이메일</div>
                <input class="input" :value="user.email" disabled />
              </div>

              <div class="field">
                <div class="label">보안</div>
                <button class="btn btn-primary full" @click="goResetPassword">비밀번호 변경</button>
              </div>

              <div class="field">
                <div class="label">세션</div>
                <button class="btn btn-ghost full" @click="logout">로그아웃</button>
              </div>
            </div>

            <div class="card-foot">
              <span class="foot-muted muted">계정과 보안 설정을 관리합니다.</span>
            </div>
          </article>
        </section>
      </main>
    </div>

    <!-- ✅ Toast -->
    <div class="toast" :class="{ show: toast.show }">
      설정이 저장되었습니다
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const sidebarQ = ref("");
const sidebarOpen = ref(false);

const theme = ref<"light" | "dark">("light");

const role = ref<"ADMIN" | "USER" | "">("");
const isAdmin = computed(() => role.value === "ADMIN");

const user = reactive({
  name: "User",
  email: "",
  lastLoginAt: new Date().toISOString(),
  joinedAt: new Date(Date.now() - 1000 * 60 * 60 * 24 * 18).toISOString(),
});

const assist = reactive({
  level: "mid" as "low" | "mid" | "high",
  termDepth: 3,
  evidenceMode: "panel" as "inline" | "panel" | "hover",
});

const ui = reactive({
  fontSize: "md" as "sm" | "md" | "lg",
  sentenceMode: true,
});

const toast = reactive({
  show: false,
  timer: 0 as unknown as number,
});

function go(name: string) {
  sidebarOpen.value = false;
  router.push({ name }).catch(() => {});
}

function applyTheme(next: "light" | "dark") {
  theme.value = next;
  document.documentElement.setAttribute("data-theme", next);
  document.body.setAttribute("data-theme", next);
  localStorage.setItem("theme", next);
}
function setTheme(next: "light" | "dark") {
  applyTheme(next);
}
function toggleTheme() {
  applyTheme(theme.value === "dark" ? "light" : "dark");
}

onMounted(() => {
  const savedTheme = (localStorage.getItem("theme") as "light" | "dark") || "light";
  applyTheme(savedTheme);

  role.value = (localStorage.getItem("role") as "ADMIN" | "USER") || "";
  user.name = localStorage.getItem("user_name") || "User";
  user.email = localStorage.getItem("user_email") || "";

  const last = localStorage.getItem("last_login_at");
  user.lastLoginAt = last || new Date().toISOString();

  // ✅ 저장해둔 설정 복원
  const saved = localStorage.getItem("profile_settings");
  if (saved) {
    try {
      const obj = JSON.parse(saved);
      if (obj?.assist) Object.assign(assist, obj.assist);
      if (obj?.ui) Object.assign(ui, obj.ui);
    } catch {}
  }
});

function goResetPassword() {
  router.push({ name: "resetPassword" }).catch(() => {});
}

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

function save() {
  const payload = { assist: { ...assist }, ui: { ...ui } };
  localStorage.setItem("profile_settings", JSON.stringify(payload));

  toast.show = false;
  if (toast.timer) window.clearTimeout(toast.timer);

  // 다음 tick 느낌으로 다시 show (애니메이션 재생 보장)
  requestAnimationFrame(() => {
    toast.show = true;
    toast.timer = window.setTimeout(() => {
      toast.show = false;
    }, 1800);
  });
}

function initials(name: string) {
  const s = (name || "").trim();
  if (!s) return "U";
  const parts = s.split(/\s+/);
  const a = parts[0]?.[0] ?? "U";
  const b = parts.length > 1 ? parts[1]?.[0] ?? "" : "";
  return (a + b).toUpperCase();
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
</script>

<style scoped>
:global(:root) {
  --b1: #1d4ed8;
  --b2: #0ea5e9;
  --ring: rgba(29, 78, 216, 0.18);
}

/* Layout */
.app {
  --ink: #111827;
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
  border-right: 1px solid var(--line);
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
  border: 1px solid var(--line);
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
  color: var(--ink);
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
  background: var(--line);
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
  border: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  font-size: 16px;
}

/* Main */
.main {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* Header */
.topbar {
  background: #fff;
  border-bottom: 1px solid var(--line);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 18px;
  min-height: 76px;
  gap: 12px;
}
.tb-left {
  display: grid;
  gap: 6px;
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
  color: var(--muted);
  font-size: 12px;
  font-weight: 700;
}
.tb-right {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}
.muted {
  color: var(--muted);
  font-size: 12px;
}
.small {
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

/* Cards */
.card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 18px;
  box-shadow: var(--shadow);
  padding: 16px;
  backdrop-filter: blur(10px);
}
.profile-card {
  padding: 18px;
}

.pc-left {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}

.avatar {
  position: relative;
  width: 74px;
  height: 74px;
  flex: 0 0 auto;
}
.avatar-ring {
  position: absolute;
  inset: -3px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--b1), var(--b2));
}
.avatar-img {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: var(--card-solid);
  border: 1px solid var(--line);
  display: grid;
  place-items: center;
  font-weight: 1100;
  letter-spacing: -0.3px;
}

.pc-meta {
  min-width: 0;
}
.name-row {
  display: flex;
  align-items: center;
  gap: 10px;
}
.name {
  font-weight: 1100;
  font-size: 18px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 520px;
}
.email {
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 520px;
}
.meta-line {
  margin-top: 8px;
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}
.tag {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.55);
  font-weight: 1000;
}
.sep {
  opacity: 0.6;
}

.admin-pill {
  font-size: 12px;
  font-weight: 1100;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(17, 24, 39, 0.1);
  border: 1px solid rgba(17, 24, 39, 0.15);
}
/* Grid equal */
.grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  align-items: stretch;
}
.card-eq {
  display: flex;
  flex-direction: column;
  min-height: 280px;
}
.form-eq {
  display: grid;
  gap: 12px;
  flex: 1 1 auto;
}
.card-foot {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--line);
}
.foot-muted {
  font-size: 12px;
  font-weight: 850;
}

/* Card head */
.card-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}
.card-head h2 {
  margin: 0;
  font-size: 16px;
  font-weight: 1100;
}
.badge {
  font-size: 12px;
  font-weight: 1100;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(29, 78, 216, 0.1);
  border: 1px solid rgba(29, 78, 216, 0.18);
}
.right-badges {
  display: flex;
  gap: 8px;
  align-items: center;
}
.admin-badge {
  font-size: 12px;
  font-weight: 1100;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(17, 24, 39, 0.1);
  border: 1px solid rgba(17, 24, 39, 0.15);
}
/* Fields */
.field {
  display: grid;
  gap: 8px;
}
.label {
  font-size: 12px;
  font-weight: 1000;
  color: var(--muted);
}

.input,
.select {
  width: 100%;
  padding: 12px 12px;
  border-radius: 14px;
  border: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.7);
  outline: none;
  font-weight: 950;
}
.help {
  font-size: 12px;
}
.range {
  width: 100%;
}
.range-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.seg {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.seg-btn {
  border-radius: 14px;
  padding: 10px 12px;
  font-weight: 1100;
  cursor: pointer;
  border: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.7);
}
.seg-btn.on {
  border-color: rgba(29, 78, 216, 0.3);
  background: rgba(29, 78, 216, 0.1);
}

.toggle {
  display: flex;
  align-items: center;
  gap: 10px;
}
.toggle input {
  display: none;
}
.knob {
  width: 46px;
  height: 26px;
  border-radius: 999px;
  background: rgba(148, 163, 184, 0.35);
  position: relative;
  border: 1px solid var(--line);
}
.knob::after {
  content: "";
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  left: 3px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--card-solid);
  transition: all 0.18s ease;
}
.toggle input:checked + .knob {
  background: rgba(29, 78, 216, 0.32);
}
.toggle input:checked + .knob::after {
  left: 23px;
}

.row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.full {
  width: 100%;
}

.mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono",
    "Courier New", monospace;
  font-weight: 1100;
}

/* Buttons */
.btn {
  border-radius: 14px;
  padding: 10px 12px;
  font-weight: 1100;
  cursor: pointer;
  border: 1px solid transparent;
  background: rgba(255, 255, 255, 0.75);
}
.btn-save {
  background: linear-gradient(90deg, #2563eb, #1d4ed8);
  color: #fff;
  border-color: rgba(37, 99, 235, 0.35);
}
.btn-primary {
  background: linear-gradient(90deg, var(--b1), var(--b2));
  color: #071221;
  border-color: rgba(29, 78, 216, 0.28);
}
.btn-outline {
  border-color: var(--line);
}
.theme-btn.on {
  background: #2563eb;
  border-color: #2563eb;
  color: #fff;
}
.theme-btn.on:hover {
  background: #1d4ed8;
}
.btn-ghost {
  background: transparent;
  border-color: var(--line);
}

/* ✅ Toast */
.toast {
  position: fixed;
  right: 24px;
  bottom: 24px;
  padding: 12px 14px;
  border-radius: 14px;
  background: rgba(17, 24, 39, 0.92);
  color: #fff;
  font-weight: 950;
  font-size: 13px;
  transform: translateY(10px);
  opacity: 0;
  pointer-events: none;
  transition: all 0.18s ease;
}
.toast.show {
  transform: translateY(0);
  opacity: 1;
}

/* Responsive */
@media (max-width: 1180px) {
  .grid {
    grid-template-columns: 1fr 1fr;
  }
}
@media (max-width: 1040px) {
  .app {
    grid-template-columns: 240px 1fr;
  }
}
@media (max-width: 820px) {
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
  .grid {
    grid-template-columns: 1fr;
  }
  .card-eq {
    min-height: auto;
  }
}
</style>


















