<template>
  <div class="app">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sb-brand">
        <div class="sb-logo"><img src="/logo.png" alt="DocAssist" /></div>
        <div class="sb-name">DocAssist</div>
      </div>

      <div class="sb-search">
        <input class="sb-input" placeholder="Search" v-model="sidebarQ" />
      </div>

      <nav class="sb-nav">
        <button class="sb-item" @click="go('home')"><span class="ico">🏠</span><span class="txt">Home</span></button>
        <button class="sb-item" @click="go('drive')"><span class="ico">🗂️</span><span class="txt">Drive</span></button>
        <button class="sb-item" @click="go('upload')"><span class="ico">⬆️</span><span class="txt">Upload</span></button>
        <button class="sb-item" @click="go('qa')"><span class="ico">💬</span><span class="txt">Q&A</span></button>
        <div class="sb-sep"></div>
        <button class="sb-item active" @click="go('profile')"><span class="ico">👤</span><span class="txt">Profile</span></button>
        <button class="sb-item" @click="go('admin')"><span class="ico">🛡️</span><span class="txt">Admin</span></button>
      </nav>

      <div class="sb-bottom">
        <button class="sb-mini" @click="toggleTheme" :title="theme === 'dark' ? 'Light' : 'Dark'">
          {{ theme === "dark" ? "☀️" : "🌙" }}
        </button>
        <button class="sb-mini" @click="logoutMock" title="Logout">↩️</button>
      </div>
    </aside>

    <!-- Main -->
    <div class="main">
      <header class="top">
        <div class="top-bg"></div>

        <div class="top-inner">
          <div class="top-left">
            <div class="crumb">
              <span class="pill">Settings</span>
              <span class="dot">•</span>
              <span class="muted">Profile</span>
            </div>
            <h1 class="title">프로필 / 설정</h1>
            <p class="sub muted">
              문서 이해 보조 옵션과 화면 표시를 개인화합니다.
            </p>
          </div>

          <div class="top-right">
            <button class="btn btn-ghost" @click="saveMock">저장(데모)</button>
            <button class="btn btn-primary" @click="goResetPassword">비밀번호 변경</button>
          </div>
        </div>
      </header>

      <main class="content">
        <!-- Profile Card -->
        <section class="card profile-card">
          <div class="pc-head">
            <div class="avatar">
              <div class="avatar-ring"></div>
              <div class="avatar-img">HJ</div>
            </div>

            <div class="pc-meta">
              <div class="name">{{ user.name }}</div>
              <div class="email muted">{{ user.email }}</div>
              <div class="meta-line">
                <span class="tag">Last login</span>
                <span class="muted">{{ formatDateTime(user.lastLoginAt) }}</span>
                <span class="sep">·</span>
                <span class="tag">Joined</span>
                <span class="muted">{{ formatDate(user.joinedAt) }}</span>
              </div>
            </div>

            <div class="pc-actions">
              <button class="btn btn-outline" @click="go('drive')">내 드라이브</button>
              <button class="btn btn-outline" @click="go('qa')">Q&A</button>
            </div>
          </div>
        </section>

        <!-- Settings grid -->
        <section class="grid">
          <!-- 이해 보조 설정 -->
          <article class="card">
            <div class="card-head">
              <h2>이해 보조 설정</h2>
              <div class="badge">AI Assist</div>
            </div>

            <div class="form">
              <div class="field">
                <div class="label">쉬운말 변환 강도</div>
                <div class="seg">
                  <button :class="['seg-btn', assist.level==='low' && 'on']" @click="assist.level='low'">약</button>
                  <button :class="['seg-btn', assist.level==='mid' && 'on']" @click="assist.level='mid'">중</button>
                  <button :class="['seg-btn', assist.level==='high' && 'on']" @click="assist.level='high'">강</button>
                </div>
                <div class="help muted">강도를 높일수록 문장 단순화/용어 풀어쓰기가 적극적으로 적용됩니다.</div>
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
          </article>

          <!-- 화면 표시 -->
          <article class="card">
            <div class="card-head">
              <h2>화면 표시</h2>
              <div class="badge">UI</div>
            </div>

            <div class="form">
              <div class="field">
                <div class="label">테마</div>
                <div class="row">
                  <button class="btn btn-outline" @click="setTheme('light')" :disabled="theme==='light'">라이트</button>
                  <button class="btn btn-outline" @click="setTheme('dark')" :disabled="theme==='dark'">다크(딥 네이비)</button>
                </div>
                <div class="help muted">테마는 전 페이지 공통으로 적용됩니다.</div>
              </div>

              <div class="field">
                <div class="label">글자 크기</div>
                <div class="seg">
                  <button :class="['seg-btn', ui.fontSize==='sm' && 'on']" @click="ui.fontSize='sm'">작게</button>
                  <button :class="['seg-btn', ui.fontSize==='md' && 'on']" @click="ui.fontSize='md'">보통</button>
                  <button :class="['seg-btn', ui.fontSize==='lg' && 'on']" @click="ui.fontSize='lg'">크게</button>
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
          </article>

          <!-- 계정 관리 -->
          <article class="card">
            <div class="card-head">
              <h2>계정 관리</h2>
              <div class="badge">Account</div>
            </div>

            <div class="form">
              <div class="field">
                <div class="label">이메일</div>
                <input class="input" :value="user.email" disabled />
              </div>

              <div class="field">
                <div class="label">보안</div>
                <div class="row">
                  <button class="btn btn-primary" @click="goResetPassword">비밀번호 변경</button>
                  <button class="btn btn-outline" @click="go('login')">로그인 화면</button>
                </div>
              </div>

              <div class="field">
                <div class="label">로그아웃</div>
                <button class="btn btn-ghost" @click="logoutMock">로그아웃(데모)</button>
              </div>

              <div class="help muted">
                실제 연동 시: FastAPI auth + JWT/세션 기반으로 설정 저장/불러오기 연결
              </div>
            </div>
          </article>

          <!-- 우측 미니 패널 -->
          <aside class="panel">
            <div class="panel-card">
              <div class="panel-head">
                <div class="panel-title">미리보기</div>
                <div class="panel-dot"></div>
              </div>

              <div class="preview">
                <div class="pv-title">적용될 설정</div>
                <ul class="pv-list">
                  <li>쉬운말 강도: <b>{{ labelLevel(assist.level) }}</b></li>
                  <li>용어 깊이: <b>Lv. {{ assist.termDepth }}</b></li>
                  <li>근거 표시: <b>{{ assist.evidenceMode }}</b></li>
                  <li>테마: <b>{{ theme }}</b></li>
                  <li>글자 크기: <b>{{ ui.fontSize }}</b></li>
                  <li>문장 단위: <b>{{ ui.sentenceMode ? "ON" : "OFF" }}</b></li>
                </ul>
              </div>

              <button class="btn btn-outline full" @click="saveMock">저장(데모)</button>
            </div>
          </aside>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const sidebarQ = ref("");

