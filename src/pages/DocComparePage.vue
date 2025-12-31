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

          <button class="sb-item" @click="go('profile')">
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
        <!-- Topbar -->
        <header class="topbar">
          <div class="tb-left">
            <div class="tb-title">
              <span class="tb-title-strong">문서 비교 · 이해</span>
              <span class="tb-sub">· ID: {{ docId }}</span>
            </div>
  
            <div class="tb-meta">
              <span class="pill">{{ docMeta.type }}</span>
              <span class="muted">·</span>
              <span class="muted">{{ docMeta.title }}</span>
            </div>
          </div>
  
          <div class="tb-right">
            <label class="toggle">
              <input type="checkbox" v-model="syncScroll" />
              <span>동기 스크롤</span>
            </label>
  
            <button class="btn btn-outline" type="button" @click="downloadMock">내보내기</button>
            <button class="btn btn-primary" type="button" @click="reAnalyzeMock">재분석</button>
          </div>
        </header>
  
        <!-- Content -->
        <main class="content">
          <!-- Summary / Terms -->
          <section class="strip">
            <div class="strip-card">
              <div class="strip-title">핵심 요약</div>
              <div class="strip-body">
                {{ analysis.summary }}
              </div>
            </div>
  
            <div class="strip-card">
              <div class="strip-title">핵심 용어</div>
              <div class="chips">
                <button
                  v-for="t in analysis.terms"
                  :key="t.term"
                  class="chip"
                  type="button"
                  @click="openTerm(t)"
                >
                  {{ t.term }}
                </button>
              </div>
            </div>
          </section>
  
          <!-- Compare -->
          <section class="compare">
            <!-- Left: Original -->
            <article class="panel">
              <div class="panel-head">
                <div class="panel-title">원문(Original)</div>
                <div class="panel-actions">
                  <button class="icon-btn" type="button" title="폰트 -" @click="fontDown">A-</button>
                  <button class="icon-btn" type="button" title="폰트 +" @click="fontUp">A+</button>
                </div>
              </div>
  
              <div
                ref="leftRef"
                class="panel-body"
                :style="{ fontSize: fontSize + 'px' }"
                @scroll="onScroll('left')"
                @mousemove="onMouseMove"
                @mouseleave="hideTooltip"
                @click="onHighlightClick"
              >
                <div v-for="(p, i) in originalParagraphs" :key="'o' + i" class="para">
                  <div class="para-no">{{ i + 1 }}</div>
                  <div class="para-text" v-html="highlightTerms(p)"></div>
                </div>
              </div>
            </article>
  
            <!-- Right: Assisted -->
            <article class="panel">
              <div class="panel-head">
                <div class="panel-title">이해 보조(Assisted)</div>
                <div class="panel-actions">
                  <button
                    class="icon-btn"
                    type="button"
                    :class="{ on: viewMode === 'para' }"
                    @click="viewMode = 'para'"
                  >
                    문단
                  </button>
                  <button
                    class="icon-btn"
                    type="button"
                    :class="{ on: viewMode === 'rules' }"
                    @click="viewMode = 'rules'"
                  >
                    조건
                  </button>
                </div>
              </div>
  
              <div
                ref="rightRef"
                class="panel-body"
                :style="{ fontSize: fontSize + 'px' }"
                @scroll="onScroll('right')"
              >
                <template v-if="viewMode === 'para'">
                  <div v-for="(p, i) in assistedParagraphs" :key="'a' + i" class="para">
                    <div class="para-no">{{ i + 1 }}</div>
                    <div class="para-text">
                      <div class="assist-block">
                        <div class="assist-label">쉬운 설명</div>
                        <div class="assist-main">{{ p.easy }}</div>
                      </div>
  
                      <div class="assist-block">
                        <div class="assist-label">핵심 포인트</div>
                        <ul class="assist-list">
                          <li v-for="(b, idx) in p.bullets" :key="'b' + i + '_' + idx">{{ b }}</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </template>
  
                <template v-else>
                  <div class="rules">
                    <div v-for="(r, i) in analysis.rules" :key="'r' + i" class="rule">
                      <div class="rule-title">{{ r.title }}</div>
                      <div class="rule-body">{{ r.desc }}</div>
                      <div class="rule-tag">근거: {{ r.source }}</div>
                    </div>
                  </div>
                </template>
              </div>
            </article>
          </section>
  
          <!-- Q&A -->
          <section class="qa">
            <div class="qa-head">
              <div>
                <div class="qa-title">문서 기반 Q&A</div>
                <div class="qa-sub muted">문서 내용 근거로 답변을 생성합니다.</div>
              </div>
  
              <div class="qa-actions">
                <button class="btn btn-outline" type="button" @click="seedQuestions">추천 질문</button>
                <button class="btn btn-ghost" type="button" @click="clearChat">지우기</button>
              </div>
            </div>
  
            <div class="qa-body" ref="qaBodyRef">
              <div v-if="chat.length === 0" class="empty">
                아래에 질문을 입력해보세요. 예: “보관 기간은 얼마나 되나요?”
              </div>
  
              <div v-else class="chat">
                <div v-for="m in chat" :key="m.id" class="msg" :class="m.role">
                  <div class="bubble">
                    <div class="text">{{ m.text }}</div>
                    <div v-if="m.citePara" class="cite">
                      근거:
                      <button class="cite-btn" type="button" @click="jumpTo(m.citePara)">
                        원문 {{ m.citePara }}번 문단
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
  
            <form class="qa-input" @submit.prevent="ask">
              <input v-model="question" class="input" placeholder="문서에 대해 질문해보세요..." />
              <button class="btn btn-primary" :disabled="!question.trim()">질문</button>
            </form>
          </section>
        </main>
      </div>
  
      <!-- Term Drawer -->
      <div v-if="termOpen" class="drawer-backdrop" @click="termOpen = false"></div>
      <aside v-if="termOpen" class="drawer">
        <div class="drawer-head">
          <div>
            <div class="drawer-title">{{ selectedTerm?.term }}</div>
            <div class="drawer-sub muted">문서 내 전문 용어 설명</div>
          </div>
          <button class="icon-btn" type="button" @click="termOpen = false">닫기</button>
        </div>
  
        <div class="drawer-body">
          <div class="kv">
            <div class="k">정의</div>
            <div class="v">{{ selectedTerm?.definition }}</div>
          </div>
          <div class="kv">
            <div class="k">쉬운 말</div>
            <div class="v">{{ selectedTerm?.plain }}</div>
          </div>
          <div class="kv">
            <div class="k">문서 근거</div>
            <div class="v">
              <button class="cite-btn" type="button" @click="jumpTo(selectedTerm?.para || 1)">
                원문 {{ selectedTerm?.para }}번 문단 보기
              </button>
            </div>
          </div>
  
          <div class="divider"></div>
  
          <div class="drawer-title-sm">관련 문장(예시)</div>
          <div class="quote">
            {{ selectedTerm?.snippet }}
          </div>
        </div>
      </aside>

    <!-- Hover Tooltip -->
      <div
        v-if="hoverTip.visible"
        class="tooltip"
        :style="{ left: hoverTip.x + 'px', top: hoverTip.y + 'px' }"
      >
        <div class="tt-title">{{ hoverTip.term }}</div>
        <div class="tt-body">{{ hoverTip.definition }}</div>
        <div class="tt-hint">클릭하면 상세 보기</div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed, nextTick, onMounted, reactive, ref } from "vue";
  import { useRoute, useRouter } from "vue-router";
  
  type Role = "user" | "assistant";
  
  interface Term {
    term: string;
    definition: string;
    plain: string;
    para: number;
    snippet: string;
  }
  interface AssistedPara {
    easy: string;
    bullets: string[];
  }
  interface RuleItem {
    title: string;
    desc: string;
    source: string;
  }
  interface ChatMsg {
    id: string;
    role: Role;
    text: string;
    citePara?: number;
  }
  
  const router = useRouter();
  const route = useRoute();
  const docId = computed(() => String(route.params.id ?? "unknown"));
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
  
  const leftRef = ref<HTMLDivElement | null>(null);
  const rightRef = ref<HTMLDivElement | null>(null);
  const qaBodyRef = ref<HTMLDivElement | null>(null);
  
  const syncScroll = ref(true);
  const viewMode = ref<"para" | "rules">("para");
  const fontSize = ref(14);
  
  const docMeta = reactive({
    title: "사내 안내문",
    type: "PDF",
  });
  
  const analysis = reactive({
    summary:
      "이 문서는 개인정보 수집 범위, 처리 목적, 보관 기간 및 예외 조건을 안내합니다. 용어 설명과 문단별 핵심 포인트를 통해 사용자가 스스로 정확히 해석하도록 돕습니다.",
    terms: <Term[]>[
      {
        term: "개인정보",
        definition: "개인을 식별하거나 식별할 수 있는 정보(예: 이름, 연락처 등).",
        plain: "사람을 알아볼 수 있게 하는 정보",
        para: 1,
        snippet: "…개인정보는 서비스 제공을 위해 최소한으로 수집됩니다…",
      },
      {
        term: "보관 기간",
        definition: "수집한 정보를 저장해 두는 기간.",
        plain: "정보를 저장해두는 기간",
        para: 2,
        snippet: "…보관 기간은 목적 달성 시까지이며, 법령에 따라 달라질 수 있습니다…",
      },
      {
        term: "제3자 제공",
        definition: "다른 회사/기관에 정보를 전달하는 행위.",
        plain: "다른 곳에 정보를 주는 것",
        para: 3,
        snippet: "…원칙적으로 제3자 제공은 하지 않으며, 예외적으로 동의 시 가능합니다…",
      },
    ],
    rules: <RuleItem[]>[
      { title: "원칙", desc: "필요 최소한의 정보만 수집합니다.", source: "원문 1번 문단" },
      { title: "보관", desc: "목적 달성 시까지 보관하되, 법령이 있으면 해당 기간을 따릅니다.", source: "원문 2번 문단" },
      { title: "제3자 제공", desc: "원칙적으로 제공하지 않으며, 동의 또는 법령 근거가 있을 때만 제공합니다.", source: "원문 3번 문단" },
    ],
  });
  
  const originalParagraphs = ref<string[]>([
    "본 안내문은 서비스 제공을 위하여 개인정보를 수집·이용하는 범위와 목적을 설명합니다. 개인정보는 서비스 제공을 위해 필요한 최소 범위로 수집됩니다.",
    "수집된 정보의 보관 기간은 수집·이용 목적 달성 시까지이며, 관계 법령에 따라 보존이 필요한 경우 해당 법령에서 정한 기간 동안 보관합니다.",
    "회사는 원칙적으로 이용자의 개인정보를 제3자에게 제공하지 않습니다. 다만 이용자 동의가 있거나 법령에 근거한 경우 예외적으로 제공될 수 있습니다.",
    "이용자는 개인정보 처리에 관한 문의를 담당 부서로 요청할 수 있으며, 필요한 경우 열람·정정·삭제를 요구할 수 있습니다.",
  ]);
  
  const assistedParagraphs = ref<AssistedPara[]>([
    { easy: "이 문서는 서비스를 제공하기 위해 어떤 개인정보를 왜 받는지 알려줍니다.", bullets: ["필요한 정보만 최소한으로 수집", "수집 목적을 문서로 안내"] },
    { easy: "정보는 목적이 끝날 때까지 보관하지만, 법에 정해진 기간이 있으면 그 기간을 따릅니다.", bullets: ["기본: 목적 달성 시까지", "예외: 법령 보존 의무 시 법정 기간"] },
    { easy: "원칙적으로 다른 회사에 정보를 주지 않지만, 동의하거나 법이 요구하면 줄 수 있습니다.", bullets: ["기본: 제3자 제공 없음", "예외: 동의/법령 근거"] },
    { easy: "궁금한 점은 문의할 수 있고, 내 정보를 확인하거나 수정/삭제를 요청할 수 있습니다.", bullets: ["문의 가능", "열람/정정/삭제 요청 가능"] },
  ]);
  
  function go(name: string) {
    router.push({ name }).catch(() => {});
  }
  
  /** ===== Highlight 처리 ===== */
  function escapeRegExp(s: string) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }
  
  function highlightTerms(text: string) {
    let out = text;
    for (const t of analysis.terms) {
      const safe = escapeRegExp(t.term);
      const re = new RegExp(`(${safe})`, "g");
      out = out.replace(re, `<span class="hl" data-term="${t.term}">$1</span>`);
    }
    return out;
  }
  
  /** ===== Tooltip (hover) ===== */
  const hoverTip = reactive({
    visible: false,
    term: "",
    definition: "",
    x: 0,
    y: 0,
  });
  
  function hideTooltip() {
    hoverTip.visible = false;
  }
  
  function onMouseMove(e: MouseEvent) {
    const t = e.target as HTMLElement | null;
    if (!t || !t.classList.contains("hl")) {
      hideTooltip();
      return;
    }
    const termName = t.getAttribute("data-term");
    const found = analysis.terms.find((x) => x.term === termName);
    if (!found) return;
  
    hoverTip.term = found.term;
    hoverTip.definition = found.definition;
    hoverTip.visible = true;
    hoverTip.x = Math.min(e.clientX + 14, window.innerWidth - 260);
    hoverTip.y = Math.min(e.clientY + 14, window.innerHeight - 140);
  }
  
  const termOpen = ref(false);
  const selectedTerm = ref<Term | null>(null);
  
  function openTerm(t: Term) {
    selectedTerm.value = t;
    termOpen.value = true;
    hideTooltip();
  }
  
  function onHighlightClick(e: MouseEvent) {
    const t = e.target as HTMLElement | null;
    if (!t || !t.classList.contains("hl")) return;
    const termName = t.getAttribute("data-term");
    const found = analysis.terms.find((x) => x.term === termName);
    if (!found) return;
    openTerm(found);
  }
  
  /** ===== Scroll sync ===== */
  let lockSide: "left" | "right" | null = null;
  
  function onScroll(side: "left" | "right") {
    if (!syncScroll.value) return;
    if (lockSide && lockSide !== side) return;
  
    const src = side === "left" ? leftRef.value : rightRef.value;
    const dst = side === "left" ? rightRef.value : leftRef.value;
    if (!src || !dst) return;
  
    lockSide = side;
    const ratio = src.scrollTop / Math.max(1, src.scrollHeight - src.clientHeight);
    dst.scrollTop = ratio * (dst.scrollHeight - dst.clientHeight);
  
    window.setTimeout(() => {
      lockSide = null;
    }, 0);
  }
  
  /** ===== Q&A ===== */
  const chat = ref<ChatMsg[]>([]);
  const question = ref("");
  
  function seedQuestions() {
    const seeds = ["개인정보를 왜 수집하나요?", "보관 기간은 얼마나 되나요?", "제3자 제공은 언제 가능한가요?"];
    question.value = seeds[Math.floor(Math.random() * seeds.length)];
  }
  
  function clearChat() {
    chat.value = [];
    question.value = "";
  }
  
  function cryptoId() {
    return Math.random().toString(16).slice(2) + Date.now().toString(16);
  }
  
  function mockAnswer(q: string): ChatMsg {
    const s = q.toLowerCase();
    if (s.includes("보관") || s.includes("기간")) {
      return {
        id: cryptoId(),
        role: "assistant",
        text: "보관 기간은 기본적으로 ‘목적 달성 시까지’이며, 법령상 보존 의무가 있으면 법에서 정한 기간을 따릅니다.",
        citePara: 2,
      };
    }
    if (s.includes("제3자") || s.includes("제삼자")) {
      return {
        id: cryptoId(),
        role: "assistant",
        text: "원칙적으로 제3자 제공은 하지 않지만, 이용자 동의가 있거나 법령 근거가 있을 때 예외적으로 제공될 수 있습니다.",
        citePara: 3,
      };
    }
    return {
      id: cryptoId(),
      role: "assistant",
      text: "개인정보는 서비스 제공에 필요한 범위로 최소한 수집되며, 수집 목적과 범위를 문서로 안내합니다.",
      citePara: 1,
    };
  }
  
  async function ask() {
    const q = question.value.trim();
    if (!q) return;
  
    chat.value.push({ id: cryptoId(), role: "user", text: q });
    chat.value.push(mockAnswer(q));
    question.value = "";
  
    await nextTick();
    qaBodyRef.value?.scrollTo({ top: qaBodyRef.value.scrollHeight, behavior: "smooth" });
  }
  
  /** ===== Jump ===== */
  async function jumpTo(paraNo: number) {
    const el = leftRef.value;
    if (!el) return;
  
    await nextTick();
    const paraHeight = 140; //  추정값
    el.scrollTo({ top: Math.max(0, (paraNo - 1) * paraHeight), behavior: "smooth" });
  }
  
  /** ===== UI actions ===== */
  function fontUp() {
    fontSize.value = Math.min(18, fontSize.value + 1);
  }
  function fontDown() {
    fontSize.value = Math.max(12, fontSize.value - 1);
  }
  function downloadMock() {
    alert("내보내기: PDF/리포트로 내보내기 예정");
  }
  function reAnalyzeMock() {
    alert("재분석: FastAPI 분석 파이프라인 호출 예정");
  }
  </script>
  
  <style scoped>
  :global(:root) {
    --b1: #1d4ed8;
    --b2: #0ea5e9;
    --ring: rgba(29, 78, 216, 0.18);
  }

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
    font-weight: 1100;
    font-size: 16px;
    letter-spacing: -0.2px;
  }
  .tb-sub {
    color: #6b7280;
    font-size: 12px;
    font-weight: 700;
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
  .toggle {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: #374151;
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
  
  /* Summary strip */
  .strip {
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 12px;
  }
  .strip-card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 14px 16px;
  }
  .strip-title { font-weight: 900; margin-bottom: 8px; }
  .strip-body { color: #374151; line-height: 1.6; font-size: 13px; }
  .chips { display: flex; gap: 8px; flex-wrap: wrap; }
  .chip {
    border: 1px solid #e5e7eb;
    background: #f9fafb;
    padding: 6px 10px;
    border-radius: 999px;
    font-weight: 900;
    font-size: 12px;
    cursor: pointer;
  }
  .chip:hover { background: #eff6ff; border-color: #dbeafe; }
  
  /* Compare */
  .compare {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
  .panel {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    overflow: hidden;
    display: grid;
    grid-template-rows: 52px 1fr;
    min-height: 520px;
  }
  .panel-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 14px;
    border-bottom: 1px solid #eef2f7;
    background: #fff;
  }
  .panel-title { font-weight: 900; }
  .panel-actions { display: flex; gap: 8px; }
  .icon-btn {
    border: 1px solid #e5e7eb;
    background: #fff;
    padding: 6px 10px;
    border-radius: 12px;
    font-weight: 900;
    font-size: 12px;
    cursor: pointer;
  }
  .icon-btn:hover { background: #f9fafb; }
  .icon-btn.on { background: #eff6ff; border-color: #dbeafe; }
  
  .panel-body {
    padding: 14px;
    overflow: auto;
    background: #fbfcff;
  }
  .para {
    display: grid;
    grid-template-columns: 32px 1fr;
    gap: 10px;
    padding: 12px;
    border: 1px solid #eef2f7;
    border-radius: 14px;
    background: #fff;
    margin-bottom: 10px;
  }
  .para-no {
    width: 32px; height: 32px;
    border-radius: 12px;
    display: grid; place-items: center;
    background: #f1f5f9;
    font-weight: 900;
    color: #334155;
    font-size: 12px;
  }
  .para-text { line-height: 1.7; color: #111827; }
  :deep(.hl) {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    padding: 0 4px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 900;
  }
  
  .assist-block { margin-bottom: 10px; }
  .assist-label { font-size: 12px; color: #6b7280; font-weight: 900; margin-bottom: 6px; }
  .assist-main { font-weight: 700; color: #111827; }
  .assist-list { margin: 6px 0 0; padding-left: 18px; color: #374151; }
  .assist-list li { margin: 4px 0; }
  
  .rules { display: grid; gap: 10px; }
  .rule {
    border: 1px solid #eef2f7;
    border-radius: 14px;
    background: #fff;
    padding: 12px;
  }
  .rule-title { font-weight: 900; margin-bottom: 6px; }
  .rule-body { color: #374151; line-height: 1.6; font-size: 13px; }
  .rule-tag {
    margin-top: 8px;
    display: inline-block;
    font-size: 12px;
    color: #1d4ed8;
    background: #eff6ff;
    border: 1px solid #dbeafe;
    padding: 2px 8px;
    border-radius: 999px;
    font-weight: 900;
  }
  
  /* Q&A */
  .qa {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    overflow: hidden;
    display: grid;
    grid-template-rows: auto 1fr auto;
    min-height: 360px;
  }
  .qa-head {
    padding: 14px 16px;
    border-bottom: 1px solid #eef2f7;
    display: flex;
    justify-content: space-between;
    gap: 12px;
    align-items: center;
  }
  .qa-title { font-weight: 900; }
  .qa-actions { display: flex; gap: 10px; flex-wrap: wrap; }
  .qa-body {
    padding: 14px 16px;
    background: #fbfcff;
    overflow: auto;
  }
  .empty {
    padding: 14px;
    border: 1px dashed #e5e7eb;
    border-radius: 14px;
    color: #6b7280;
    background: #fff;
  }
  .chat { display: grid; gap: 10px; }
  .msg { display: flex; }
  .msg.user { justify-content: flex-end; }
  .msg.assistant { justify-content: flex-start; }
  .bubble {
    max-width: 78%;
    padding: 10px 12px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    background: #fff;
  }
  .msg.user .bubble {
    background: #2563eb;
    border-color: #2563eb;
    color: #fff;
  }
  .text { line-height: 1.6; font-size: 13px; }
  .cite { margin-top: 8px; font-size: 12px; }
  .cite-btn {
    border: none;
    background: transparent;
    color: #1d4ed8;
    font-weight: 900;
    cursor: pointer;
    text-decoration: underline;
  }
  
  .qa-input {
    padding: 12px 14px;
    border-top: 1px solid #eef2f7;
    background: #fff;
    display: flex;
    gap: 10px;
  }
  .input {
    flex: 1;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 10px 12px;
    outline: none;
  }
  .input:focus {
    border-color: #93c5fd;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15);
  }
  
  /* Buttons */
  .btn {
    border: 1px solid #e5e7eb;
    background: #fff;
    padding: 10px 14px;
    border-radius: 12px;
    font-weight: 900;
    cursor: pointer;
  }
  .btn:hover { background: #f9fafb; }
  .btn-primary { background: #2563eb; border-color: #2563eb; color: #fff; }
  .btn-primary:hover { background: #1d4ed8; }
  .btn-outline { border-color: #cbd5e1; }
  .btn-ghost { border-color: transparent; }
  
  /* Drawer */
  .drawer-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(15, 23, 42, 0.35);
    z-index: 40;
  }
  .drawer {
    position: fixed;
    right: 0;
    top: 0;
    width: 360px;
    height: 100vh;
    background: #fff;
    border-left: 1px solid #e5e7eb;
    z-index: 50;
    display: grid;
    grid-template-rows: auto 1fr;
  }
  .drawer-head {
    padding: 14px;
    border-bottom: 1px solid #eef2f7;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .drawer-title { font-weight: 900; font-size: 16px; }
  .drawer-body { padding: 14px; overflow: auto; }
  .drawer-title-sm { font-weight: 900; margin-bottom: 8px; }
  .kv { display: grid; gap: 6px; margin-bottom: 12px; }
  .k { font-size: 12px; color: #6b7280; font-weight: 900; }
  .v { color: #111827; line-height: 1.6; font-size: 13px; }
  .divider { height: 1px; background: #eef2f7; margin: 14px 0; }
  .quote {
    border: 1px solid #eef2f7;
    background: #fbfcff;
    border-radius: 14px;
    padding: 12px;
    color: #374151;
    line-height: 1.6;
    font-size: 13px;
  }
  
  /* Tooltip */
  .tooltip {
    position: fixed;
    width: 240px;
    background: #111827;
    color: #fff;
    border-radius: 14px;
    padding: 10px 12px;
    z-index: 60;
    box-shadow: 0 16px 36px rgba(0,0,0,0.25);
  }
  .tt-title { font-weight: 900; margin-bottom: 6px; }
  .tt-body { font-size: 12px; line-height: 1.5; opacity: 0.95; }
  .tt-hint { font-size: 11px; opacity: 0.75; margin-top: 8px; }
  
  /* Responsive */
  @media (max-width: 980px) {
    .strip { grid-template-columns: 1fr; }
    .compare { grid-template-columns: 1fr; }
    .drawer { width: min(92vw, 380px); }
  }
  </style>
  













