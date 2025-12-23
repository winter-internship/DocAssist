<template>
  <div class="page">
    <div class="shell">
      <!-- LEFT -->
      <section class="left">
        <div class="left-top">
          <img class="logo" src="/logo.png" alt="DocAssist" />
        </div>

        <div class="left-center">
          <div class="welcome">Reset<br />Password</div>
          <div class="left-sub">이메일로 재설정 링크를 보내드려요</div>
        </div>

        <div class="left-bottom">
          <div class="mini">© {{ new Date().getFullYear() }} DocAssist</div>
        </div>
      </section>

      <!-- RIGHT -->
      <section class="right">
        <h1 class="title">Forget Password</h1>
        <p class="desc">가입한 이메일을 입력하면 재설정 링크를 전송합니다.</p>

        <form class="form" @submit.prevent="onSubmit">
          <label class="field">
            <span class="label">Email</span>
            <input
              class="input"
              type="email"
              placeholder="you@example.com"
              v-model="email"
              autocomplete="email"
              required
            />
          </label>

          <button class="btn" type="submit" :disabled="loading">
            {{ loading ? "Sending..." : "Send reset link" }}
          </button>

          <div v-if="sent" class="success">
            ✅ 재설정 링크를 전송했어요. 메일함을 확인해주세요. (데모)
          </div>

          <div v-if="error" class="error">{{ error }}</div>

          <div class="footer">
            <button class="link strong" type="button" @click="goLogin">← Back to Login</button>
            <span class="muted">·</span>
            <button class="link strong" type="button" @click="goSignup">Signup</button>
          </div>
        </form>
      </section>
    </div>

    <div class="bg" />
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const email = ref("");
const loading = ref(false);
const sent = ref(false);
const error = ref("");

function goLogin() {
  router.push({ name: "login" }).catch(() => {});
}
function goSignup() {
  router.push({ name: "signup" }).catch(() => {});
}

async function onSubmit() {
  error.value = "";
  sent.value = false;
  loading.value = true;

  try {
    if (!email.value.includes("@")) throw new Error("이메일 형식이 올바르지 않아요.");

    // TODO: FastAPI 연결
    // POST /auth/forgot-password { email }

    sent.value = true;
  } catch (e: any) {
    error.value = e?.message ?? "요청에 실패했어요.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
:root {
  --b1: #1d4ed8;
  --b2: #0ea5e9;
  --ink: #111827;
  --muted: #6b7280;
  --line: #e5e7eb;
  --ring: rgba(29, 78, 216, 0.18);
}

.page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  background: #f3f7ff;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR", Arial;
  position: relative;
  overflow: hidden;
}

.bg {
  position: absolute;
  inset: -40%;
  background:
    radial-gradient(circle at 20% 20%, rgba(14,165,233,0.22), transparent 45%),
    radial-gradient(circle at 80% 60%, rgba(29,78,216,0.18), transparent 45%),
    radial-gradient(circle at 50% 90%, rgba(59,130,246,0.14), transparent 40%);
  filter: blur(20px);
  z-index: 0;
}

.shell {
  width: min(980px, 100%);
  min-height: 520px;
  background: #fff;
  border-radius: 22px;
  box-shadow: 0 24px 70px rgba(17, 24, 39, 0.18);
  overflow: hidden;
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  z-index: 1;
}

/* left */
.left {
  position: relative;
  color: #fff;
  padding: 26px 26px 18px;
  background: linear-gradient(135deg, rgba(29,78,216,0.95), rgba(14,165,233,0.90));
}
.left::before {
  content: "";
  position: absolute;
  inset: -20%;
  background:
    radial-gradient(circle at 30% 35%, rgba(255,255,255,0.22), transparent 45%),
    radial-gradient(circle at 70% 65%, rgba(255,255,255,0.12), transparent 45%);
  transform: rotate(10deg);
  opacity: 0.9;
}
.left-top, .left-center, .left-bottom { position: relative; z-index: 1; }
.left-top { display: flex; align-items: center; }
.logo {
  width: 34px; height: 34px; object-fit: contain; border-radius: 10px;
  filter: drop-shadow(0 10px 18px rgba(0,0,0,0.22));
}
.left-center { margin-top: 68px; }
.welcome {
  font-weight: 1000;
  font-size: 56px;
  line-height: 1.02;
  letter-spacing: -0.8px;
  text-shadow: 0 18px 30px rgba(0, 0, 0, 0.18);
}
.left-sub { margin-top: 16px; font-weight: 800; opacity: 0.9; }
.left-bottom { margin-top: auto; padding-top: 80px; }
.mini { font-weight: 800; opacity: 0.7; font-size: 12px; }

/* right */
.right { padding: 46px 46px 34px; display: grid; align-content: start; }
.title { margin: 0; font-size: 32px; font-weight: 1000; color: var(--ink); }
.desc { margin: 10px 0 22px; color: var(--muted); font-weight: 700; font-size: 13px; }

.form { display: grid; gap: 16px; }
.field { display: grid; gap: 8px; }
.label { font-size: 12px; color: #9ca3af; font-weight: 900; }

.input {
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 12px 12px;
  outline: none;
  font-weight: 800;
  color: var(--ink);
  background: #fff;
}
.input:focus { border-color: rgba(29,78,216,0.35); box-shadow: 0 0 0 3px var(--ring); }

.btn {
  margin-top: 6px;
  height: 46px;
  border: none;
  border-radius: 10px;
  font-weight: 1000;
  color: #fff;
  cursor: pointer;
  background: linear-gradient(90deg, var(--b1), var(--b2));
  box-shadow: 0 14px 24px rgba(14,165,233,0.20);
}
.btn:hover { filter: brightness(0.98); }
.btn:disabled { opacity: 0.7; cursor: not-allowed; }

.success {
  border: 1px solid #bbf7d0;
  background: #ecfdf5;
  color: #065f46;
  border-radius: 12px;
  padding: 10px 12px;
  font-weight: 900;
  font-size: 12px;
}

.link {
  border: none;
  background: transparent;
  color: var(--b1);
  font-weight: 900;
  cursor: pointer;
  padding: 4px 6px;
  border-radius: 8px;
  font-size: 12px;
}
.link:hover { background: rgba(29, 78, 216, 0.08); }
.link.strong { padding: 0 6px; }

.footer {
  margin-top: 10px;
  display: flex;
  gap: 8px;
  align-items: center;
  justify-content: center;
}

.muted { color: #9ca3af; font-weight: 800; font-size: 12px; }

.error {
  border: 1px solid #fecaca;
  background: #fef2f2;
  color: #991b1b;
  border-radius: 12px;
  padding: 10px 12px;
  font-weight: 900;
  font-size: 12px;
}

@media (max-width: 900px) {
  .shell { grid-template-columns: 1fr; }
  .left-center { margin-top: 26px; }
  .welcome { font-size: 44px; }
  .right { padding: 28px 22px 22px; }
}
</style>
