<template>
    <div class="app">
      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="sb-top">
          <div class="sb-logo">AI</div>
          <div class="sb-badge">ADMIN</div>
        </div>
  
        <nav class="sb-nav">
          <button class="sb-item active" title="관리자 대시보드" @click="tab = 'dashboard'">📊</button>
          <button class="sb-item" title="사용자 관리" @click="tab = 'users'">👥</button>
          <button class="sb-item" title="문서/분석 관리" @click="tab = 'docs'">📄</button>
          <button class="sb-item" title="Q&A/로그" @click="tab = 'logs'">🧾</button>
          <button class="sb-item" title="설정" @click="tab = 'settings'">⚙️</button>
        </nav>
  
        <div class="sb-bottom">
          <button class="sb-item" title="서비스로 돌아가기" @click="go('home')">↩️</button>
        </div>
      </aside>
  
      <!-- Main -->
      <div class="main">
        <!-- Topbar -->
        <header class="topbar">
          <div class="tb-left">
            <div class="tb-title">
              <span class="tb-title-strong">관리자</span>
              <span class="tb-sub">· 운영 현황 & 관리</span>
            </div>
  
            <div class="tb-meta">
              <span class="pill">상태: 정상</span>
              <span class="muted">·</span>
              <span class="muted">데모 데이터</span>
            </div>
          </div>
  
          <div class="tb-right">
            <button class="btn btn-outline" type="button" @click="refreshMock">새로고침</button>
            <button class="btn btn-primary" type="button" @click="deployMock">배포/점검(데모)</button>
          </div>
        </header>
  
        <!-- Content -->
        <main class="content">
          <!-- Tabs header -->
          <section class="tabs">
            <button class="tab" :class="{ on: tab === 'dashboard' }" @click="tab = 'dashboard'">대시보드</button>
            <button class="tab" :class="{ on: tab === 'users' }" @click="tab = 'users'">사용자</button>
            <button class="tab" :class="{ on: tab === 'docs' }" @click="tab = 'docs'">문서/분석</button>
            <button class="tab" :class="{ on: tab === 'logs' }" @click="tab = 'logs'">로그</button>
            <button class="tab" :class="{ on: tab === 'settings' }" @click="tab = 'settings'">설정</button>
          </section>
  
          <!-- DASHBOARD -->
          <section v-if="tab === 'dashboard'" class="grid">
            <article class="card">
              <div class="card-head">
                <h2>오늘의 요약</h2>
              </div>
  
              <div class="stat-grid">
                <div class="stat">
                  <div class="stat-label">총 사용자</div>
                  <div class="stat-value">{{ stats.users }}</div>
                </div>
                <div class="stat">
                  <div class="stat-label">총 문서</div>
                  <div class="stat-value">{{ stats.docs }}</div>
                </div>
                <div class="stat">
                  <div class="stat-label">분석 대기</div>
                  <div class="stat-value">{{ stats.queue }}</div>
                </div>
                <div class="stat">
                  <div class="stat-label">Q&A 요청(일)</div>
                  <div class="stat-value">{{ stats.qaToday }}</div>
                </div>
              </div>
  
              <div class="hint muted">
                (연동 포인트) FastAPI: <b>GET /admin/metrics</b> 로 교체 예정
              </div>
            </article>
  
            <article class="card">
              <div class="card-head">
                <h2>시스템 상태</h2>
              </div>
  
              <div class="health">
                <div class="health-row">
                  <div class="k">API</div>
                  <div class="v ok">OK</div>
                </div>
                <div class="health-row">
                  <div class="k">PostgreSQL</div>
                  <div class="v ok">OK</div>
                </div>
                <div class="health-row">
                  <div class="k">Worker(분석)</div>
                  <div class="v warn">DEGRADED</div>
                </div>
                <div class="health-row">
                  <div class="k">Storage</div>
                  <div class="v ok">OK</div>
                </div>
              </div>
  
              <div class="actions">
                <button class="btn btn-outline" type="button" @click="openLogs">에러 로그 보기</button>
                <button class="btn btn-primary" type="button" @click="restartMock">워커 재시작(데모)</button>
              </div>
            </article>
  
            <article class="card span2">
              <div class="card-head">
                <h2>최근 작업(분석 큐)</h2>
                <div class="head-actions">
                  <button class="btn btn-outline btn-sm" @click="tab = 'docs'">문서 관리로 →</button>
                </div>
              </div>
  
              <div class="table">
                <div class="thead">
                  <div class="th">작업 ID</div>
                  <div class="th">문서</div>
                  <div class="th">사용자</div>
                  <div class="th">상태</div>
                  <div class="th">생성</div>
                  <div class="th">작업</div>
                </div>
  
                <div v-for="j in jobs" :key="j.id" class="trow">
                  <div class="td mono">{{ j.id }}</div>
                  <div class="td">
                    <div class="strong">{{ j.docTitle }}</div>
                    <div class="muted small">docId: {{ j.docId }}</div>
                  </div>
                  <div class="td">{{ j.user }}</div>
                  <div class="td">
                    <span :class="['badge', jobBadge(j.status)]">{{ jobLabel(j.status) }}</span>
                  </div>
                  <div class="td muted">{{ fmt(j.createdAt) }}</div>
                  <div class="td">
                    <button class="btn btn-sm" @click="inspectJob(j)">보기</button>
                    <button class="btn btn-sm btn-outline" @click="cancelMock(j)" :disabled="j.status !== 'queued'">
                      취소
                    </button>
                  </div>
                </div>
              </div>
            </article>
          </section>
  
          <!-- USERS -->
          <section v-else-if="tab === 'users'" class="grid">
            <article class="card span2">
              <div class="card-head">
                <h2>사용자 관리</h2>
                <div class="head-actions">
                  <input class="input" v-model="userQ" placeholder="이메일/이름 검색..." />
                  <button class="btn btn-outline btn-sm" @click="createUserMock">+ 사용자 추가(데모)</button>
                </div>
              </div>
  
              <div class="table">
                <div class="thead users">
                  <div class="th">ID</div>
                  <div class="th">이메일</div>
                  <div class="th">권한</div>
                  <div class="th">상태</div>
                  <div class="th">가입</div>
                  <div class="th">작업</div>
                </div>
  
                <div v-for="u in filteredUsers" :key="u.id" class="trow users">
                  <div class="td mono">{{ u.id }}</div>
                  <div class="td">
                    <div class="strong">{{ u.email }}</div>
                    <div class="muted small">{{ u.name }}</div>
                  </div>
                  <div class="td">
                    <span class="chip" :class="{ admin: u.role === 'admin' }">{{ u.role }}</span>
                  </div>
                  <div class="td">
                    <span :class="['badge', u.active ? 'ok' : 'bad']">{{ u.active ? "활성" : "정지" }}</span>
                  </div>
                  <div class="td muted">{{ fmt(u.joinedAt) }}</div>
                  <div class="td">
                    <button class="btn btn-sm" @click="toggleRoleMock(u)">권한변경</button>
                    <button class="btn btn-sm btn-outline" @click="toggleActiveMock(u)">
                      {{ u.active ? "정지" : "활성" }}
                    </button>
                  </div>
                </div>
              </div>
            </article>
          </section>
  
          <!-- DOCS -->
          <section v-else-if="tab === 'docs'" class="grid">
            <article class="card span2">
              <div class="card-head">
                <h2>문서/분석 관리</h2>
                <div class="head-actions">
                  <select class="select" v-model="docStatus">
                    <option value="all">상태 전체</option>
                    <option value="done">완료</option>
                    <option value="processing">처리중</option>
                    <option value="failed">실패</option>
                  </select>
                  <button class="btn btn-outline btn-sm" @click="requeueMock">실패 재시도(데모)</button>
                </div>
              </div>
  
              <div class="table">
                <div class="thead docs">
                  <div class="th">문서 ID</div>
                  <div class="th">제목</div>
                  <div class="th">사용자</div>
                  <div class="th">상태</div>
                  <div class="th">업로드</div>
                  <div class="th">작업</div>
                </div>
  
                <div v-for="d in filteredDocs" :key="d.id" class="trow docs">
                  <div class="td mono">{{ d.id }}</div>
                  <div class="td">
                    <div class="strong">{{ d.title }}</div>
                    <div class="muted small">{{ d.type }}</div>
                  </div>
                  <div class="td">{{ d.user }}</div>
                  <div class="td">
                    <span :class="['badge', docBadge(d.status)]">{{ docLabel(d.status) }}</span>
                  </div>
                  <div class="td muted">{{ fmt(d.createdAt) }}</div>
                  <div class="td">
                    <button class="btn btn-sm" @click="openDoc(d.id)" :disabled="d.status !== 'done'">열기</button>
                    <button class="btn btn-sm btn-outline" @click="deleteDocMock(d)">삭제</button>
                  </div>
                </div>
              </div>
            </article>
          </section>
  
          <!-- LOGS -->
          <section v-else-if="tab === 'logs'" class="grid">
            <article class="card span2">
              <div class="card-head">
                <h2>운영 로그</h2>
                <div class="head-actions">
                  <button class="btn btn-outline btn-sm" @click="generateLogMock">샘플 로그 생성</button>
                </div>
              </div>
  
              <div class="logs">
                <div v-for="l in logs" :key="l.id" class="log">
                  <span :class="['lvl', l.level]">{{ l.level.toUpperCase() }}</span>
                  <span class="mono">{{ l.at }}</span>
                  <span class="msg">{{ l.msg }}</span>
                </div>
              </div>
            </article>
          </section>
  
          <!-- SETTINGS -->
          <section v-else class="grid">
            <article class="card span2">
              <div class="card-head">
                <h2>설정</h2>
              </div>
  
              <div class="settings">
                <div class="set-row">
                  <div>
                    <div class="strong">분석 워커 동시 처리 수</div>
                    <div class="muted small">(데모) 실제는 서버 설정 값</div>
                  </div>
                  <input class="input small-input" type="number" v-model.number="settings.workerConcurrency" min="1" max="64" />
                </div>
  
                <div class="set-row">
                  <div>
                    <div class="strong">Q&A 최대 컨텍스트 문단 수</div>
                    <div class="muted small">근거 패널에 표시할 최대 문단</div>
                  </div>
                  <input class="input small-input" type="number" v-model.number="settings.maxEvidence" min="1" max="20" />
                </div>
  
                <div class="set-row">
                  <div>
                    <div class="strong">파일 최대 업로드(MB)</div>
                    <div class="muted small">PDF/이미지 제한</div>
                  </div>
                  <input class="input small-input" type="number" v-model.number="settings.maxUploadMb" min="1" max="500" />
                </div>
  
                <div class="actions">
                  <button class="btn btn-primary" @click="saveSettingsMock">저장(데모)</button>
                  <button class="btn btn-outline" @click="resetSettingsMock">초기화</button>
                </div>
              </div>
            </article>
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
  
  type Tab = "dashboard" | "users" | "docs" | "logs" | "settings";
  const tab = ref<Tab>("dashboard");
  
  const toast = ref("");
  let timer: number | undefined;
  function showToast(msg: string) {
    toast.value = msg;
    if (timer) window.clearTimeout(timer);
    timer = window.setTimeout(() => (toast.value = ""), 1400);
  }
  
  function go(name: string) {
    router.push({ name }).catch(() => {});
  }
  function openDoc(id: string) {
    router.push({ name: "documentView", params: { id } }).catch(() => {});
  }
  function openLogs() {
    tab.value = "logs";
    showToast("로그 탭으로 이동");
  }
  
  function fmt(iso: string) {
    const d = new Date(iso);
    return d.toLocaleString("ko-KR", { month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" });
  }
  
  /* ---- Dashboard data (demo) ---- */
  const stats = ref({
    users: 128,
    docs: 943,
    queue: 7,
    qaToday: 41,
  });
  
  type JobStatus = "queued" | "running" | "done" | "failed";
  interface JobItem {
    id: string;
    docId: string;
    docTitle: string;
    user: string;
    status: JobStatus;
    createdAt: string;
  }
  const jobs = ref<JobItem[]>([
    { id: "job_1001", docId: "doc_121", docTitle: "사내 보안 정책 개정 안내", user: "user01@corp.com", status: "queued", createdAt: new Date(Date.now()-1000*60*5).toISOString() },
    { id: "job_1002", docId: "doc_122", docTitle: "협력사 계약서 표준 조항", user: "partner@ext.com", status: "running", createdAt: new Date(Date.now()-1000*60*18).toISOString() },
    { id: "job_1003", docId: "doc_119", docTitle: "개인정보 처리방침 변경 공지", user: "user02@corp.com", status: "done", createdAt: new Date(Date.now()-1000*60*60).toISOString() },
    { id: "job_1004", docId: "doc_118", docTitle: "공공기관 민원 안내문(이미지)", user: "public@guest.com", status: "failed", createdAt: new Date(Date.now()-1000*60*90).toISOString() },
  ]);
  
  function jobBadge(s: JobStatus) {
    if (s === "done") return "ok";
    if (s === "running") return "warn";
    if (s === "queued") return "info";
    return "bad";
  }
  function jobLabel(s: JobStatus) {
    if (s === "done") return "완료";
    if (s === "running") return "실행중";
    if (s === "queued") return "대기";
    return "실패";
  }
  function inspectJob(j: JobItem) {
    showToast(`작업 보기(데모): ${j.id}`);
  }
  function cancelMock(j: JobItem) {
    showToast(`취소(데모): ${j.id}`);
  }
  
  /* ---- Users (demo) ---- */
  type Role = "user" | "admin";
  interface UserItem {
    id: string;
    email: string;
    name: string;
    role: Role;
    active: boolean;
    joinedAt: string;
  }
  const users = ref<UserItem[]>([
    { id: "u_001", email: "user01@corp.com", name: "User 01", role: "user", active: true, joinedAt: new Date(Date.now()-1000*60*60*24*8).toISOString() },
    { id: "u_002", email: "admin@docassist.com", name: "Admin", role: "admin", active: true, joinedAt: new Date(Date.now()-1000*60*60*24*30).toISOString() },
    { id: "u_003", email: "partner@ext.com", name: "Partner", role: "user", active: true, joinedAt: new Date(Date.now()-1000*60*60*24*3).toISOString() },
    { id: "u_004", email: "blocked@corp.com", name: "Blocked", role: "user", active: false, joinedAt: new Date(Date.now()-1000*60*60*24*40).toISOString() },
  ]);
  
  const userQ = ref("");
  const filteredUsers = computed(() => {
    const q = userQ.value.trim().toLowerCase();
    if (!q) return users.value;
    return users.value.filter((u) => u.email.toLowerCase().includes(q) || u.name.toLowerCase().includes(q));
  });
  
  function toggleRoleMock(u: UserItem) {
    users.value = users.value.map((x) => (x.id === u.id ? { ...x, role: x.role === "admin" ? "user" : "admin" } : x));
    showToast("권한 변경(데모)");
  }
  function toggleActiveMock(u: UserItem) {
    users.value = users.value.map((x) => (x.id === u.id ? { ...x, active: !x.active } : x));
    showToast("활성/정지 변경(데모)");
  }
  function createUserMock() {
    showToast("사용자 추가(데모)");
  }
  
  /* ---- Docs (demo) ---- */
  type DocStatus = "done" | "processing" | "failed";
  interface DocItem {
    id: string;
    title: string;
    type: "PDF" | "PNG" | "JPG";
    user: string;
    status: DocStatus;
    createdAt: string;
  }
  const docs = ref<DocItem[]>([
    { id: "doc_121", title: "사내 보안 정책 개정 안내", type: "PDF", user: "user01@corp.com", status: "processing", createdAt: new Date(Date.now()-1000*60*40).toISOString() },
    { id: "doc_119", title: "개인정보 처리방침 변경 공지", type: "PDF", user: "user02@corp.com", status: "done", createdAt: new Date(Date.now()-1000*60*120).toISOString() },
    { id: "doc_118", title: "공공기관 민원 안내문(이미지)", type: "PNG", user: "public@guest.com", status: "failed", createdAt: new Date(Date.now()-1000*60*180).toISOString() },
  ]);
  
  const docStatus = ref<"all" | DocStatus>("all");
  const filteredDocs = computed(() => {
    if (docStatus.value === "all") return docs.value;
    return docs.value.filter((d) => d.status === docStatus.value);
  });
  
  function docBadge(s: DocStatus) {
    if (s === "done") return "ok";
    if (s === "processing") return "warn";
    return "bad";
  }
  function docLabel(s: DocStatus) {
    if (s === "done") return "완료";
    if (s === "processing") return "처리중";
    return "실패";
  }
  function deleteDocMock(d: DocItem) {
    const ok = confirm(`삭제할까요? (데모)\n${d.id} - ${d.title}`);
    if (!ok) return;
    docs.value = docs.value.filter((x) => x.id !== d.id);
    showToast("삭제(데모)");
  }
  function requeueMock() {
    showToast("재시도(데모): 실패 문서 재처리 요청 예정");
  }
  
  /* ---- Logs (demo) ---- */
  interface LogItem {
    id: string;
    level: "info" | "warn" | "error";
    at: string;
    msg: string;
  }
  const logs = ref<LogItem[]>([
    { id: "l1", level: "info", at: new Date().toISOString(), msg: "서비스 시작" },
    { id: "l2", level: "warn", at: new Date().toISOString(), msg: "Worker latency increased" },
    { id: "l3", level: "error", at: new Date().toISOString(), msg: "OCR task failed: timeout" },
  ]);
  
  function generateLogMock() {
    logs.value = [
      { id: `l${Date.now()}`, level: "info", at: new Date().toISOString(), msg: "Health check OK" },
      ...logs.value,
    ];
    showToast("로그 생성(데모)");
  }
  
  /* ---- Settings (demo) ---- */
  const settings = ref({
    workerConcurrency: 4,
    maxEvidence: 6,
    maxUploadMb: 25,
  });
  function saveSettingsMock() {
    showToast("저장(데모): 서버에 반영 예정");
  }
  function resetSettingsMock() {
    settings.value = { workerConcurrency: 4, maxEvidence: 6, maxUploadMb: 25 };
    showToast("초기화");
  }
  
  /* ---- Header actions (demo) ---- */
  function refreshMock() {
    showToast("새로고침(데모)");
  }
  function deployMock() {
    showToast("배포/점검(데모)");
  }
  function restartMock() {
    showToast("워커 재시작(데모)");
  }
  </script>
  
  <style scoped>
  .app {
    min-height: 100vh;
    background: #f4f6fb;
    color: #111827;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR", Arial;
    display: grid;
    grid-template-columns: 84px 1fr;
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
  .sb-top { display: grid; place-items: center; gap: 6px; padding: 6px 0 10px; }
  .sb-logo {
    width: 48px; height: 48px;
    border-radius: 16px;
    display: grid; place-items: center;
    background: rgba(255,255,255,0.14);
    font-weight: 1000;
  }
  .sb-badge {
    font-size: 10px;
    font-weight: 1000;
    letter-spacing: 1px;
    padding: 4px 8px;
    border-radius: 999px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.14);
  }
  .sb-nav, .sb-bottom {
    display: grid;
    gap: 10px;
    width: 100%;
    justify-items: center;
  }
  .sb-bottom { margin-top: auto; padding-bottom: 8px; }
  .sb-item {
    width: 48px; height: 48px;
    border-radius: 16px;
    border: none;
    background: transparent;
    color: #fff;
    cursor: pointer;
    display: grid;
    place-items: center;
    font-size: 18px;
    opacity: 0.92;
  }
  .sb-item:hover { background: rgba(255,255,255,0.12); }
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
  .tb-title-strong { font-weight: 1000; font-size: 16px; }
  .tb-sub { color: #6b7280; font-size: 12px; font-weight: 700; }
  .tb-meta { display: flex; align-items: center; gap: 8px; }
  .pill {
    font-size: 12px;
    padding: 2px 10px;
    border-radius: 999px;
    border: 1px solid #e5e7eb;
    background: #f9fafb;
    font-weight: 900;
  }
  .muted { color: #6b7280; font-size: 12px; font-weight: 700; }
  .small { font-size: 12px; }
  .tb-right { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
  
  /* Content */
  .content {
    max-width: 1280px;
    margin: 0 auto;
    padding: 16px 18px 44px;
    display: grid;
    gap: 12px;
  }
  
  /* Tabs */
  .tabs {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    align-items: center;
  }
  .tab {
    border: 1px solid #e5e7eb;
    background: #fff;
    padding: 10px 12px;
    border-radius: 999px;
    font-weight: 1000;
    cursor: pointer;
  }
  .tab.on {
    border-color: #bfdbfe;
    background: #eff6ff;
    color: #1d4ed8;
  }
  
  /* Grid / Cards */
  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    align-items: start;
  }
  .card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 16px;
  }
  .span2 { grid-column: 1 / -1; }
  .card-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 10px;
  }
  .card-head h2 { margin: 0; font-size: 16px; font-weight: 1000; }
  .head-actions { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
  
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
  .stat-label { color: #6b7280; font-size: 12px; font-weight: 900; }
  .stat-value { font-weight: 1000; font-size: 22px; margin-top: 6px; }
  .hint { margin-top: 10px; }
  
  .health { display: grid; gap: 10px; }
  .health-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 12px;
    border: 1px solid #eef2f7;
    border-radius: 14px;
  }
  .k { font-weight: 900; }
  .v { font-weight: 1000; }
  .v.ok { color: #065f46; }
  .v.warn { color: #92400e; }
  .v.bad { color: #991b1b; }
  
  .actions { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px; }
  
  /* Tables */
  .table { width: 100%; }
  .thead, .trow {
    display: grid;
    grid-template-columns: 140px 1fr 180px 120px 140px 220px;
    gap: 10px;
    align-items: center;
  }
  .thead {
    padding: 10px 10px;
    border-bottom: 1px solid #eef2f7;
    color: #6b7280;
    font-size: 12px;
    font-weight: 1000;
  }
  .trow {
    padding: 12px 10px;
    border-bottom: 1px solid #f1f5f9;
  }
  .trow:last-child { border-bottom: none; }
  
  .thead.users, .trow.users {
    grid-template-columns: 120px 1fr 120px 120px 140px 220px;
  }
  .thead.docs, .trow.docs {
    grid-template-columns: 140px 1fr 180px 120px 140px 220px;
  }
  
  .strong { font-weight: 1000; }
  .mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }
  
  .badge {
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid transparent;
    white-space: nowrap;
    font-weight: 1000;
  }
  .badge.ok { background: #ecfdf5; border-color: #a7f3d0; color: #065f46; }
  .badge.warn { background: #fffbeb; border-color: #fde68a; color: #92400e; }
  .badge.bad { background: #fef2f2; border-color: #fecaca; color: #991b1b; }
  .badge.info { background: #eff6ff; border-color: #bfdbfe; color: #1d4ed8; }
  
  .chip {
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid #e5e7eb;
    background: #f9fafb;
    font-weight: 1000;
  }
  .chip.admin {
    border-color: #bfdbfe;
    background: #eff6ff;
    color: #1d4ed8;
  }
  
  /* Logs */
  .logs { display: grid; gap: 10px; }
  .log {
    border: 1px solid #eef2f7;
    border-radius: 14px;
    padding: 10px 12px;
    display: grid;
    grid-template-columns: 90px 230px 1fr;
    gap: 12px;
    align-items: center;
  }
  .lvl {
    font-weight: 1000;
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid transparent;
    justify-self: start;
  }
  .lvl.info { background: #eff6ff; border-color: #bfdbfe; color: #1d4ed8; }
  .lvl.warn { background: #fffbeb; border-color: #fde68a; color: #92400e; }
  .lvl.error { background: #fef2f2; border-color: #fecaca; color: #991b1b; }
  .msg { font-weight: 800; }
  
  /* Settings */
  .settings { display: grid; gap: 12px; }
  .set-row {
    border: 1px solid #eef2f7;
    border-radius: 14px;
    padding: 12px;
    display: flex;
    justify-content: space-between;
    gap: 12px;
    align-items: center;
  }
  .small-input { width: 120px; }
  
  /* Inputs */
  .input {
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 10px 12px;
    outline: none;
    background: #fff;
    font-weight: 900;
  }
  .select {
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 10px 12px;
    background: #fff;
    font-weight: 900;
  }
  
  /* Buttons */
  .btn {
    border: 1px solid #e5e7eb;
    background: #fff;
    padding: 10px 12px;
    border-radius: 12px;
    font-weight: 1000;
    cursor: pointer;
  }
  .btn:hover { background: #f9fafb; }
  .btn-primary { background: #2563eb; border-color: #2563eb; color: #fff; }
  .btn-primary:hover { background: #1d4ed8; }
  .btn-outline { border-color: #cbd5e1; }
  .btn-sm { padding: 8px 10px; border-radius: 10px; }
  
  .toast {
    position: fixed;
    left: 50%;
    bottom: 18px;
    transform: translateX(-50%);
    padding: 10px 12px;
    border-radius: 14px;
    font-weight: 1000;
    border: 1px solid #bfdbfe;
    background: #eff6ff;
    color: #1d4ed8;
  }
  
  @media (max-width: 980px) {
    .grid { grid-template-columns: 1fr; }
    .thead, .trow { grid-template-columns: 120px 1fr 160px 110px 120px 200px; }
    .thead.users, .trow.users { grid-template-columns: 110px 1fr 110px 110px 120px 200px; }
  }
  @media (max-width: 720px) {
    .app { grid-template-columns: 70px 1fr; }
    .thead { display: none; }
    .trow, .trow.users, .trow.docs {
      grid-template-columns: 1fr;
      gap: 8px;
    }
  }
  </style>
  