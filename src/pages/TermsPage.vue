<template>
    <div class="app">
      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="sb-brand">
          <div class="sb-logo">
            <img src="/logo.png" alt="DoQ" />
          </div>
          <div class="sb-name">DoQ</div>
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
            <span class="ico">⬆️</span><span class="txt">업로드</span>
          </button>

          <button class="sb-item" @click="go('qa')">
            <span class="ico">💬</span><span class="txt">Q&A</span>
          </button>
        <button class="sb-item" @click="go('terms')">
          <span class="ico">📘</span><span class="txt">용어집</span>
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
          <button class="sb-mini" @click="toggleTheme" :title="theme === 'dark' ? 'Light' : 'Dark'">
            {{ theme === "dark" ? "☀️" : "🌙" }}
          </button>
          <button class="sb-mini" @click="logout" title="Logout">↩️</button>
        </div>
      </aside>
  
      <!-- Main -->
      <div class="main">
        <!-- Topbar -->
        <header class="topbar">
          <div class="tb-left">
            <div class="tb-title">
              <span class="tb-title-strong">용어집</span>
              <span class="tb-sub">· 문서에서 추출된 전문 용어/정의를 모아봅니다</span>
            </div>
  
            <div class="tb-meta">
              <span class="pill">총 {{ filteredTerms.length }}개</span>
              <span class="muted">·</span>
              <span class="muted">{{ selectedDocLabel }}</span>
            </div>
          </div>
  
          <div class="tb-right">
            <button class="btn btn-outline" type="button" @click="exportMock">내보내기(데모)</button>
            <button class="btn btn-primary" type="button" @click="go('upload')">+ 새 문서 업로드</button>
          </div>
        </header>
  
        <main class="content">
          <!-- Filters -->
          <section class="filters">
            <div class="left">
              <select class="select" v-model="docFilter">
                <option value="all">문서 전체</option>
                <option v-for="d in docs" :key="d.id" :value="d.id">
                  {{ d.title }}
                </option>
              </select>
  
              <select class="select" v-model="tagFilter">
                <option value="all">태그 전체</option>
                <option value="legal">법/규정</option>
                <option value="security">보안</option>
                <option value="finance">재무</option>
                <option value="policy">정책</option>
                <option value="general">일반</option>
              </select>
  
              <select class="select" v-model="sortBy">
                <option value="freq">빈도순</option>
                <option value="alpha">가나다순</option>
                <option value="new">최근추가순</option>
              </select>
            </div>
  
            <div class="right">
              <input v-model.trim="q" class="input" placeholder="용어/정의 검색..." />
              <button class="btn btn-outline" type="button" @click="resetFilters">초기화</button>
            </div>
          </section>
  
          <section class="grid">
            <!-- List -->
            <article class="card list">
              <div class="card-head">
                <h2>용어 목록</h2>
                <div class="head-actions">
                  <button class="link" type="button" @click="togglePinnedOnly">
                    {{ pinnedOnly ? "전체 보기" : "핀만 보기" }}
                  </button>
                </div>
              </div>
  
              <div v-if="filteredTerms.length === 0" class="empty">
                결과가 없어요.
                <button class="inline" type="button" @click="resetFilters">필터 초기화</button>
              </div>
  
              <ul v-else class="term-list">
                <li
                  v-for="t in pagedTerms"
                  :key="t.id"
                  class="term-item"
                  :class="{ active: selected?.id === t.id }"
                  @click="selectTerm(t)"
                >
                  <div class="term-left">
                    <div class="term-title">
                      <span class="pin" @click.stop="togglePin(t)">{{ t.pinned ? "📌" : "📍" }}</span>
                      {{ t.term }}
                    </div>
                    <div class="term-sub muted">
                      <span class="chip">{{ tagLabel(t.tag) }}</span>
                      <span class="muted">·</span>
                      <span class="muted">{{ docTitle(t.docId) }}</span>
                    </div>
                  </div>
  
                  <div class="term-right">
                    <span class="badge">{{ t.freq }}회</span>
                    <button class="btn btn-sm btn-outline" type="button" @click.stop="copyTerm(t)">
                      복사
                    </button>
                  </div>
                </li>
              </ul>
  
              <div v-if="filteredTerms.length > 0" class="pager">
                <div class="muted">페이지 {{ page }} / {{ totalPages }}</div>
                <div class="pager-actions">
                  <button class="btn btn-outline btn-sm" type="button" :disabled="page <= 1" @click="page--">이전</button>
                  <button class="btn btn-outline btn-sm" type="button" :disabled="page >= totalPages" @click="page++">다음</button>
                </div>
              </div>
            </article>
  
            <!-- Detail -->
            <article class="card detail">
              <div class="card-head">
                <h2>상세</h2>
                <div class="head-actions">
                  <button class="btn btn-outline btn-sm" type="button" :disabled="!selected" @click="openDocFromTerm">
                    문서에서 보기
                  </button>
                </div>
              </div>
  
              <div v-if="!selected" class="empty">
                왼쪽에서 용어를 선택하면 정의/근거 문장을 보여줘요.
              </div>
  
              <div v-else class="detail-body">
                <div class="detail-title">
                  <div class="big">{{ selected.term }}</div>
                  <div class="detail-meta">
                    <span class="chip">{{ tagLabel(selected.tag) }}</span>
                    <span class="muted">·</span>
                    <span class="muted">{{ docTitle(selected.docId) }}</span>
                    <span class="muted">·</span>
                    <span class="muted">빈도 {{ selected.freq }}회</span>
                  </div>
                </div>
  
                <div class="block">
                  <div class="block-title">정의(쉬운 설명)</div>
                  <div class="block-text">
                    {{ selected.definition }}
                  </div>
                </div>
  
                <div class="block">
                  <div class="block-title">근거 문장(예시)</div>
                  <ul class="evid">
                    <li v-for="(s, idx) in selected.evidence" :key="idx" class="evid-item">
                      <span class="evid-no">#{{ idx + 1 }}</span>
                      <span class="evid-text">{{ s }}</span>
                    </li>
                  </ul>
                </div>
  
                <div class="block">
                  <div class="block-title">액션</div>
                  <div class="actions">
                    <button class="btn btn-primary" type="button" @click="askWithTerm">
                      이 용어로 Q&A 질문하기(데모)
                    </button>
                    <button class="btn btn-outline" type="button" @click="copyDefinition">
                      정의 복사
                    </button>
                  </div>
                  <div class="hint muted">
                    (연동 예정) FastAPI: 용어/정의/근거 문장 반환 → 여기서 Q&A로 넘기기
                  </div>
                </div>
              </div>
  
              <div v-if="toast" class="toast">{{ toast }}</div>
            </article>
          </section>
        </main>
      </div>
    </div>
