<template>
  <div class="app">
    <!-- Sidebar -->
    <aside class="sidebar">
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
        <div class="sb-sep"></div>
        <button class="sb-item" :class="{ active: tab === 'dashboard' }" @click="tab = 'dashboard'">
          <span class="ico">📊</span><span class="txt">대시보드</span>
        </button>
        <button class="sb-item" :class="{ active: tab === 'users' }" @click="tab = 'users'">
          <span class="ico">👥</span><span class="txt">사용자</span>
        </button>
        <button class="sb-item" :class="{ active: tab === 'docs' }" @click="tab = 'docs'">
          <span class="ico">📄</span><span class="txt">문서 관리</span>
        </button>
        <button class="sb-item" :class="{ active: tab === 'tickets' }" @click="tab = 'tickets'">
          <span class="ico">🧾</span><span class="txt">문의/신고</span>
        </button>
        <button class="sb-item" :class="{ active: tab === 'access' }" @click="tab = 'access'">
          <span class="ico">🛡️</span><span class="txt">권한/접근</span>
        </button>
        <button class="sb-item" :class="{ active: tab === 'logs' }" @click="tab = 'logs'">
          <span class="ico">🧰</span><span class="txt">로그/통계</span>
        </button>
        <button class="sb-item" :class="{ active: tab === 'settings' }" @click="tab = 'settings'">
          <span class="ico">⚙️</span><span class="txt">설정</span>
        </button>
      </nav>

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
            <span class="muted">데이터</span>
          </div>
        </div>

        <div class="tb-right">
          <button class="btn btn-outline" type="button" @click="refreshMock">새로고침</button>
        </div>
      </header>

      <!-- Tabs -->
      <section class="tabs-bar">
        <div class="tabs">
          <button class="tab" :class="{ on: tab === 'dashboard' }" @click="tab = 'dashboard'">대시보드</button>
          <button class="tab" :class="{ on: tab === 'users' }" @click="tab = 'users'">사용자</button>
          <button class="tab" :class="{ on: tab === 'docs' }" @click="tab = 'docs'">문서 관리</button>
          <button class="tab" :class="{ on: tab === 'tickets' }" @click="tab = 'tickets'">문의/신고</button>
          <button class="tab" :class="{ on: tab === 'access' }" @click="tab = 'access'">권한/접근</button>
          <button class="tab" :class="{ on: tab === 'logs' }" @click="tab = 'logs'">로그/통계</button>
          <button class="tab" :class="{ on: tab === 'settings' }" @click="tab = 'settings'">설정</button>
        </div>
      </section>

      <!-- Content -->
      <main class="content">

        <!-- DASHBOARD -->
        <section v-if="tab === 'dashboard'" class="grid dash-grid">
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
              <button class="btn btn-primary" type="button" @click="restartMock">워커 재시작</button>
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
                <button class="btn btn-outline btn-sm" @click="createUserMock">+ 사용자 추가</button>
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
                <button class="btn btn-outline btn-sm" @click="requeueMock">실패 재시도</button>
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

        <!-- TICKETS -->
        <section v-else-if="tab === 'tickets'" class="grid">
          <article class="card span2">
            <div class="card-head">
              <h2>문의/신고 처리</h2>
              <div class="head-actions">
                <select class="select" v-model="ticketStatus">
                  <option value="all">전체</option>
                  <option value="open">접수</option>
                  <option value="in_progress">처리 중</option>
                  <option value="resolved">완료</option>
                </select>
                <button class="btn btn-outline btn-sm" @click="bulkResolveMock">일괄 처리</button>
              </div>
            </div>

            <div class="table">
              <div class="thead tickets">
                <div class="th">ID</div>
                <div class="th">제목</div>
                <div class="th">요청자</div>
                <div class="th">우선순위</div>
                <div class="th">상태</div>
                <div class="th">작업</div>
              </div>

              <div v-for="t in filteredTickets" :key="t.id" class="trow tickets">
                <div class="td mono">{{ t.id }}</div>
                <div class="td">
                  <div class="strong">{{ t.subject }}</div>
                  <div class="muted small">{{ t.type }}</div>
                </div>
                <div class="td">{{ t.requester }}</div>
                <div class="td">
                  <span :class="['badge', ticketPriorityBadge(t.priority)]">{{ ticketPriorityLabel(t.priority) }}</span>
                </div>
                <div class="td">
                  <span :class="['badge', ticketStatusBadge(t.status)]">{{ ticketStatusLabel(t.status) }}</span>
                </div>
                <div class="td">
                  <button class="btn btn-sm" @click="assignTicketMock(t)">담당</button>
                  <button class="btn btn-sm btn-outline" @click="resolveTicketMock(t)">완료</button>
                </div>
              </div>
            </div>
          </article>
        </section>

        <!-- ACCESS -->
        <section v-else-if="tab === 'access'" class="grid">
          <article class="card span2">
            <div class="card-head">
              <h2>역할 관리</h2>
              <div class="head-actions">
                <button class="btn btn-outline btn-sm" @click="createRoleMock">+ 역할 추가</button>
              </div>
            </div>

            <div class="table">
              <div class="thead roles">
                <div class="th">ID</div>
                <div class="th">역할</div>
                <div class="th">인원</div>
                <div class="th">업데이트</div>
                <div class="th">작업</div>
              </div>

              <div v-for="r in roles" :key="r.id" class="trow roles">
                <div class="td mono">{{ r.id }}</div>
                <div class="td">
                  <div class="strong">{{ r.name }}</div>
                  <div class="muted small">{{ r.desc }}</div>
                </div>
                <div class="td">{{ r.members }}</div>
                <div class="td muted">{{ fmt(r.updatedAt) }}</div>
                <div class="td">
                  <button class="btn btn-sm" @click="editRoleMock(r)">편집</button>
                  <button class="btn btn-sm btn-outline" @click="auditRoleMock(r)">감사</button>
                </div>
              </div>
            </div>
          </article>

          <article class="card span2">
            <div class="card-head">
              <h2>접근 정책</h2>
              <div class="head-actions">
                <button class="btn btn-outline btn-sm" @click="syncPolicyMock">동기화</button>
              </div>
            </div>

            <div class="table">
              <div class="thead policies">
                <div class="th">ID</div>
                <div class="th">정책</div>
                <div class="th">범위</div>
                <div class="th">보안 등급</div>
                <div class="th">상태</div>
              </div>

              <div v-for="p in policies" :key="p.id" class="trow policies">
                <div class="td mono">{{ p.id }}</div>
                <div class="td">
                  <div class="strong">{{ p.name }}</div>
                  <div class="muted small">{{ p.updatedBy }}</div>
                </div>
                <div class="td">{{ p.scope }}</div>
                <div class="td">{{ p.level }}</div>
                <div class="td">
                  <button class="btn btn-sm" :class="{ 'btn-outline': p.enabled }" @click="togglePolicyMock(p)">
                    {{ p.enabled ? "활성" : "중지" }}
                  </button>
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

            <div class="stat-grid stats-compact">
              <div class="stat">
                <div class="stat-label">총 로그</div>
                <div class="stat-value">{{ logStats.total }}</div>
              </div>
              <div class="stat">
                <div class="stat-label">경고</div>
                <div class="stat-value">{{ logStats.warn }}</div>
              </div>
              <div class="stat">
                <div class="stat-label">에러</div>
                <div class="stat-value">{{ logStats.error }}</div>
              </div>
              <div class="stat">
                <div class="stat-label">오늘 이벤트</div>
                <div class="stat-value">{{ logStats.today }}</div>
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
                  <div class="muted small">실제는 서버 설정 값</div>
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
                <button class="btn btn-primary" @click="saveSettingsMock">저장</button>
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