const theme = ref<"light" | "dark">("light");

const user = reactive({
  name: "Hyejin",
  email: "abcd63980041@gmail.com",
  lastLoginAt: new Date(Date.now() - 1000 * 60 * 60 * 6).toISOString(),
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

function go(name: string) {
  router.push({ name }).catch(() => {});
}

function applyTheme(next: "light" | "dark") {
  theme.value = next;
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("theme", next);
}
function setTheme(next: "light" | "dark") {
  applyTheme(next);
}
function toggleTheme() {
  applyTheme(theme.value === "dark" ? "light" : "dark");
}

onMounted(() => {
  const saved = (localStorage.getItem("theme") as "light" | "dark") || "light";
  applyTheme(saved);
});

function goResetPassword() {
  // 데모: 토큰 없이 이동
  router.push({ name: "resetPassword" }).catch(() => {});
}

function logoutMock() {
  alert("로그아웃(데모): 나중에 토큰 삭제/세션 만료 처리");
}

function saveMock() {
  alert("저장(데모): 이 설정들을 DB에 저장하도록 FastAPI 연결 예정");
}

function labelLevel(v: "low" | "mid" | "high") {
  if (v === "low") return "약";
  if (v === "mid") return "중";
  return "강";
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
/* 전역 토큰은 style.css에 있고, 여기선 레이아웃만 */
.app{
  min-height: 100vh;
  display: grid;
  grid-template-columns: 280px 1fr;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR", Arial;
  color: var(--ink);
  background: var(--bg);
}

/* Sidebar */
.sidebar{
  background: rgba(255,255,255,0.65);
  border-right: 1px solid var(--line);
  backdrop-filter: blur(10px);
  padding: 16px 14px;
  display:flex;
  flex-direction: column;
  gap: 12px;
}
:global(:root[data-theme="dark"]) .sidebar{
  background: rgba(12,23,43,0.72);
}

.sb-brand{ display:flex; align-items:center; gap: 10px; padding: 8px 6px; }
.sb-logo{
  width: 36px; height: 36px; border-radius: 12px;
  background: rgba(255,255,255,0.7);
  border: 1px solid var(--line);
  display:grid; place-items:center;
  overflow:hidden;
}
:global(:root[data-theme="dark"]) .sb-logo{ background: rgba(255,255,255,0.06); }
.sb-logo img{ width: 22px; height: 22px; object-fit: contain; }
.sb-name{ font-weight: 1000; letter-spacing: -0.2px; }

.sb-search{ padding: 0 6px 6px; }
.sb-input{
  width:100%;
  border:1px solid var(--line);
  border-radius: 12px;
  padding: 10px 12px;
  background: rgba(255,255,255,0.7);
  outline:none;
  font-weight: 900;
}
:global(:root[data-theme="dark"]) .sb-input{ background: rgba(255,255,255,0.06); color: var(--ink); }
.sb-input:focus{ box-shadow: 0 0 0 3px rgba(90,167,255,0.18); }

.sb-nav{ display:grid; gap: 6px; padding: 0 6px; }
.sb-item{
  width:100%;
  display:flex;
  align-items:center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 14px;
  border:1px solid transparent;
  background: transparent;
  cursor:pointer;
  color: var(--ink);
  font-weight: 950;
  text-align:left;
}
.sb-item:hover{
  background: rgba(90,167,255,0.10);
  border-color: rgba(90,167,255,0.18);
}
.sb-item.active{
  background: rgba(90,167,255,0.16);
  border-color: rgba(90,167,255,0.26);
}
.ico{ width: 18px; display:grid; place-items:center; }
.txt{ font-size: 13px; }

.sb-sep{ height: 1px; background: var(--line); margin: 6px 0; }

.sb-bottom{
  margin-top:auto;
  display:flex;
  gap: 8px;
  padding: 8px 6px 0;
}
.sb-mini{
  width: 40px; height: 40px;
  border-radius: 14px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,0.7);
  cursor:pointer;
  font-size: 16px;
}
:global(:root[data-theme="dark"]) .sb-mini{ background: rgba(255,255,255,0.06); color: var(--ink); }
.sb-mini:hover{ filter: brightness(0.99); }

/* Main */
.main{ display:flex; flex-direction: column; min-width: 0; }

.top{ position: relative; padding: 22px 24px 18px; }
.top-bg{
  position:absolute; inset: 0;
  background: linear-gradient(135deg,
    rgba(90,167,255,0.60),
    rgba(139,220,255,0.45),
    rgba(125,140,255,0.40)
  );
  border-bottom: 1px solid var(--line);
}
:global(:root[data-theme="dark"]) .top-bg{
  background: linear-gradient(135deg,
    rgba(20,52,96,0.85),
    rgba(10,92,112,0.55),
    rgba(48,36,110,0.55)
  );
}

.top-inner{
  position: relative;
  max-width: 1180px;
  margin: 0 auto;
  display:flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-end;
}
.crumb{ display:flex; align-items:center; gap: 8px; margin-bottom: 8px; }
.pill{
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(255,255,255,0.55);
  border: 1px solid rgba(255,255,255,0.45);
  font-weight: 1000;
}
:global(:root[data-theme="dark"]) .pill{ background: rgba(12,23,43,0.55); border-color: var(--line); }
.dot{ opacity: .7; }
.title{ margin:0; font-size: 28px; font-weight: 1100; letter-spacing: -0.4px; }
.sub{ margin: 8px 0 0; }

.top-right{ display:flex; gap: 10px; align-items:center; flex-wrap: wrap; }

/* Content */
.content{
  max-width: 1180px;
  margin: 0 auto;
  width: 100%;
  padding: 18px 24px 40px;
  display:grid;
  gap: 14px;
}
.profile-card{ padding: 18px; }

.pc-head{
  display:flex;
  align-items:center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}
.avatar{ position: relative; width: 74px; height: 74px; }
.avatar-ring{
  position:absolute; inset: -3px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(90,167,255,1), rgba(139,220,255,1));
  filter: blur(0px);
}
.avatar-img{
  position:absolute; inset: 0;
  border-radius: 50%;
  background: var(--card-solid);
  border: 1px solid var(--line);
  display:grid; place-items:center;
  font-weight: 1100;
  letter-spacing: -0.3px;
}
.name{ font-weight: 1100; font-size: 18px; }
.email{ margin-top: 2px; }
.meta-line{ margin-top: 8px; display:flex; gap: 10px; align-items:center; flex-wrap: wrap; }
.tag{
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 999px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,0.55);
  font-weight: 1000;
}
:global(:root[data-theme="dark"]) .tag{ background: rgba(255,255,255,0.04); }