</template>
  
 <script setup lang="ts">
  import { computed, ref, watch, onMounted } from "vue";
  import { useRouter } from "vue-router";

  const sidebarQ = ref("");
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
    localStorage.removeItem("access_token");
    localStorage.removeItem("role");
    localStorage.removeItem("user_name");
    localStorage.removeItem("user_email");
    localStorage.removeItem("remember_me");
    localStorage.removeItem("last_login_at");
    router.push({ name: "login" }).catch(() => {});
  }
  
  type Tag = "legal" | "security" | "finance" | "policy" | "general";
  
  interface DocItem {
    id: string;
    title: string;
  }
  
  interface TermItem {
    id: string;
    docId: string;
    term: string;
    definition: string;
    evidence: string[];
    tag: Tag;
    freq: number;
    pinned: boolean;
    createdAt: string; // ISO
  }
  
  const router = useRouter();
  
  const docs = ref<DocItem[]>([
    { id: "doc_001", title: "사내 보안 정책 개정 안내" },
    { id: "doc_004", title: "사내 출장 정산 가이드" },
    { id: "doc_007", title: "개인정보 처리방침 변경 공지" },
  ]);
  
  const terms = ref<TermItem[]>([
    {
      id: "t1",
      docId: "doc_001",
      term: "접근 통제(Access Control)",
      definition: "누가(사용자/시스템) 어떤 정보에 접근할 수 있는지 권한을 정해 관리하는 규칙/기능이에요.",
      evidence: [
        "본 정책은 중요 정보 자산에 대한 접근 통제를 강화한다.",
        "권한 승인 없이 시스템에 접근하는 행위를 금지한다.",
      ],
      tag: "security",
      freq: 8,
      pinned: true,
      createdAt: new Date(Date.now() - 1000 * 60 * 60 * 10).toISOString(),
    },
    {
      id: "t2",
      docId: "doc_001",
      term: "기밀성(Confidentiality)",
      definition: "허가된 사람만 정보를 볼 수 있도록 보호하는 성질이에요.",
      evidence: ["기밀성 유지 의무를 위반할 경우 징계 대상이 된다."],
      tag: "security",
      freq: 5,
      pinned: false,
      createdAt: new Date(Date.now() - 1000 * 60 * 60 * 14).toISOString(),
    },
    {
      id: "t3",
      docId: "doc_004",
      term: "증빙 서류",
      definition: "비용을 실제로 썼다는 것을 보여주는 영수증/계약서/내역서 같은 문서예요.",
      evidence: ["출장비 정산 시 증빙 서류를 반드시 첨부한다."],
      tag: "finance",
      freq: 6,
      pinned: false,
      createdAt: new Date(Date.now() - 1000 * 60 * 60 * 30).toISOString(),
    },
    {
      id: "t4",
      docId: "doc_007",
      term: "개인정보 처리(Processing)",
      definition: "개인정보를 수집·이용·보관·제공·파기하는 모든 행위를 말해요.",
      evidence: ["개인정보 처리는 법령 및 내부 규정에 따라 수행한다."],
      tag: "legal",
      freq: 9,
      pinned: true,
      createdAt: new Date(Date.now() - 1000 * 60 * 60 * 40).toISOString(),
    },
    {
      id: "t5",
      docId: "doc_007",
      term: "보유기간(Retention Period)",
      definition: "개인정보를 보관하는 기간이에요. 기간이 끝나면 안전하게 삭제(파기)해야 해요.",
      evidence: ["보유기간 경과 시 지체 없이 파기한다."],
      tag: "policy",
      freq: 4,
      pinned: false,
      createdAt: new Date(Date.now() - 1000 * 60 * 60 * 60).toISOString(),
    },
  ]);
  
  const q = ref("");
  const docFilter = ref<"all" | string>("all");
  const tagFilter = ref<"all" | Tag>("all");
  const sortBy = ref<"freq" | "alpha" | "new">("freq");
  const pinnedOnly = ref(false);
  
  const page = ref(1);
  const perPage = 6;
  
  const selected = ref<TermItem | null>(null);
  
  const toast = ref("");
  let tt: number | undefined;
  
  function showToast(msg: string) {
    toast.value = msg;
    if (tt) window.clearTimeout(tt);
    tt = window.setTimeout(() => (toast.value = ""), 1800);
  }
  
  function go(name: string) {
    router.push({ name }).catch(() => {});
  }
  
  function docTitle(id: string) {
    return docs.value.find((d) => d.id === id)?.title ?? id;
  }
  
  function tagLabel(tag: Tag) {
    if (tag === "legal") return "법/규정";
    if (tag === "security") return "보안";
    if (tag === "finance") return "재무";
    if (tag === "policy") return "정책";
    return "일반";
  }
  
  const filteredTerms = computed(() => {
    const qq = q.value.trim().toLowerCase();
  
    let arr = terms.value.filter((t) => {
      const matchQ = !qq || t.term.toLowerCase().includes(qq) || t.definition.toLowerCase().includes(qq);
      const matchDoc = docFilter.value === "all" ? true : t.docId === docFilter.value;
      const matchTag = tagFilter.value === "all" ? true : t.tag === tagFilter.value;
      const matchPin = pinnedOnly.value ? t.pinned : true;
      return matchQ && matchDoc && matchTag && matchPin;
    });
  
    if (sortBy.value === "freq") arr.sort((a, b) => b.freq - a.freq);
    if (sortBy.value === "alpha") arr.sort((a, b) => a.term.localeCompare(b.term, "ko"));
    if (sortBy.value === "new") arr.sort((a, b) => +new Date(b.createdAt) - +new Date(a.createdAt));
  
    return arr;
  });
  
  const totalPages = computed(() => Math.max(1, Math.ceil(filteredTerms.value.length / perPage)));
  const pagedTerms = computed(() => {
    const start = (page.value - 1) * perPage;
    return filteredTerms.value.slice(start, start + perPage);
  });
  
  watch([q, docFilter, tagFilter, sortBy, pinnedOnly], () => {
    page.value = 1;
  
    // 선택된 항목이 필터 결과에서 사라지면 selection 해제
    if (selected.value && !filteredTerms.value.some((t) => t.id === selected.value?.id)) {
      selected.value = null;
    }
  });
  
  watch(totalPages, () => {
    page.value = Math.min(page.value, totalPages.value);
  });
  
  const selectedDocLabel = computed(() => {
    if (docFilter.value === "all") return "문서 전체";
    return docTitle(docFilter.value);
  });
  
  function resetFilters() {
    q.value = "";
    docFilter.value = "all";
    tagFilter.value = "all";
    sortBy.value = "freq";
    pinnedOnly.value = false;
    page.value = 1;
    selected.value = null;
  }
  
  function togglePinnedOnly() {
    pinnedOnly.value = !pinnedOnly.value;
  }
  
  function selectTerm(t: TermItem) {
    selected.value = t;
  }
  
  function togglePin(t: TermItem) {
    terms.value = terms.value.map((x) => (x.id === t.id ? { ...x, pinned: !x.pinned } : x));
    // 선택 상태 갱신
    if (selected.value?.id === t.id) {
      selected.value = terms.value.find((x) => x.id === t.id) ?? null;
    }
  }
  
  async function copyTerm(t: TermItem) {
    try {
      await navigator.clipboard.writeText(t.term);
      showToast("용어 복사 완료");
    } catch {
      showToast("복사 실패(권한/브라우저 설정 확인)");
    }
  }
  
  async function copyDefinition() {
    if (!selected.value) return;
    try {
      await navigator.clipboard.writeText(selected.value.definition);
      showToast("정의 복사 완료");
    } catch {
      showToast("복사 실패(권한/브라우저 설정 확인)");
    }
  }
  
  function openDocFromTerm() {
    if (!selected.value) return;
    router.push({ name: "documentView", params: { id: selected.value.docId } }).catch(() => {});
  }
  
  function openLastDoc() {
    // 데모: 고정 문서
    router.push({ name: "documentView", params: { id: "doc_001" } }).catch(() => {});
  }
  
  function askWithTerm() {
    if (!selected.value) return;
    alert(`(데모) Q&A로 이동: "${selected.value.term}" 관련 질문을 생성할 예정`);
  }
  
  function exportMock() {
    alert("(데모) 용어집 내보내기: CSV/PDF로 다운로드 연결 예정");
  }
 </script>
  