const sidebarQ = ref("");

type Tab = "dashboard" | "users" | "docs" | "tickets" | "access" | "logs" | "settings";
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
  showToast(`작업 보기: ${j.id}`);
}
function cancelMock(j: JobItem) {
  showToast(`취소: ${j.id}`);
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
  { id: "u_002", email: "admin@DoQ.com", name: "Admin", role: "admin", active: true, joinedAt: new Date(Date.now()-1000*60*60*24*30).toISOString() },
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
  showToast("권한 변경");
}
function toggleActiveMock(u: UserItem) {
  users.value = users.value.map((x) => (x.id === u.id ? { ...x, active: !x.active } : x));
  showToast("활성/정지 변경");
}
function createUserMock() {
  showToast("사용자 추가");
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
  const ok = confirm(`삭제할까요?\n${d.id} - ${d.title}`);
  if (!ok) return;
  docs.value = docs.value.filter((x) => x.id !== d.id);
  showToast("삭제");
}
function requeueMock() {
  showToast("재시도: 실패 문서 재처리 요청 예정");
}

/* ---- Tickets (demo) ---- */
type TicketStatus = "open" | "in_progress" | "resolved";
type TicketPriority = "low" | "medium" | "high";
interface TicketItem {
  id: string;
  type: string;
  subject: string;
  requester: string;
  status: TicketStatus;
  priority: TicketPriority;
  createdAt: string;
}
const tickets = ref<TicketItem[]>([
  { id: "t_1001", type: "문의", subject: "결제 영수증 재발급", requester: "user01@corp.com", status: "open", priority: "low", createdAt: new Date(Date.now()-1000*60*50).toISOString() },
  { id: "t_1002", type: "신고", subject: "문서 접근 권한 오류", requester: "auditor@corp.com", status: "in_progress", priority: "high", createdAt: new Date(Date.now()-1000*60*120).toISOString() },
  { id: "t_1003", type: "문의", subject: "OCR 처리 지연", requester: "partner@ext.com", status: "open", priority: "medium", createdAt: new Date(Date.now()-1000*60*200).toISOString() },
  { id: "t_1004", type: "신고", subject: "비정상 로그인 의심", requester: "sec@corp.com", status: "resolved", priority: "high", createdAt: new Date(Date.now()-1000*60*300).toISOString() },
]);

