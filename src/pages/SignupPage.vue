<template>
    <div class="auth">
      <header class="topbar">
        <div class="brand" @click="goHome">
          <div class="logo">AI</div>
          <div class="brand-text">
            <div class="title">DocAssist</div>
            <div class="sub">회원가입</div>
          </div>
        </div>
        <button class="btn btn-ghost" type="button" @click="goLogin">로그인</button>
      </header>
  
      <main class="container single">
        <section class="card">
          <div class="card-head">
            <h1>회원가입</h1>
            <p class="muted">기본 정보만 입력하면 바로 시작할 수 있어요.</p>
          </div>
  
          <form class="form" @submit.prevent="onSubmit">
            <label class="field">
              <span class="label">이름</span>
              <input v-model.trim="name" class="input" placeholder="이름" required />
            </label>
  
            <label class="field">
              <span class="label">이메일</span>
              <input v-model.trim="email" class="input" type="email" placeholder="name@example.com" required />
            </label>
  
            <label class="field">
              <span class="label">비밀번호</span>
              <input v-model="pw" class="input" type="password" placeholder="8자 이상" minlength="8" required />
            </label>
  
            <label class="field">
              <span class="label">비밀번호 확인</span>
              <input v-model="pw2" class="input" type="password" placeholder="비밀번호 재입력" minlength="8" required />
            </label>
  
            <label class="check">
              <input type="checkbox" v-model="agree" />
              <span>이용약관 및 개인정보 처리방침에 동의합니다.</span>
            </label>
  
            <button class="btn btn-primary" type="submit" :disabled="loading">
              {{ loading ? "가입 중..." : "가입하기" }}
            </button>
  
            <div class="footer">
              <span class="muted">이미 계정이 있나요?</span>
              <button class="link" type="button" @click="goLogin">로그인</button>
            </div>
          </form>
  
          <div v-if="toast" class="toast" :class="toastType">{{ toast }}</div>
        </section>
      </main>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  
  const router = useRouter();
  const name = ref("");
  const email = ref("");
  const pw = ref("");
  const pw2 = ref("");
  const agree = ref(false);
  const loading = ref(false);
  
  const toast = ref("");
  const toastType = ref<"ok" | "bad">("ok");
  let t: number | undefined;
  
  function showToast(msg: string, type: "ok" | "bad" = "ok") {
    toast.value = msg;
    toastType.value = type;
    if (t) window.clearTimeout(t);
    t = window.setTimeout(() => (toast.value = ""), 2500);
  }
  
  function goHome() {
    router.push({ name: "home" }).catch(() => {});
  }
  function goLogin() {
    router.push({ name: "login" }).catch(() => {});
  }
  
  async function onSubmit() {
    if (!agree.value) return showToast("약관 동의가 필요합니다.", "bad");
    if (pw.value !== pw2.value) return showToast("비밀번호가 일치하지 않습니다.", "bad");
  
    loading.value = true;
    // TODO: FastAPI 연동
    // POST /auth/signup { name, email, pw }
    await new Promise((r) => setTimeout(r, 700));
    loading.value = false;
  
    showToast("회원가입 완료! 로그인 페이지로 이동합니다.", "ok");
    setTimeout(() => goLogin(), 600);
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
    max-width: 760px;
    margin: 0 auto;
    padding: 18px;
  }
  .container.single {
    display: grid;
    place-items: start center;
  }
  .card {
    width: 100%;
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
  .check {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    font-weight: 800;
    color: #374151;
  }
  .footer {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-top: 6px;
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
  </style>
  