<style scoped>
  :global(:root) {
    --b1: #1d4ed8;
    --b2: #0ea5e9;
    --ring: rgba(29, 78, 216, 0.18);
  }

  .app {
    min-height: 100vh;
    display: grid;
    grid-template-columns: 280px 1fr;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR", Arial;
    color: #111827;
    background: #f4f6fb;
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
  :global(:root[data-theme="dark"]) .sidebar {
    background: rgba(12, 23, 43, 0.72);
  }

  .sb-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 6px;
  }
  .sb-logo {
    width: 36px;
    height: 36px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.7);
    border: 1px solid #e5e7eb;
    display: grid;
    place-items: center;
    overflow: hidden;
  }
  :global(:root[data-theme="dark"]) .sb-logo {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(148, 163, 184, 0.2);
  }
  .sb-logo img {
    width: 22px;
    height: 22px;
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
  :global(:root[data-theme="dark"]) .sb-input {
    background: rgba(255, 255, 255, 0.06);
    color: #e5e7eb;
    border-color: rgba(148, 163, 184, 0.2);
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
  :global(:root[data-theme="dark"]) .sb-sep {
    background: rgba(148, 163, 184, 0.2);
  }

  .sb-bottom {
    margin-top: auto;
    display: flex;
    gap: 8px;
    padding: 8px 6px 0;
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
  :global(:root[data-theme="dark"]) .sb-mini {
    background: rgba(255, 255, 255, 0.06);
    color: #e5e7eb;
    border-color: rgba(148, 163, 184, 0.2);
  }
  
  /* Main */
  .main {
    display: grid;
    grid-template-rows: 76px 1fr;
  }
  
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
    font-weight: 900;
    font-size: 16px;
  }
  .tb-sub {
    color: #6b7280;
    font-size: 12px;
  }
  .tb-meta {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .pill {
    font-size: 12px;
    padding: 2px 10px;
    border-radius: 999px;
    border: 1px solid #e5e7eb;
    background: #f9fafb;
    font-weight: 800;
  }
  .muted {
    color: #6b7280;
    font-size: 12px;
  }
  .tb-right {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
  }
  
  /* Content */
  .content {
    max-width: 1280px;
    margin: 0 auto;
    padding: 16px 18px 44px;
    display: grid;
    gap: 14px;
  }
  
  /* Filters */
  .filters {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
    align-items: center;
  }
  .filters .left,
  .filters .right {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: center;
  }
  .select {
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 10px 12px;
    background: #fff;
    font-weight: 800;
  }
  .input {
    width: min(420px, 78vw);
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
  
  /* Grid */
  .grid {
    display: grid;
    grid-template-columns: 1fr 0.95fr;
    gap: 14px;
    align-items: start;
  }
  
  /* Cards */
  .card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 16px;
    position: relative;
  }
  .card-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 10px;
  }
  .card-head h2 {
    margin: 0;
    font-size: 16px;
    font-weight: 900;
  }
  .head-actions {
    display: flex;
    gap: 10px;
    align-items: center;
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
    font-weight: 900;
    cursor: pointer;
    padding: 0 2px;
  }
  
  /* List */
  .term-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 10px;
  }
  .term-item {
    border: 1px solid #eef2f7;
    border-radius: 14px;
    padding: 12px;
    display: flex;
    justify-content: space-between;
    gap: 12px;
    cursor: pointer;
  }
  .term-item:hover {
    border-color: #dbeafe;
    background: #f8fbff;
  }
  .term-item.active {
    outline: 2px solid rgba(37, 99, 235, 0.18);
    border-color: #bfdbfe;
  }
  .term-title {
    font-weight: 900;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .pin {
    cursor: pointer;
  }
  .term-sub {
    margin-top: 6px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .term-right {
    display: flex;
    gap: 10px;
    align-items: center;
  }
  .chip {
    font-size: 12px;
    border: 1px solid #e5e7eb;
    padding: 2px 8px;
    border-radius: 999px;
    background: #f9fafb;
    font-weight: 900;
  }
  .badge {
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid #e5e7eb;
    background: #fff;
    white-space: nowrap;
    font-weight: 900;
  }
  
  /* Detail */
  .detail-title .big {
    font-size: 20px;
    font-weight: 900;
  }
  .detail-meta {
    margin-top: 6px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
  }
  .block {
    margin-top: 14px;
    border: 1px solid #eef2f7;
    border-radius: 14px;
    padding: 12px;
    background: #fff;
  }
  .block-title {
    font-weight: 900;
    margin-bottom: 8px;
  }
  .block-text {
    line-height: 1.65;
    color: #374151;
    font-weight: 700;
  }
  .evid {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 10px;
  }
  .evid-item {
    display: grid;
    grid-template-columns: 44px 1fr;
    gap: 10px;
    align-items: start;
  }
  .evid-no {
    font-weight: 900;
    color: #2563eb;
  }
  .evid-text {
    line-height: 1.6;
    color: #374151;
    font-weight: 700;
  }
  .actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  .hint {
    margin-top: 10px;
  }
  
  /* Pager */
  .pager {
    margin-top: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
  }
  .pager-actions {
    display: flex;
    gap: 10px;
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
  .btn-sm {
    padding: 8px 10px;
    border-radius: 10px;
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
  
  .toast {
    position: absolute;
    left: 16px;
    right: 16px;
    bottom: 14px;
    padding: 10px 12px;
    border-radius: 14px;
    font-weight: 900;
    border: 1px solid #a7f3d0;
    background: #ecfdf5;
    color: #065f46;
  }
  
  @media (max-width: 980px) {
    .grid {
      grid-template-columns: 1fr;
    }
  }
</style>
  