const ticketStatus = ref<"all" | TicketStatus>("all");
const filteredTickets = computed(() => {
  if (ticketStatus.value === "all") return tickets.value;
  return tickets.value.filter((t) => t.status === ticketStatus.value);
});

function ticketPriorityBadge(p: TicketPriority) {
  if (p === "high") return "bad";
  if (p === "medium") return "warn";
  return "info";
}
function ticketPriorityLabel(p: TicketPriority) {
  if (p === "high") return "높음";
  if (p === "medium") return "중간";
  return "낮음";
}
function ticketStatusBadge(s: TicketStatus) {
  if (s === "resolved") return "ok";
  if (s === "in_progress") return "warn";
  return "info";
}
function ticketStatusLabel(s: TicketStatus) {
  if (s === "resolved") return "완료";
  if (s === "in_progress") return "처리 중";
  return "접수";
}
function assignTicketMock(t: TicketItem) {
  tickets.value = tickets.value.map((x) => (x.id === t.id ? { ...x, status: "in_progress" } : x));
  showToast(`담당 지정: ${t.id}`);
}
function resolveTicketMock(t: TicketItem) {
  tickets.value = tickets.value.map((x) => (x.id === t.id ? { ...x, status: "resolved" } : x));
  showToast(`처리 완료: ${t.id}`);
}
function bulkResolveMock() {
  tickets.value = tickets.value.map((x) => (x.status === "resolved" ? x : { ...x, status: "resolved" }));
  showToast("일괄 처리");
}

/* ---- Access control (demo) ---- */
interface RoleItem {
  id: string;
  name: string;
  desc: string;
  members: number;
  updatedAt: string;
}
const roles = ref<RoleItem[]>([
  { id: "r_admin", name: "Admin", desc: "전체 관리 권한", members: 2, updatedAt: new Date(Date.now()-1000*60*60*24).toISOString() },
  { id: "r_auditor", name: "Auditor", desc: "로그/감사 열람", members: 4, updatedAt: new Date(Date.now()-1000*60*60*48).toISOString() },
  { id: "r_ops", name: "Ops", desc: "운영/모니터링", members: 6, updatedAt: new Date(Date.now()-1000*60*60*72).toISOString() },
]);

