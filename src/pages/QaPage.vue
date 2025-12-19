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
          <button class="sb-item active" title="Q&A">💬</button>
          <button class="sb-item" title="용어집" @click="go('terms')">📚</button>
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
              <span class="tb-title-strong">문서 Q&A</span>
              <span class="tb-sub">· 근거 기반으로 답변을 확인하세요</span>
            </div>
  
            <div class="tb-meta">
              <span class="pill">선택 문서: {{ selectedDoc ? selectedDoc.title : "없음" }}</span>
              <span class="muted">·</span>
              <span class="muted">{{ selectedDoc ? selectedDoc.type : "—" }}</span>
            </div>
          </div>
  
          <div class="tb-right">
            <button class="btn btn-outline" type="button" @click="newChat">새 대화</button>
            <button class="btn btn-primary" type="button" @click="go('upload')">+ 새 문서 업로드</button>
          </div>
        </header>
  
        <main class="content">
          <!-- 3-column layout -->
          <section class="grid">
            <!-- Left: Document picker + prompt shortcuts -->
            <aside class="card left">
              <div class="card-head">
                <h2>문서 선택</h2>
              </div>
  
              <div class="doc-picker">
                <select class="select" v-model="selectedDocId">
                  <option value="">문서를 선택하세요</option>
                  <option v-for="d in docs" :key="d.id" :value="d.id">
                    {{ d.title }}
                  </option>
                </select>
  
                <div v-if="selectedDoc" class="doc-meta">
                  <div class="row">
                    <span class="chip">{{ selectedDoc.type }}</span>
                    <span class="muted">·</span>
                    <span class="muted">ID: {{ selectedDoc.id }}</span>
                  </div>
                  <div class="muted small">
                    (데모) FastAPI 연동 시: 문서 요약/용어/섹션을 여기서 불러올 수 있어요.
                  </div>
  
                  <div class="quick">
                    <button class="quick-item" type="button" @click="usePrompt('요약해줘')">요약</button>
                    <button class="quick-item" type="button" @click="usePrompt('핵심 용어 10개 뽑아줘')">용어</button>
                    <button class="quick-item" type="button" @click="usePrompt('중요한 조항/규정만 뽑아줘')">조항</button>
                    <button class="quick-item" type="button" @click="usePrompt('주의해야 할 부분(리스크) 알려줘')">리스크</button>
                  </div>
                </div>
  
                <div v-else class="empty">
                  먼저 문서를 선택해야 질문할 수 있어요.
                </div>
              </div>
  
              <div class="sep"></div>
  
              <div class="card-head">
                <h2>대화 설정</h2>
              </div>
  
              <div class="settings">
                <label class="setting">
                  <span class="label">답변 스타일</span>
                  <select class="select" v-model="answerStyle">
                    <option value="concise">짧게(핵심)</option>
                    <option value="balanced">보통</option>
                    <option value="detailed">자세히</option>
                  </select>
                </label>
  
                <label class="setting">
                  <span class="label">근거 표시</span>
                  <select class="select" v-model="citeMode">
                    <option value="top">상단에 요약 근거</option>
                    <option value="inline">문장별 근거(요약)</option>
                  </select>
                </label>
  
                <label class="check">
                  <input type="checkbox" v-model="highlightEvidence" />
                  <span>근거 문단 하이라이트(데모)</span>
                </label>
              </div>
            </aside>
  
            <!-- Center: Chat -->
            <section class="card center">
              <div class="card-head">
                <h2>대화</h2>
                <div class="head-actions">
                  <span class="muted small">메시지 {{ messages.length }}개</span>
                </div>
              </div>
  
              <div class="chat" ref="chatRef">
                <div v-if="messages.length === 0" class="empty big">
                  <div class="big-title">문서 기반 질문을 시작해보세요</div>
                  <div class="muted">
                    왼쪽에서 문서를 선택한 뒤, 아래 입력창에 질문을 적으면 돼요.
                  </div>
                </div>
  
                <div v-else class="msgs">
                  <div
                    v-for="m in messages"
                    :key="m.id"
                    class="msg"
                    :class="m.role"
                  >
                    <div class="bubble">
                      <div class="meta">
                        <span class="who">{{ m.role === 'user' ? '나' : 'DocAssist' }}</span>
                        <span class="muted">·</span>
                        <span class="muted">{{ formatTime(m.at) }}</span>
                      </div>
  
                      <div class="text">
                        <p v-for="(line, idx) in m.text.split('\n')" :key="idx">{{ line }}</p>
                      </div>
  
                      <div v-if="m.role === 'assistant' && m.citations?.length" class="cite">
                        <div class="cite-title">
                          {{ citeMode === 'top' ? "근거(요약)" : "근거(인라인 요약)" }}
                        </div>
                        <div class="cite-chips">
                          <button
                            v-for="c in m.citations"
                            :key="c.citeId"
                            class="cite-chip"
                            type="button"
                            @click="selectEvidence(c)"
                          >
                            §{{ c.section }} · p{{ c.page }} · {{ c.score }}%
                          </button>
                        </div>
                      </div>
  
                      <div v-if="m.role === 'assistant'" class="assist-actions">
                        <button class="link" type="button" @click="copyText(m.text)">답변 복사</button>
                        <button class="link" type="button" @click="pinAnswer(m.id)">핀</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
  
              <!-- Composer -->
              <form class="composer" @submit.prevent="send">
                <input
                  v-model="input"
                  class="input"
                  placeholder="예) 이 문서에서 ‘보유기간’은 얼마나야?"
                  :disabled="sending"
                  @keydown.enter.exact.prevent="send"
                />
                <button class="btn btn-primary" type="submit" :disabled="sending || !input.trim() || !selectedDocId">
                  {{ sending ? "전송..." : "전송" }}
                </button>
              </form>
  
              <div v-if="!selectedDocId" class="hint muted">
                ※ 문서를 선택해야 전송 버튼이 활성화돼요.
              </div>
            </section>
  
            <!-- Right: Evidence panel -->
            <aside class="card right">
              <div class="card-head">
                <h2>근거 패널</h2>
                <div class="head-actions">
                  <button class="btn btn-outline btn-sm" type="button" @click="clearEvidence" :disabled="!activeEvidence">
                    해제
                  </button>
                </div>
              </div>
  
              <div v-if="!activeEvidence" class="empty">
                답변 아래의 근거 칩(§/p)을 클릭하면<br />
                해당 문단 근거를 여기에서 볼 수 있어요.
              </div>
  
              <div v-else class="evidence">
                <div class="ev-head">
                  <div class="ev-title">섹션 §{{ activeEvidence.section }}</div>
                  <div class="muted small">
                    page {{ activeEvidence.page }} · score {{ activeEvidence.score }}%
                  </div>
                </div>
  
                <div class="ev-body" :class="{ hl: highlightEvidence }">
                  {{ activeEvidence.quote }}
                </div>
  
                <div class="ev-actions">
                  <button class="btn btn-outline btn-sm" type="button" @click="copyText(activeEvidence.quote)">
                    근거 복사
                  </button>
                  <button class="btn btn-sm" type="button" @click="openDocFromEvidence">
                    문서에서 보기
                  </button>
                </div>
  
                <div class="ev-note muted">
                  (데모) 실제 구현 시: DocComparePage에서 해당 페이지/문단으로 스크롤 이동까지 연결 가능
                </div>
              </div>
  
              <div class="sep"></div>
  
              <div class="card-head">
                <h2>핀된 답변</h2>
              </div>
  
              <div v-if="pinned.length === 0" class="empty small">
                핀이 아직 없어요.
              </div>
  
              <ul v-else class="pin-list">
                <li v-for="p in pinned" :key="p.id" class="pin-item">
                  <div class="pin-text">{{ p.text }}</div>
                  <button class="link" type="button" @click="removePin(p.id)">삭제</button>
                </li>
              </ul>
            </aside>
          </section>
  
          <div v-if="toast" class="toast">{{ toast }}</div>
        </main>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { computed, nextTick, onMounted, ref, watch } from "vue";
  import { useRouter } from "vue-router";
  
  type DocType = "PDF" | "JPG" | "PNG";
  interface DocItem {
    id: string;
    title: string;
    type: DocType;
  }
  
  interface Citation {
    citeId: string;
    section: string; // e.g., "2.1"
    page: number;
    score: number; // 0~100
    quote: string;
  }
  
  type Role = "user" | "assistant";
  interface ChatMsg {
    id: string;
    role: Role;
    text: string;
    at: string; // ISO
    citations?: Citation[];
  }
  
  interface PinItem {
    id: string;
    text: string;
  }
  
  const router = useRouter();
  
  /** Mock docs (Drive에서 가져오는 걸로 나중에 교체) */
  const docs = ref<DocItem[]>([
    { id: "doc_001", title: "사내 보안 정책 개정 안내", type: "PDF" },
    { id: "doc_004", title: "사내 출장 정산 가이드", type: "PDF" },
    { id: "doc_007", title: "개인정보 처리방침 변경 공지", type: "PDF" },
  ]);
  
  const selectedDocId = ref<string>("");
  const selectedDoc = computed(() => docs.value.find((d) => d.id === selectedDocId.value) ?? null);
  
  const answerStyle = ref<"concise" | "balanced" | "detailed">("balanced");
  const citeMode = ref<"top" | "inline">("top");
  const highlightEvidence = ref(true);
  
  const input = ref("");
  const messages = ref<ChatMsg[]>([]);
  const sending = ref(false);
  
  const activeEvidence = ref<Citation | null>(null);
  const pinned = ref<PinItem[]>([]);
  
  const chatRef = ref<HTMLElement | null>(null);
  
  const toast = ref("");
  let toastTimer: number | undefined;
  
  function showToast(msg: string) {
    toast.value = msg;
    if (toastTimer) window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => (toast.value = ""), 1800);
  }
  
  function go(name: string) {
    router.push({ name }).catch(() => {});
  }
  
  function openLastDoc() {
    router.push({ name: "documentView", params: { id: "doc_001" } }).catch(() => {});
  }
  
  function newChat() {
    messages.value = [];
    activeEvidence.value = null;
    input.value = "";
    showToast("새 대화를 시작했어요");
  }
  
  function formatTime(iso: string) {
    const d = new Date(iso);
    return d.toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit" });
  }
  
  async function copyText(text: string) {
    try {
      await navigator.clipboard.writeText(text);
      showToast("복사 완료");
    } catch {
      showToast("복사 실패(권한/브라우저 설정 확인)");
    }
  }
  
  function pinAnswer(msgId: string) {
    const msg = messages.value.find((m) => m.id === msgId);
    if (!msg) return;
    const short = msg.text.length > 80 ? msg.text.slice(0, 80) + "…" : msg.text;
    pinned.value = [{ id: `${msgId}_${Date.now()}`, text: short }, ...pinned.value].slice(0, 8);
    showToast("핀에 저장했어요");
  }
  
  function removePin(id: string) {
    pinned.value = pinned.value.filter((p) => p.id !== id);
  }
  
  function clearEvidence() {
    activeEvidence.value = null;
  }
  
  function selectEvidence(c: Citation) {
    activeEvidence.value = c;
  }
  
  function openDocFromEvidence() {
    const docId = selectedDocId.value;
    if (!docId) return;
    router.push({ name: "documentView", params: { id: docId } }).catch(() => {});
  }
  
  function usePrompt(text: string) {
    input.value = text;
  }
  
  function buildDemoAnswer(question: string): { answer: string; citations: Citation[] } {
    // 문서별로 다른 데모 근거/답변 제공
    const docId = selectedDocId.value;
  
    const base: Citation[] = [
      {
        citeId: "c1",
        section: "2.1",
        page: 3,
        score: 92,
        quote: "…중요 정보 자산에 대한 접근 권한은 업무 필요 최소 범위로 부여하며, 정기적으로 검토한다…",
      },
      {
        citeId: "c2",
        section: "3.2",
        page: 5,
        score: 86,
        quote: "…권한 승인 없이 시스템에 접근하거나 정보 자산을 반출하는 행위를 금지한다…",
      },
    ];
  
    const privacy: Citation[] = [
      {
        citeId: "c3",
        section: "1.3",
        page: 2,
        score: 90,
        quote: "…개인정보의 처리 목적 달성 또는 보유기간 경과 시 지체 없이 파기한다…",
      },
      {
        citeId: "c4",
        section: "2.4",
        page: 4,
        score: 81,
        quote: "…개인정보는 수집·이용 목적 범위 내에서만 처리하며, 목적 외 이용·제공을 제한한다…",
      },
    ];
  
    const travel: Citation[] = [
      {
        citeId: "c5",
        section: "4.1",
        page: 6,
        score: 88,
        quote: "…정산 시 증빙 서류(영수증/내역서)를 필수로 첨부하며, 누락 시 지급이 보류될 수 있다…",
      },
      {
        citeId: "c6",
        section: "4.3",
        page: 7,
        score: 79,
        quote: "…비용 항목별 상한 및 승인 절차는 사내 규정에 따른다…",
      },
    ];
  
    let citations = base;
    if (docId === "doc_007") citations = privacy;
    if (docId === "doc_004") citations = travel;
  
    const style = answerStyle.value;
    const prefix =
      style === "concise"
        ? "핵심만 정리하면:\n"
        : style === "detailed"
        ? "문서 근거를 바탕으로 자세히 설명하면:\n"
        : "정리하면:\n";
  
    const answer =
      prefix +
      `질문: ${question}\n\n` +
      (style === "concise"
        ? "- 결론: 문서 기준으로 해당 항목은 규정/절차에 따라 처리됩니다.\n- 필요한 조치: 관련 조항(근거) 확인 후 진행하세요."
        : style === "detailed"
        ? "1) 문서에서 관련 조항을 먼저 확인하고,\n2) 예외/승인 조건이 있으면 승인 흐름을 따라가며,\n3) 증빙/로그가 필요한 경우 사후 감사 대비용으로 보관하는 것이 안전합니다.\n\n아래 근거 문단을 확인하면 핵심 표현을 그대로 볼 수 있어요."
        : "관련 조항을 기준으로 처리 범위를 확인한 뒤, 필요한 승인/증빙이 있는지 체크하면 돼요.\n아래 근거 문단을 확인해보세요.");
  
    return { answer, citations };
  }
  
  async function send() {
    if (!selectedDocId.value) {
      showToast("문서를 먼저 선택해줘!");
      return;
    }
    const q = input.value.trim();
    if (!q) return;
  
    sending.value = true;
  
    const userMsg: ChatMsg = {
      id: `u_${Date.now()}`,
      role: "user",
      text: q,
      at: new Date().toISOString(),
    };
    messages.value = [...messages.value, userMsg];
    input.value = "";
  
    await nextTick();
    scrollToBottom();
  
    // TODO: FastAPI 연동 (예시)
    // POST /qa/ask { doc_id, question, style, cite_mode }
    // => { answer, citations: [{section,page,score,quote}] }
  
    await new Promise((r) => setTimeout(r, 650)); // demo latency
    const demo = buildDemoAnswer(q);
  
    const botMsg: ChatMsg = {
      id: `a_${Date.now()}`,
      role: "assistant",
      text: demo.answer,
      at: new Date().toISOString(),
      citations: demo.citations,
    };
    messages.value = [...messages.value, botMsg];
  
    // 첫 답변이면 자동으로 1번 근거 선택
    if (demo.citations.length) activeEvidence.value = demo.citations[0];
  
    sending.value = false;
    await nextTick();
    scrollToBottom();
  }
  
  function scrollToBottom() {
    const el = chatRef.value;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
  }
  
  onMounted(() => {
    // 데모: 문서 하나 미리 선택해두고 싶으면 주석 해제
    // selectedDocId.value = "doc_001";
  });
  
  watch(selectedDocId, () => {
    // 문서 바뀌면 근거 패널 초기화 + 새 대화 유도
    activeEvidence.value = null;
    if (messages.value.length > 0) {
      showToast("문서를 변경했어요. 필요하면 새 대화를 시작해줘!");
    }
  });
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
  .small {
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
    max-width: 1400px;
    margin: 0 auto;
    padding: 16px 18px 44px;
    display: grid;
    gap: 14px;
  }
  
  /* Grid */
  .grid {
    display: grid;
    grid-template-columns: 340px 1fr 360px;
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
  
  .sep {
    height: 1px;
    background: #eef2f7;
    margin: 14px 0;
  }
  
  .empty {
    padding: 14px;
    border: 1px dashed #e5e7eb;
    border-radius: 14px;
    color: #6b7280;
    background: #fafafa;
  }
  .empty.big {
    padding: 20px;
  }
  .big-title {
    font-weight: 900;
    font-size: 16px;
    margin-bottom: 8px;
  }
  
  /* Left */
  .doc-picker {
    display: grid;
    gap: 10px;
  }
  .select {
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 10px 12px;
    background: #fff;
    font-weight: 800;
    width: 100%;
  }
  .doc-meta .row {
    display: flex;
    gap: 8px;
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
  .quick {
    margin-top: 10px;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }
  .quick-item {
    border: 1px solid #e5e7eb;
    background: #fff;
    border-radius: 12px;
    padding: 10px;
    font-weight: 900;
    cursor: pointer;
  }
  .quick-item:hover {
    background: #f9fafb;
  }
  .settings {
    display: grid;
    gap: 12px;
  }
  .setting {
    display: grid;
    gap: 6px;
  }
  .label {
    font-weight: 900;
    font-size: 12px;
  }
  .check {
    display: flex;
    gap: 8px;
    align-items: center;
    font-size: 12px;
    font-weight: 800;
    color: #374151;
  }
  
  /* Center chat */
  .chat {
    height: calc(100vh - 76px - 16px - 16px - 120px);
    min-height: 360px;
    overflow: auto;
    border: 1px solid #eef2f7;
    border-radius: 14px;
    padding: 12px;
    background: #fbfcff;
  }
  .msgs {
    display: grid;
    gap: 10px;
  }
  .msg {
    display: flex;
  }
  .msg.user {
    justify-content: flex-end;
  }
  .msg.assistant {
    justify-content: flex-start;
  }
  .bubble {
    max-width: 78%;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    background: #fff;
    padding: 10px 12px;
  }
  .msg.user .bubble {
    background: #eff6ff;
    border-color: #bfdbfe;
  }
  .meta {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
  }
  .who {
    font-weight: 900;
    font-size: 12px;
  }
  .text p {
    margin: 0;
    line-height: 1.6;
    font-weight: 700;
    color: #374151;
  }
  .text p + p {
    margin-top: 6px;
  }
  
  .cite {
    margin-top: 10px;
    border-top: 1px dashed #e5e7eb;
    padding-top: 10px;
  }
  .cite-title {
    font-weight: 900;
    font-size: 12px;
    margin-bottom: 8px;
  }
  .cite-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
  .cite-chip {
    border: 1px solid #e5e7eb;
    background: #fff;
    border-radius: 999px;
    padding: 6px 10px;
    font-weight: 900;
    font-size: 12px;
    cursor: pointer;
  }
  .cite-chip:hover {
    background: #f9fafb;
  }
  
  .assist-actions {
    margin-top: 8px;
    display: flex;
    gap: 10px;
    justify-content: flex-end;
  }
  
  .composer {
    margin-top: 10px;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 10px;
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
  .hint {
    margin-top: 8px;
  }
  
  /* Right evidence */
  .evidence {
    display: grid;
    gap: 10px;
  }
  .ev-head {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 10px;
  }
  .ev-title {
    font-weight: 900;
    font-size: 14px;
  }
  .ev-body {
    border: 1px solid #eef2f7;
    border-radius: 14px;
    padding: 12px;
    background: #fff;
    line-height: 1.7;
    color: #374151;
    font-weight: 700;
  }
  .ev-body.hl {
    background: #fff7ed;
    border-color: #fed7aa;
  }
  .ev-actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  .ev-note {
    margin-top: 6px;
  }
  
  .pin-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    gap: 10px;
  }
  .pin-item {
    border: 1px solid #eef2f7;
    border-radius: 14px;
    padding: 10px;
    display: grid;
    gap: 8px;
  }
  .pin-text {
    font-weight: 800;
    color: #374151;
    font-size: 13px;
    line-height: 1.5;
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
    position: fixed;
    left: 50%;
    bottom: 18px;
    transform: translateX(-50%);
    padding: 10px 12px;
    border-radius: 14px;
    font-weight: 900;
    border: 1px solid #a7f3d0;
    background: #ecfdf5;
    color: #065f46;
  }
  
  @media (max-width: 1160px) {
    .grid {
      grid-template-columns: 320px 1fr;
    }
    .right {
      grid-column: 1 / -1;
    }
    .chat {
      height: 520px;
    }
  }
  @media (max-width: 820px) {
    .app {
      grid-template-columns: 62px 1fr;
    }
    .grid {
      grid-template-columns: 1fr;
    }
    .chat {
      height: 520px;
    }
  }
  </style>
  