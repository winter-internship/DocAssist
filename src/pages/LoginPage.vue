<template>
    <div class="auth">
      <header class="topbar">
        <div class="brand" @click="goHome" role="button" tabindex="0">
          <div class="logo">AI</div>
          <div class="brand-text">
            <div class="title">DocAssist</div>
            <div class="sub">AI 문서 이해 보조</div>
          </div>
        </div>
  
        <button class="btn btn-ghost" type="button" @click="goHome">대시보드</button>
      </header>
  
      <main class="container">
        <section class="card">
          <div class="card-head">
            <h1>로그인</h1>
            <p class="muted">문서 업로드/드라이브/Q&A 기능을 사용하려면 로그인하세요.</p>
          </div>
  
          <form class="form" @submit.prevent="onSubmit">
            <label class="field">
              <span class="label">이메일</span>
              <input
                v-model.trim="email"
                class="input"
                type="email"
                placeholder="name@example.com"
                autocomplete="email"
                required
              />
            </label>
  
            <label class="field">
              <span class="label">비밀번호</span>
              <div class="pw">
                <input
                  v-model="password"
                  class="input"
                  :type="showPw ? 'text' : 'password'"
                  placeholder="비밀번호"
                  autocomplete="current-password"
                  required
                />
                <button class="pw-toggle" type="button" @click="showPw = !showPw">
                  {{ showPw ? "숨김" : "보기" }}
                </button>
              </div>
            </label>
  
            <div class="row">
              <label class="check">
                <input type="checkbox" v-model="remember" />
                <span>로그인 상태 유지</span>
              </label>
  
              <button class="link" type="button" @click="goForgot">비밀번호 찾기</button>
            </div>
  
            <button class="btn btn-primary" type="submit" :disabled="loading">
              {{ loading ? "로그인 중..." : "로그인" }}
            </button>
  
            <div class="divider"><span>또는</span></div>
  
            <button class="btn btn-outline" type="button" @click="demoLogin">
              데모 계정으로 로그인
            </button>
          </form>
  
          <div class="footer">
            <span class="muted">계정이 없나요?</span>
            <button class="link" type="button" @click="goSignup">회원가입</button>
          </div>
  
          <div v-if="toast" class="toast" :class="toastType">
            {{ toast }}
          </div>
        </section>
  
        <aside class="side">
          <div class="side-card">
            <div class="side-title">DocAssist에서 할 수 있는 것</div>
            <ul class="side-list">
              <li>PDF/이미지 업로드 후 텍스트 추출</li>
              <li>전문용어 용어집/정의 자동 생성</li>
              <li>원문 vs 쉬운 말 변환 비교</li>
              <li>문서 근거 기반 Q&A</li>
            </ul>
            <div class="side-hint muted">
              (현재는 프론트 목업 단계 / FastAPI 연동 예정)
            </div>
          </div>
        </aside>
      </main>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  
  const router = useRouter();
  
  const email = ref("");
  const password = ref("");
  const remember = ref(true);
  const showPw = ref(false);
  const loading = ref(false);
  
  const toast = ref<string>("");
  const toastType = ref<"ok" | "bad">("ok");
  let toastTimer: number | undefined;
  
  function showToast(msg: string, type: "ok" | "bad" = "ok") {
    toast.value = msg;
    toastType.value = type;
    if (toastTimer) window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => (toast.value = ""), 2500);
  }
  
  function goHome() {
    router.push({ name: "home" }).catch(() => {});
  }
  function goSignup() {
    router.push({ name: "signup" }).catch(() => {});
  }
  function goForgot() {
    router.push({ name: "forgot" }).catch(() => {});
  }
  
  async function onSubmit() {
    loading.value = true;
  
    // TODO: FastAPI 연동
    // POST /auth/login { email, password }
    await new Promise((r) => setTimeout(r, 600));
  
    if (!email.value || !password.value) {
      showToast("이메일/비밀번호를 입력하세요.", "bad");
      loading.value = false;
      return;
    }
  
    // 데모: 아무 값이나 로그인 성공 처리
    showToast("로그인 성공! (데모)", "ok");
    loading.value = false;
  
    // 로그인 후 드라이브로 이동
    router.push({ name: "drive" }).catch(() => {});
  }
  
  function demoLogin() {
    email.value = "demo@docassist.ai";
    password.value = "demo1234";
    showToast("데모 계정 입력 완료", "ok");
  }
  </script>
  
  <style scoped>
  .auth {
    min-height: 100vh;
    background: #f4f6fb;
    color: #111827;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR", Arial;
  }
  
  .topbar {
    height: 72px;
    background: #fff;
    border-bottom: 1px solid #e5e7eb;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 18px;
  }
  
  .brand {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    user-select: none;
  }
  .logo {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: grid;
    place-items: center;
    background: #111827;
    color: #fff;
    font-weight: 900;
  }
  .brand-text .title {
    font-weight: 900;
    font-size: 14px;
  }
  .brand-text .sub {
    color: #6b7280;
    font-size: 12px;
    margin-top: 2px;
  }
  
  .container {
    max-width: 1060px;
    margin: 0 auto;
    padding: 18px;
    display: grid;
    grid-template-columns: 1.1fr 0.9fr;
    gap: 14px;
    align-items: start;
  }
  
  .card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 18px;
    position: relative;
  }
  
  .card-head h1 {
    margin: 0;
    font-size: 20px;
    font-weight: 900;
  }
  .muted {
    color: #6b7280;
    font-size: 12px;
  }
  .card-head p {
    margin: 8px 0 0;
    line-height: 1.6;
  }
  
  .form {
    margin-top: 14px;
    display: grid;
    gap: 12px;
  }
  
  .field {
    display: grid;
    gap: 6px;
  }
  .label {
    font-weight: 900;
    font-size: 12px;
  }
  
  .input {
    width: 100%;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 10px 12px;
    outline: none;
    background: #fff;
  }
  .input:focus {
    border-color: #93c5fd;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
  }
  
  .pw {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 8px;
    align-items: center;
  }
  .pw-toggle {
    border: 1px solid #e5e7eb;
    background: #fff;
    padding: 10px 12px;
    border-radius: 12px;
    cursor: pointer;
    font-weight: 900;
  }
  .pw-toggle:hover {
    background: #f9fafb;
  }
  
  .row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
  }
  .check {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 800;
    color: #374151;
  }
  
  .divider {
    display: grid;
    place-items: center;
    margin: 6px 0;
    position: relative;
  }
  .divider::before {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    height: 1px;
    background: #eef2f7;
  }
  .divider span {
    background: #fff;
    padding: 0 10px;
    color: #6b7280;
    font-size: 12px;
    position: relative;
    z-index: 1;
  }
  
  .footer {
    margin-top: 12px;
    display: flex;
    gap: 8px;
    align-items: center;
  }
  
  .side {
    display: grid;
    gap: 14px;
  }
  .side-card {
    background: linear-gradient(180deg, #ffffff, #f9fafb);
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 18px;
  }
  .side-title {
    font-weight: 900;
    margin-bottom: 10px;
  }
  .side-list {
    margin: 0;
    padding-left: 18px;
    display: grid;
    gap: 8px;
    color: #374151;
    font-weight: 700;
    font-size: 13px;
  }
  .side-hint {
    margin-top: 12px;
  }
  
  .toast {
    position: absolute;
    left: 18px;
    right: 18px;
    bottom: 14px;
    padding: 10px 12px;
    border-radius: 14px;
    font-weight: 900;
    border: 1px solid transparent;
  }
  .toast.ok {
    background: #ecfdf5;
    border-color: #a7f3d0;
    color: #065f46;
  }
  .toast.bad {
    background: #fef2f2;
    border-color: #fecaca;
    color: #991b1b;
  }
  
  /* Buttons */
  .btn {
    border: 1px solid #e5e7eb;
    background: #fff;
    padding: 10px 12px;
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
    border-color: transparent;
    background: transparent;
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
  
  .btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  @media (max-width: 920px) {
    .container {
      grid-template-columns: 1fr;
    }
  }
  </style>
  