.sep{ opacity: .6; }
.pc-actions{ display:flex; gap: 10px; flex-wrap: wrap; }

/* Grid for cards + panel */
.grid{
  display:grid;
  grid-template-columns: 1fr 1fr 1fr 360px;
  gap: 14px;
  align-items: start;
}

.card{
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 18px;
  box-shadow: var(--shadow);
  padding: 16px;
  backdrop-filter: blur(10px);
}

.card-head{
  display:flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}
.card-head h2{ margin:0; font-size: 16px; font-weight: 1100; }
.badge{
  font-size: 12px;
  font-weight: 1100;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(90,167,255,0.14);
  border: 1px solid rgba(90,167,255,0.22);
}

.form{ display:grid; gap: 12px; }
.field{ display:grid; gap: 8px; }
.label{ font-size: 12px; font-weight: 1000; color: var(--muted); }

.input{
  width: 100%;
  padding: 12px 12px;
  border-radius: 14px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,0.7);
  outline: none;
  font-weight: 950;
}
:global(:root[data-theme="dark"]) .input{ background: rgba(255,255,255,0.06); color: var(--ink); }

.select{
  width: 100%;
  padding: 12px 12px;
  border-radius: 14px;
  border: 1px solid var(--line);
  background: rgba(255,255,255,0.7);
  outline: none;
  font-weight: 950;
}
:global(:root[data-theme="dark"]) .select{ background: rgba(255,255,255,0.06); color: var(--ink); }

