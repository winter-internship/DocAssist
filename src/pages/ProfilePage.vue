<template>
    <div class="app">
      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="sb-top">
          <div class="sb-logo">AI</div>
        </div>
  
        <nav class="sb-nav">
          <button class="sb-item" title="대시보드" @click="go('home')">🏠</button>
          <button class="sb-item" title="업로드" @click="go('upload')">⬆️</button>
          <button class="sb-item" title="내 드라이브" @click="go('drive')">🗂️</button>
          <button class="sb-item" title="문서 보기(최근 열기)" @click="openLastDoc">📄</button>
          <button class="sb-item" title="Q&A" @click="go('qa')">💬</button>
          <button class="sb-item" title="용어집" @click="go('terms')">📚</button>
          <button class="sb-item active" title="프로필/설정">👤</button>
        </nav>
  
        <div class="sb-bottom">
          <button class="sb-item" title="도움말(준비중)" disabled>❓</button>
          <button class="sb-item" title="설정(준비중)" disabled>⚙️</button>
        </div>
      </aside>
  
      <!-- Main -->
      <div class="main">
        <!-- Topbar -->
        <header class="topbar">
          <div class="tb-left">
            <div class="tb-title">
              <span class="tb-title-strong">프로필/설정</span>
              <span class="tb-sub">· 결과 표시 방식과 계정 정보를 관리하세요</span>
            </div>
  
            <div class="tb-meta">
              <span class="pill">계정: {{ profile.email }}</span>
              <span class="muted">·</span>
              <span class="muted">플랜: {{ profile.plan }}</span>
            </div>
          </div>
  
          <div class="tb-right">
            <button class="btn btn-outline" type="button" @click="restoreDefaults">기본값 복원</button>
            <button class="btn btn-primary" type="button" @click="saveMock">저장</button>
          </div>
        </header>
  
        <main class="content">
          <!-- Profile card -->
          <section class="card">
            <div class="card-head">
              <h2>내 정보</h2>
              <div class="head-actions">
                <span class="muted small">(데모) 실제로는 FastAPI에서 사용자 정보 로드</span>
              </div>
            </div>
  
            <div class="profile">
              <div class="avatar">{{ initials }}</div>
  
              <div class="pinfo">
                <div class="name-row">
                  <div class="name">{{ profile.name }}</div>
                  <span class="badge">Active</span>
                </div>
                <div class="muted">{{ profile.email }}</div>
                <div class="muted small">마지막 로그인: {{ profile.lastLogin }}</div>
              </div>
  
              <div class="pactions">
                <button class="btn btn-outline" type="button" @click="changePasswordMock">비밀번호 변경</button>
                <button class="btn" type="button" @click="logoutMock">로그아웃</button>
              </div>
            </div>
          </section>
  
          <!-- Settings grid -->
          <section class="grid">
            <!-- Explanation settings -->
            <article class="card">
              <div class="card-head">
                <h2>이해 보조 설정</h2>
              </div>
  
              <div class="form">
                <label class="field">
                  <span class="label">쉬운말 변환 강도</span>
                  <select class="select" v-model="settings.simplifyLevel">
                    <option value="low">낮음(원문 최대 보존)</option>
                    <option value="mid">중간(권장)</option>
                    <option value="high">높음(최대한 쉽게)</option>
                  </select>
                </label>
  
                <label class="field">
                  <span class="label">용어 설명 깊이</span>
                  <select class="select" v-model="settings.glossaryDepth">
                    <option value="short">짧게(정의만)</option>
                    <option value="mid">보통(정의+예시)</option>
                    <option value="deep">자세히(정의+예시+주의사항)</option>
                  </select>
                </label>
  
                <label class="field">
                  <span class="label">근거 표시 방식</span>
                  <select class="select" v-model="settings.citationMode">
                    <option value="top">답변 아래 근거 칩</option>
                    <option value="inline">문장별 요약 근거</option>
                  </select>
                </label>
  
                <label class="check">
                  <input type="checkbox" v-model="settings.highlightEvidence" />
                  <span>근거 문단 하이라이트</span>
                </label>
  
                <label class="check">
                  <input type="checkbox" v-model="settings.autoPickEvidence" />
                  <span>답변 생성 시 1번 근거 자동 선택</span>
                </label>
              </div>
            </article>
  
            <!-- Display settings -->
            <article class="card">
              <div class="card-head">
                <h2>화면 표시</h2>
              </div>
  
              <div class="form">
                <label class="field">
                  <span class="label">테마</span>
                  <select class="select" v-model="settings.theme">
                    <option value="light">라이트</option>
                    <option value="dark">다크(데모)</option>
                  </select>
                </label>
  
                <label class="field">
                  <span class="label">글자 크기</span>
                  <select class="select" v-model="settings.fontScale">
                    <option value="sm">작게</option>
                    <option value="md">보통</option>
                    <option value="lg">크게</option>
                  </select>
                </label>
  
                <label class="field">
                  <span class="label">문장 단위 표시</span>
                  <select class="select" v-model="settings.splitMode">
                    <option value="paragraph">문단 기준</option>
                    <option value="sentence">문장 기준</option>
                  </select>
                </label>
  
                <div class="preview">
                  <div class="preview-title">미리보기</div>
                  <div class="preview-box" :data-scale="settings.fontScale">
                    <div class="pv-h">원문</div>
                    <div class="pv-p">
                      본 문서는 내부 규정에 따라 처리되며, 접근 권한은 최소 범위로 부여됩니다.
                    </div>
                    <div class="pv-h">쉬운말</div>
                    <div class="pv-p">
                      이 문서는 회사 규칙에 따라 처리돼요. 시스템 접근 권한은 꼭 필요한 사람에게만 줍니다.
                    </div>
                  </div>
                </div>
              </div>
            </article>
          </section>
  
          <!-- Danger zone -->
          <section class="card danger">
            <div class="card-head">
              <h2>계정 관리</h2>
            </div>
  
            <div class="danger-body">
              <div class="danger-item">
                <div>
                  <div class="danger-title">내 데이터 초기화(데모)</div>
                  <div class="muted small">업로드 문서, Q&A 기록, 설정 등을 초기화합니다.</div>
                </div>
                <button class="btn btn-outline" type="button" @click="resetDataMock">초기화</button>
              </div>
  
              <div class="danger-item">
                <div>
                  <div class="danger-title">계정 삭제(데모)</div>
                  <div class="muted small">실제 서비스에서는 본인 확인 후 진행합니다.</div>
                </div>
                <button class="btn btn-danger" type="button" @click="deleteAccountMock">삭제</button>
              </div>
            </div>
          </section>
  
          <div v-if="toast" class="toast">{{ toast }}</div>
        </main>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed, ref } from "vue";
  import { useRouter } from "vue-router";
  
  const router = useRouter();
  
  const profile = ref({
    name: "혜진",
    email: "abcd63980041@gmail.com",
    plan: "Free (Demo)",
    lastLogin: new Date().toLocaleString("ko-KR", { hour: "2-digit", minute: "2-digit" }),
  });
  
  const settings = ref({
    simplifyLevel: "mid" as "low" | "mid" | "high",
    glossaryDepth: "mid" as "short" | "mid" | "deep",
    citationMode: "top" as "top" | "inline",
    highlightEvidence: true,
    autoPickEvidence: true,
  
    theme: "light" as "light" | "dark",
    fontScale: "md" as "sm" | "md" | "lg",
    splitMode: "paragraph" as "paragraph" | "sentence",
  });
  
  const defaults = JSON.parse(JSON.stringify(settings.value)) as typeof settings.value;
  
  const toast = ref("");
  let timer: number | undefined;
  
  function showToast(msg: string) {
    toast.value = msg;
    if (timer) window.clearTimeout(timer);
    timer = window.setTimeout(() => (toast.value = ""), 1600);
  }
  
  const initials = computed(() => {
    const n = profile.value.name?.trim() || "U";
    return n.slice(0, 1).toUpperCase();
  });
  
  function go(name: string) {
    router.push({ name }).catch(() => {});
  }
  
  function openLastDoc() {
    router.push({ name: "documentView", params: { id: "doc_001" } }).catch(() => {});
  }
  
  function restoreDefaults() {
    settings.value = JSON.parse(JSON.stringify(defaults));
    showToast("기본값으로 복원했어요");
  }
  
  function saveMock() {
    showToast("저장 완료(데모)");
  }
  
  function changePasswordMock() {
    alert("비밀번호 변경(데모): 나중에 /forgot-password 또는 별도 페이지로 연결 예정");
  }
  
  function logoutMock() {
    alert("로그아웃(데모): 토큰 삭제 후 /login 이동 연결 예정");
    router.push({ name: "login" }).catch(() => {});
  }
  
  function resetDataMock() {
    const ok = confirm("정말 초기화할까요? (데모)");
    if (!ok) return;
    showToast("데이터 초기화(데모)");
  }
  
  function deleteAccountMock() {
    const ok = confirm("정말 계정을 삭제할까요? (데모)");
    if (!ok) return;
    showToast("계정 삭제 요청(데모)");
  }
  </script>
  
  <style scoped>
  .app {
    min-height: 100vh;
    background: #f4f6fb;
    color: #111827;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR", Arial;
    display: grid;
    grid-template-columns: 72px 1fr;
  }
  
  /* Sidebar */
  .sidebar {
    background: #2f3642;
    color: #fff;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 12px 0;
    gap: 10px;
  }
  .sb-top { padding: 6px 0 10px; }
  .sb-logo {
    width: 44px; height: 44px;
    border-radius: 14px;
    display: grid; place-items: center;
    background: rgba(255,255,255,0.14);
    font-weight: 900;
  }
  .sb-nav, .sb-bottom {
    display: grid;
    gap: 8px;
    width: 100%;
    justify-items: center;
  }
  .sb-bottom { margin-top: auto; padding-bottom: 6px; }
  .sb-item {
    width: 44px; height: 44px;
    border-radius: 14px;
    border: none;
    background: transparent;
    color: #fff;
    cursor: pointer;
    display: grid;
    place-items: center;
    font-size: 18px;
    opacity: 0.9;
  }
  .sb-item:hover { background: rgba(255,255,255,0.12); }
  .sb-item:disabled { opacity: 0.4; cursor: not-allowed; }
  .sb-item.active {
    background: rgba(255,255,255,0.18);
    outline: 1px solid rgba(255,255,255,0.16);
  }
  
  /* Main */
  .main { display: grid; grid-template-rows: 76px 1fr; }
  
  /* Topbar */
  .topbar {
    background: #fff;
    border-bottom: 1px solid #e5e7eb;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 18px;
    gap: 12px;
  }
  .tb-left { display: grid; gap: 6px; }
  .tb-title { display: flex; align-items: baseline; gap: 8px; }
  .tb-title-strong { font-weight: 900; font-size: 16px; }
  .tb-sub { color: #6b7280; font-size: 12px; }
  .tb-meta { display: flex; align-items: center; gap: 8px; }
  .pill {
    font-size: 12px;
    padding: 2px 10px;
    border-radius: 999px;
    border: 1px solid #e5e7eb;
    background: #f9fafb;
    font-weight: 800;
  }
  .muted { color: #6b7280; font-size: 12px; }
  .small { font-size: 12px; }
  .tb-right { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
  
  .content {
    max-width: 1220px;
    margin: 0 auto;
    padding: 16px 18px 44px;
    display: grid;
    gap: 14px;
  }
  
  /* Cards */
  .card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 16px;
  }
  .card-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 10px;
  }
  .card-head h2 { margin: 0; font-size: 16px; font-weight: 900; }
  .head-actions { display: flex; gap: 10px; align-items: center; }
  
  .profile {
    display: grid;
    grid-template-columns: 72px 1fr auto;
    gap: 14px;
    align-items: center;
  }
  .avatar {
    width: 72px;
    height: 72px;
    border-radius: 22px;
    display: grid;
    place-items: center;
    font-weight: 1000;
    font-size: 22px;
    background: #111827;
    color: #fff;
  }
  .name-row {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .name { font-weight: 1000; font-size: 18px; }
  .badge {
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 999px;
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #065f46;
    font-weight: 900;
  }
  .pactions { display: flex; gap: 10px; flex-wrap: wrap; }
  
  /* Grid settings */
  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    align-items: start;
  }
  .form { display: grid; gap: 12px; }
  .field { display: grid; gap: 6px; }
  .label { font-weight: 900; font-size: 12px; color: #374151; }
  .select {
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 10px 12px;
    background: #fff;
    font-weight: 800;
  }
  .check {
    display: flex;
    gap: 8px;
    align-items: center;
    font-size: 12px;
    font-weight: 800;
    color: #374151;
  }
  
  /* Preview */
  .preview { margin-top: 6px; }
  .preview-title { font-weight: 1000; margin-bottom: 8px; }
  .preview-box {
    border: 1px solid #eef2f7;
    border-radius: 14px;
    padding: 12px;
    background: #fbfcff;
  }
  .preview-box[data-scale="sm"] { font-size: 12px; }
  .preview-box[data-scale="md"] { font-size: 14px; }
  .preview-box[data-scale="lg"] { font-size: 16px; }
  .pv-h { font-weight: 1000; margin: 6px 0; }
  .pv-p { color: #374151; font-weight: 700; line-height: 1.6; }
  
  /* Danger */
  .danger { border-color: #fee2e2; }
  .danger-body { display: grid; gap: 10px; }
  .danger-item {
    border: 1px solid #fee2e2;
    border-radius: 14px;
    padding: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    background: #fff;
  }
  .danger-title { font-weight: 1000; color: #991b1b; }
  
  /* Buttons */
  .btn {
    border: 1px solid #e5e7eb;
    background: #fff;
    padding: 10px 12px;
    border-radius: 12px;
    font-weight: 900;
    cursor: pointer;
  }
  .btn:hover { background: #f9fafb; }
  .btn-primary { background: #2563eb; border-color: #2563eb; color: #fff; }
  .btn-primary:hover { background: #1d4ed8; }
  .btn-outline { border-color: #cbd5e1; }
  .btn-danger { background: #ef4444; border-color: #ef4444; color: #fff; }
  .btn-danger:hover { background: #dc2626; }
  
  .toast {
    position: fixed;
    left: 50%;
    bottom: 18px;
    transform: translateX(-50%);
    padding: 10px 12px;
    border-radius: 14px;
    font-weight: 900;
    border: 1px solid #bfdbfe;
    background: #eff6ff;
    color: #1d4ed8;
  }
  
  @media (max-width: 980px) {
    .grid { grid-template-columns: 1fr; }
    .profile { grid-template-columns: 72px 1fr; }
    .pactions { grid-column: 1 / -1; }
  }
  @media (max-width: 720px) {
    .app { grid-template-columns: 62px 1fr; }
  }
  </style>
  