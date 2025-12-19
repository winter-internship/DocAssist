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
          <button class="sb-item active" title="내 드라이브">🗂️</button>
          <button class="sb-item" title="문서 보기(최근 열기)" @click="openLastDoc">📄</button>
          <button class="sb-item" title="Q&A(준비중)" disabled>💬</button>
          <button class="sb-item" title="용어집(준비중)" disabled>📚</button>
          <button class="sb-item" title="프로필(준비중)" disabled>👤</button>
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
              <span class="tb-title-strong">내 드라이브</span>
              <span class="tb-sub">· 업로드한 문서를 관리하세요</span>
            </div>
  
            <div class="tb-meta">
              <span class="pill">총 {{ filteredDocs.length }}건</span>
              <span class="muted">·</span>
              <span class="muted">최근 {{ recentDays }}일</span>
            </div>
          </div>
  
          <div class="tb-right">
            <button class="btn btn-outline" type="button" @click="refreshMock">새로고침</button>
            <button class="btn btn-primary" type="button" @click="go('upload')">+ 새 문서 업로드</button>
          </div>
        </header>
  
        <!-- Content -->
        <main class="content">
          <!-- Search / Filters -->
          <section class="filters">
            <div class="search">
              <input
                v-model="q"
                class="input"
                placeholder="문서 제목/유형/상태로 검색..."
                @keydown.enter.prevent
              />
            </div>
  
            <div class="selects">
              <select class="select" v-model="typeFilter">
                <option value="all">유형 전체</option>
                <option value="PDF">PDF</option>
                <option value="JPG">JPG</option>
                <option value="PNG">PNG</option>
              </select>
  
              <select class="select" v-model="statusFilter">
                <option value="all">상태 전체</option>
                <option value="done">분석 완료</option>
                <option value="processing">분석 중</option>
                <option value="failed">실패</option>
              </select>
  
              <select class="select" v-model="sortBy">
                <option value="new">최신순</option>
                <option value="old">오래된순</option>
                <option value="title">제목순</option>
              </select>
            </div>
          </section>
  
          <!-- Table/Card -->
          <section class="card">
            <div class="card-head">
              <h2>문서 목록</h2>
              <div class="head-actions">
                <button class="link" type="button" @click="selectAll">전체 선택</button>
                <button class="link" type="button" @click="clearSelect">선택 해제</button>
                <button
                  class="btn btn-outline btn-sm"
                  type="button"
                  :disabled="selectedIds.size === 0"
                  @click="deleteMock"
                >
                  삭제(데모)
                </button>
              </div>
            </div>
  
            <div v-if="filteredDocs.length === 0" class="empty">
              검색 결과가 없어요.
              <button class="inline" type="button" @click="resetFilters">필터 초기화</button>
            </div>
  
            <div v-else class="table">
              <div class="thead">
                <div class="th chk"></div>
                <div class="th title">제목</div>
                <div class="th meta">유형</div>
                <div class="th meta">상태</div>
                <div class="th meta">업로드</div>
                <div class="th actions">작업</div>
              </div>
  
              <div
                v-for="doc in pagedDocs"
                :key="doc.id"
                class="trow"
                :class="{ selected: selectedIds.has(doc.id) }"
              >
                <div class="td chk">
                  <input
                    type="checkbox"
                    :checked="selectedIds.has(doc.id)"
                    @change="toggleSelect(doc.id)"
                  />
                </div>
  
                <div class="td title">
                  <div class="doc-title">{{ doc.title }}</div>
                  <div class="doc-sub muted">ID: {{ doc.id }}</div>
                </div>
  
                <div class="td meta">
                  <span class="chip">{{ doc.type }}</span>
                </div>
  
                <div class="td meta">
                  <span :class="['badge', badgeClass(doc.status)]">
                    {{ statusLabel(doc.status) }}
                  </span>
                </div>
  
                <div class="td meta muted">{{ formatDate(doc.createdAt) }}</div>
  
                <div class="td actions">
                  <button
                    class="btn btn-sm"
                    type="button"
                    @click="openDoc(doc)"
                    :disabled="doc.status !== 'done'"
                  >
                    열기
                  </button>
                  <button class="btn btn-sm btn-outline" type="button" @click="renameMock(doc)">
                    이름변경
                  </button>
                </div>
              </div>
            </div>
  
            <!-- Pagination -->
            <div v-if="filteredDocs.length > 0" class="pager">
              <div class="muted">페이지 {{ page }} / {{ totalPages }}</div>
              <div class="pager-actions">
                <button class="btn btn-outline btn-sm" type="button" :disabled="page <= 1" @click="page--">
                  이전
                </button>
                <button
                  class="btn btn-outline btn-sm"
                  type="button"
                  :disabled="page >= totalPages"
                  @click="page++"
                >
                  다음
                </button>
              </div>
            </div>
          </section>
  
          <!-- Right: quick preview / stats -->
          <section class="grid">
            <article class="card">
              <div class="card-head">
                <h2>상태 요약</h2>
              </div>
  
              <div class="stat-grid">
                <div class="stat">
                  <div class="stat-label">분석 완료</div>
                  <div class="stat-value">{{ counts.done }}</div>
                </div>
                <div class="stat">
                  <div class="stat-label">분석 중</div>
                  <div class="stat-value">{{ counts.processing }}</div>
                </div>
                <div class="stat">
                  <div class="stat-label">실패</div>
                  <div class="stat-value">{{ counts.failed }}</div>
                </div>
                <div class="stat">
                  <div class="stat-label">전체</div>
                  <div class="stat-value">{{ counts.total }}</div>
                </div>
              </div>
            </article>
  
            <article class="card">
              <div class="card-head">
                <h2>선택한 문서</h2>
              </div>
  
              <div v-if="selectedIds.size === 0" class="empty small">
                아직 선택한 문서가 없어요.
              </div>
  
              <ul v-else class="sel-list">
                <li v-for="id in Array.from(selectedIds)" :key="id" class="sel-item">
                  <span class="sel-dot"></span>
                  <span class="sel-text">{{ id }}</span>
                </li>
              </ul>
  
              <div class="hint muted">(데모) 선택한 문서로 “일괄 내보내기/삭제” 같은 기능을 붙일 예정</div>
            </article>
          </section>
        </main>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed, ref, watch } from "vue";
  import { useRouter } from "vue-router";
  
  type DocStatus = "processing" | "done" | "failed";
  type DocType = "PDF" | "JPG" | "PNG";
  
  interface DocItem {
    id: string;
    title: string;
    type: DocType;
    status: DocStatus;
    createdAt: string; // ISO
  }
  
  const router = useRouter();
  
  const recentDays = 30;
  const q = ref("");
  const typeFilter = ref<"all" | DocType>("all");
  const statusFilter = ref<"all" | DocStatus>("all");
  const sortBy = ref<"new" | "old" | "title">("new");
  
  const page = ref(1);
  const perPage = 6;
  
  const docs = ref<DocItem[]>([
    { id: "doc_001", title: "사내 보안 정책 개정 안내", type: "PDF", status: "done", createdAt: new Date(Date.now() - 1000 * 60 * 60 * 4).toISOString() },
    { id: "doc_002", title: "고객 대상 서비스 이용약관 변경 공지", type: "PDF", status: "processing", createdAt: new Date(Date.now() - 1000 * 60 * 60 * 18).toISOString() },
    { id: "doc_003", title: "공공기관 민원 안내문(이미지)", type: "PNG", status: "failed", createdAt: new Date(Date.now() - 1000 * 60 * 60 * 30).toISOString() },
    { id: "doc_004", title: "사내 출장 정산 가이드", type: "PDF", status: "done", createdAt: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString() },
    { id: "doc_005", title: "보안 교육 수강 안내", type: "JPG", status: "done", createdAt: new Date(Date.now() - 1000 * 60 * 60 * 72).toISOString() },
    { id: "doc_006", title: "협력사 계약서 표준 조항", type: "PDF", status: "processing", createdAt: new Date(Date.now() - 1000 * 60 * 60 * 90).toISOString() },
    { id: "doc_007", title: "개인정보 처리방침 변경 공지", type: "PDF", status: "done", createdAt: new Date(Date.now() - 1000 * 60 * 60 * 120).toISOString() },
  ]);
  
  const selectedIds = ref<Set<string>>(new Set());
  
  function go(name: string) {
    router.push({ name }).catch(() => {});
  }
  
  function badgeClass(status: DocStatus) {
    if (status === "done") return "badge-ok";
    if (status === "processing") return "badge-warn";
    return "badge-bad";
  }
  function statusLabel(status: DocStatus) {
    if (status === "done") return "분석 완료";
    if (status === "processing") return "분석 중";
    return "실패";
  }
  function formatDate(iso: string) {
    const d = new Date(iso);
    return d.toLocaleDateString("ko-KR", { year: "numeric", month: "2-digit", day: "2-digit" });
  }
  
  const filteredDocs = computed(() => {
    const qq = q.value.trim().toLowerCase();
  
    let arr = docs.value.filter((d) => {
      const matchQ =
        !qq ||
        d.title.toLowerCase().includes(qq) ||
        d.type.toLowerCase().includes(qq) ||
        d.status.toLowerCase().includes(qq);
  
      const matchType = typeFilter.value === "all" ? true : d.type === typeFilter.value;
      const matchStatus = statusFilter.value === "all" ? true : d.status === statusFilter.value;
      return matchQ && matchType && matchStatus;
    });
  
    if (sortBy.value === "new") arr.sort((a, b) => +new Date(b.createdAt) - +new Date(a.createdAt));
    if (sortBy.value === "old") arr.sort((a, b) => +new Date(a.createdAt) - +new Date(b.createdAt));
    if (sortBy.value === "title") arr.sort((a, b) => a.title.localeCompare(b.title, "ko"));
  
    return arr;
  });
  
  const totalPages = computed(() => Math.max(1, Math.ceil(filteredDocs.value.length / perPage)));
  const pagedDocs = computed(() => {
    const start = (page.value - 1) * perPage;
    return filteredDocs.value.slice(start, start + perPage);
  });
  
  watch([q, typeFilter, statusFilter, sortBy], () => {
    page.value = 1;
    selectedIds.value = new Set();
  });
  
  watch(totalPages, () => {
    page.value = Math.min(page.value, totalPages.value);
  });
  
  const counts = computed(() => {
    const all = filteredDocs.value;
    return {
      total: all.length,
      done: all.filter((d) => d.status === "done").length,
      processing: all.filter((d) => d.status === "processing").length,
      failed: all.filter((d) => d.status === "failed").length,
    };
  });
  
  /** ✅ 필터 초기화 (너가 물어본 함수) */
  function resetFilters() {
    q.value = "";
    typeFilter.value = "all";
    statusFilter.value = "all";
    sortBy.value = "new";
    page.value = 1;
    selectedIds.value = new Set();
  }
  
  function toggleSelect(id: string) {
    const next = new Set(selectedIds.value);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    selectedIds.value = next;
  }
  function selectAll() {
    selectedIds.value = new Set(filteredDocs.value.map((d) => d.id));
  }
  function clearSelect() {
    selectedIds.value = new Set();
  }
  
  function openDoc(doc: DocItem) {
    if (doc.status !== "done") return;
    router.push({ name: "documentView", params: { id: doc.id } }).catch(() => {});
  }
  function openLastDoc() {
    const lastDone = filteredDocs.value.find((d) => d.status === "done");
    if (lastDone) openDoc(lastDone);
    else alert("열 수 있는(분석 완료) 문서가 아직 없어요.");
  }
  
  // 데모 액션들
  function refreshMock() {
    alert("새로고침(데모): FastAPI에서 목록 다시 불러오게 연결할 예정");
  }
  function renameMock(doc: DocItem) {
    const name = prompt("새 제목을 입력하세요", doc.title);
    if (!name) return;
    docs.value = docs.value.map((d) => (d.id === doc.id ? { ...d, title: name } : d));
  }
  function deleteMock() {
    if (selectedIds.value.size === 0) return;
    const ok = confirm(`선택한 ${selectedIds.value.size}개 문서를 삭제할까요? (데모)`);
    if (!ok) return;
    const del = selectedIds.value;
    docs.value = docs.value.filter((d) => !del.has(d.id));
    selectedIds.value = new Set();
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
  .sb-top {
    padding: 6px 0 10px;
  }
  .sb-logo {
    width: 44px;
    height: 44px;
    border-radius: 14px;
    display: grid;
    place-items: center;
    background: rgba(255, 255, 255, 0.14);
    font-weight: 900;
  }
  .sb-nav,
  .sb-bottom {
    display: grid;
    gap: 8px;
    width: 100%;
    justify-items: center;
  }
  .sb-bottom {
    margin-top: auto;
    padding-bottom: 6px;
  }
  .sb-item {
    width: 44px;
    height: 44px;
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
  .sb-item:hover {
    background: rgba(255, 255, 255, 0.12);
  }
  .sb-item:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
  .sb-item.active {
    background: rgba(255, 255, 255, 0.18);
    outline: 1px solid rgba(255, 255, 255, 0.16);
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
    max-width: 1220px;
    margin: 0 auto;
    padding: 16px 18px 44px;
    display: grid;
    gap: 14px;
  }
  
  /* Filters */
  .filters {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 12px;
    align-items: center;
  }
  .search {
    display: flex;
  }
  .input {
    width: 100%;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 10px 12px;
    outline: none;
  }
  .input:focus {
    border-color: #93c5fd;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
  }
  .selects {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    justify-content: flex-end;
  }
  .select {
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 10px 12px;
    background: #fff;
    font-weight: 700;
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
  .card-head h2 {
    margin: 0;
    font-size: 16px;
    font-weight: 900;
  }
  .head-actions {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
  }
  
  .table {
    width: 100%;
  }
  .thead,
  .trow {
    display: grid;
    grid-template-columns: 44px 1fr 120px 130px 140px 220px;
    gap: 10px;
    align-items: center;
  }
  .thead {
    padding: 10px 10px;
    border-bottom: 1px solid #eef2f7;
    color: #6b7280;
    font-size: 12px;
    font-weight: 900;
  }
  .trow {
    padding: 12px 10px;
    border-bottom: 1px solid #f1f5f9;
  }
  .trow:last-child {
    border-bottom: none;
  }
  .trow.selected {
    background: #f8fbff;
  }
  
  .td.title .doc-title {
    font-weight: 900;
  }
  .doc-sub {
    margin-top: 4px;
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
    border: 1px solid transparent;
    white-space: nowrap;
    font-weight: 900;
  }
  .badge-ok {
    background: #ecfdf5;
    border-color: #a7f3d0;
    color: #065f46;
  }
  .badge-warn {
    background: #fffbeb;
    border-color: #fde68a;
    color: #92400e;
  }
  .badge-bad {
    background: #fef2f2;
    border-color: #fecaca;
    color: #991b1b;
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
  
  /* Right grid */
  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
  }
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
  .stat-label {
    color: #6b7280;
    font-size: 12px;
    font-weight: 900;
  }
  .stat-value {
    font-weight: 900;
    font-size: 20px;
    margin-top: 6px;
  }
  
  .sel-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 8px;
  }
  .sel-item {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .sel-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #2563eb;
  }
  .sel-text {
    font-weight: 800;
    font-size: 12px;
  }
  
  .empty {
    padding: 16px;
    border: 1px dashed #e5e7eb;
    border-radius: 14px;
    color: #6b7280;
    background: #fafafa;
  }
  .empty.small {
    padding: 12px;
  }
  .inline {
    border: none;
    background: transparent;
    color: #2563eb;
    font-weight: 900;
    cursor: pointer;
    padding: 0 2px;
  }
  .hint {
    margin-top: 10px;
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
  
  @media (max-width: 980px) {
    .filters {
      grid-template-columns: 1fr;
    }
    .thead,
    .trow {
      grid-template-columns: 44px 1fr 90px 110px 120px 180px;
    }
    .grid {
      grid-template-columns: 1fr;
    }
  }
  @media (max-width: 720px) {
    .app {
      grid-template-columns: 62px 1fr;
    }
    .thead {
      display: none;
    }
    .trow {
      grid-template-columns: 44px 1fr;
      gap: 8px;
    }
    .td.meta,
    .td.actions {
      grid-column: 2 / 3;
    }
    .td.actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }
  }
  </style>
  