interface PolicyItem {
  id: string;
  name: string;
  scope: string;
  level: string;
  enabled: boolean;
  updatedBy: string;
}
const policies = ref<PolicyItem[]>([
  { id: "p_01", name: "문서 접근", scope: "Drive/Upload", level: "L2", enabled: true, updatedBy: "admin@DoQ.com" },
  { id: "p_02", name: "외부 공유 제한", scope: "Drive", level: "L3", enabled: true, updatedBy: "sec@corp.com" },
  { id: "p_03", name: "대량 다운로드 차단", scope: "API", level: "L4", enabled: false, updatedBy: "ops@corp.com" },
]);

function createRoleMock() {
  showToast("역할 추가");
}
function editRoleMock(r: RoleItem) {
  showToast(`역할 편집: ${r.name}`);
}
function auditRoleMock(r: RoleItem) {
  showToast(`권한 감사: ${r.name}`);
}
function syncPolicyMock() {
  showToast("정책 동기화");
}
function togglePolicyMock(p: PolicyItem) {
  policies.value = policies.value.map((x) => (x.id === p.id ? { ...x, enabled: !x.enabled } : x));
  showToast(`정책 ${p.enabled ? "중지" : "활성"}: ${p.id}`);
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

const logStats = computed(() => {
  const total = logs.value.length;
  const warn = logs.value.filter((l) => l.level === "warn").length;
  const error = logs.value.filter((l) => l.level === "error").length;
  return {
    total,
    warn,
    error,
    today: total,
  };
});

function generateLogMock() {
  logs.value = [
    { id: `l${Date.now()}`, level: "info", at: new Date().toISOString(), msg: "Health check OK" },
    ...logs.value,
  ];
  showToast("로그 생성");
}

/* ---- Settings (demo) ---- */
const settings = ref({
  workerConcurrency: 4,
  maxEvidence: 6,
  maxUploadMb: 25,
});
function saveSettingsMock() {
  showToast("저장: 서버에 반영 예정");
}
function resetSettingsMock() {
  settings.value = { workerConcurrency: 4, maxEvidence: 6, maxUploadMb: 25 };
  showToast("초기화");
}

/* ---- Header actions (demo) ---- */
function refreshMock() {
  showToast("새로고침");
}
function deployMock() {
  showToast("배포/점검");
}
function restartMock() {
  showToast("워커 재시작");
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
  background: var(--bg);
  color: var(--ink);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR", Arial;
  display: grid;
  grid-template-columns: 280px 1fr;
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
.main { display: grid; grid-template-rows: 76px 56px 1fr; }

/* Topbar */
.topbar {
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 18px;
  gap: 12px;
  position: sticky;
  top: 0;
  z-index: 10;
  height: 76px;
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
  max-width: 1480px;
  width: 100%;
  margin: 0 auto;
  padding: 16px 12px 32px;
  display: grid;
  gap: 16px;
  justify-items: stretch;
}

/* Tabs */
.tabs-bar {
  position: sticky;
  top: 76px;
  z-index: 9;
  background: #f4f6fb;
  border-bottom: 1px solid #e5e7eb;
}
.tabs {
  max-width: 1280px;
  margin: 0 auto;
  padding: 10px 18px;
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: nowrap;
  overflow-x: auto;
  scrollbar-width: none;
  height: 56px;
}
.tabs::-webkit-scrollbar { display: none; }
.tab {
  border: 1px solid #e5e7eb;
  background: #fff;
  padding: 10px 12px;
  border-radius: 999px;
  font-weight: 1000;
  cursor: pointer;
  font-size: 13px;
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
.dash-grid {
  align-items: stretch;
}
.dash-grid .card {
  height: 100%;
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

.stats-compact {
  grid-template-columns: repeat(4, minmax(140px, 1fr));
  margin-bottom: 12px;
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

.thead.tickets, .trow.tickets {
  grid-template-columns: 120px 1fr 180px 120px 120px 200px;
}
.thead.roles, .trow.roles {
  grid-template-columns: 120px 1fr 120px 140px 180px;
}
.thead.policies, .trow.policies {
  grid-template-columns: 120px 1fr 120px 120px 140px;
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
  .stats-compact { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 720px) {
  .thead { display: none; }
  .trow, .trow.users, .trow.docs, .trow.tickets, .trow.roles, .trow.policies {
    grid-template-columns: 1fr;
    gap: 8px;
  }
}
</style>