.help{ font-size: 12px; }

.range{ width: 100%; }
.range-row{ display:flex; justify-content: space-between; align-items:center; }

.seg{ display:flex; gap: 8px; flex-wrap: wrap; }
.seg-btn{
  border-radius: 14px;
  padding: 10px 12px;
  font-weight: 1100;
  cursor:pointer;
  border: 1px solid var(--line);
  background: rgba(255,255,255,0.7);
}
:global(:root[data-theme="dark"]) .seg-btn{ background: rgba(255,255,255,0.06); color: var(--ink); }
.seg-btn.on{
  border-color: rgba(90,167,255,0.35);
  background: rgba(90,167,255,0.14);
}

.toggle{
  display:flex;
  align-items:center;
  gap: 10px;
}
.toggle input{ display:none; }
.knob{
  width: 46px; height: 26px;
  border-radius: 999px;
  background: rgba(148,163,184,0.35);
  position: relative;
  border: 1px solid var(--line);
}
.knob::after{
  content:"";
  position:absolute;
  top: 50%;
  transform: translateY(-50%);
  left: 3px;
  width: 20px; height: 20px;
  border-radius: 50%;
  background: var(--card-solid);
  transition: all .18s ease;
}
.toggle input:checked + .knob{
  background: rgba(90,167,255,0.40);
}
.toggle input:checked + .knob::after{
  left: 23px;
}

.row{ display:flex; gap: 10px; flex-wrap: wrap; }

/* Panel */
.panel{ grid-column: 4 / 5; }
.panel-card{
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 14px;
  box-shadow: var(--shadow);
  backdrop-filter: blur(10px);
}
.panel-head{
  display:flex;
  justify-content: space-between;
  align-items:center;
  margin-bottom: 10px;
}
.panel-title{ font-weight: 1100; }
.panel-dot{ width: 10px; height: 10px; border-radius: 50%; background: rgba(90,167,255,0.9); }
.preview{ margin-top: 8px; }
.pv-title{ font-weight: 1100; margin-bottom: 8px; }
.pv-list{ margin: 0; padding-left: 18px; display:grid; gap: 8px; color: var(--muted); font-weight: 850; }
.full{ width: 100%; margin-top: 12px; }
.mono{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; font-weight: 1100; }

/* Buttons */
.btn{
  border-radius: 14px;
  padding: 10px 12px;
  font-weight: 1100;
  cursor: pointer;
  border: 1px solid transparent;
  background: rgba(255,255,255,0.75);
}
:global(:root[data-theme="dark"]) .btn{ background: rgba(255,255,255,0.06); color: var(--ink); border-color: var(--line); }
.btn-primary{
  background: linear-gradient(90deg, rgba(90,167,255,1), rgba(139,220,255,1));
  color: #071221;
  border-color: rgba(90,167,255,0.35);
}
.btn-outline{ border-color: var(--line); }
.btn-ghost{ background: transparent; border-color: var(--line); }

@media (max-width: 1180px){
  .grid{ grid-template-columns: 1fr 1fr; }
  .panel{ grid-column: auto; }
}
@media (max-width: 1040px){
  .app{ grid-template-columns: 240px 1fr; }
}
@media (max-width: 820px){
  .app{ grid-template-columns: 1fr; }
  .sidebar{ display:none; }
}
</style>
