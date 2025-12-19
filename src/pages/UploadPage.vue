<template>
    <div class="app">
      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="sb-top">
          <div class="sb-logo">AI</div>
        </div>
  
        <nav class="sb-nav">
          <button class="sb-item" title="대시보드" @click="go('home')">🏠</button>
          <button class="sb-item active" title="업로드" @click="go('upload')">⬆️</button>
          <button class="sb-item" title="드라이브" @click="go('drive')">🗂️</button>
          <button class="sb-item" title="Q&A" @click="go('qa')">💬</button>
          <button class="sb-item" title="용어집" @click="go('terms')">📚</button>
          <button class="sb-item" title="프로필" @click="go('profile')">👤</button>
        </nav>
  
        <div class="sb-bottom">
          <button class="sb-item" title="도움말" @click="go('guide')">❓</button>
          <button class="sb-item" title="설정" @click="go('profile')">⚙️</button>
        </div>
      </aside>
  
      <!-- Main -->
      <div class="main">
        <!-- Topbar -->
        <header class="topbar">
          <div class="tb-left">
            <div class="tb-title">
              <span class="tb-title-strong">문서 업로드</span>
              <span class="tb-sub">· PDF / JPG / PNG</span>
            </div>
          </div>
  
          <div class="tb-right">
            <button class="tb-icon" title="알림">🔔</button>
            <button class="tb-icon" title="계정">👤</button>
          </div>
        </header>
  
        <!-- Content -->
        <main class="content">
          <section class="card">
            <div
              class="dropzone"
              :class="{ dragging }"
              @dragenter.prevent="onDragEnter"
              @dragleave.prevent="onDragLeave"
              @dragover.prevent
              @drop.prevent="onDrop"
            >
              <div class="dz-icon">📄</div>
              <div class="dz-title">파일을 여기에 놓아 업로드하세요</div>
              <div class="dz-desc">
                또는 <button class="dz-link" @click="pickFile">파일 선택</button>
                으로 업로드할 수 있어요.
              </div>
  
              <input
                ref="fileInput"
                type="file"
                class="hidden"
                accept=".pdf,image/*"
                @change="onPick"
              />
  
              <div class="dz-actions">
                <button class="btn btn-primary" @click="pickFile">파일 선택</button>
                <button class="btn btn-ghost" :disabled="!selectedFile" @click="clearFile">
                  선택 해제
                </button>
              </div>
  
              <div class="dz-meta">
                지원 포맷: PDF, JPG, PNG · 최대 20MB (예시)
              </div>
            </div>
          </section>
  
          <!-- Selected File / Status -->
          <section class="card small" v-if="selectedFile">
            <div class="row">
              <div class="file">
                <div class="file-name">{{ selectedFile.name }}</div>
                <div class="file-sub">
                  {{ humanSize(selectedFile.size) }} · {{ selectedFile.type || "unknown" }}
                </div>
              </div>
  
              <div class="actions">
                <button class="btn btn-primary" :disabled="uploading" @click="startUpload">
                  {{ uploading ? "업로드 중..." : "업로드 시작" }}
                </button>
                <button class="btn btn-outline" :disabled="uploading" @click="clearFile">
                  취소
                </button>
              </div>
            </div>
  
            <div class="progress" v-if="uploading">
              <div class="bar" :style="{ width: progress + '%' }"></div>
            </div>
  
            <div class="hint" v-if="uploading">
              텍스트 추출 → 용어 분석 → 이해 보조 결과 생성 중...
            </div>
          </section>
  
          <!-- Next Step hint -->
          <section class="card small">
            <div class="next">
              <div class="next-title">업로드 후에는 무엇을 할 수 있나요?</div>
              <ul class="next-list">
                <li>원문과 “이해 보조 문서”를 나란히 비교</li>
                <li>전문 용어 클릭 시 정의/맥락 툴팁 제공</li>
                <li>문서 기반 Q&A로 추가 질문</li>
              </ul>
            </div>
          </section>
        </main>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  
  const router = useRouter();
  
  const fileInput = ref<HTMLInputElement | null>(null);
  const selectedFile = ref<File | null>(null);
  
  const dragging = ref(false);
  const uploading = ref(false);
  const progress = ref(0);
  
  function go(name: string) {
    router.push({ name }).catch(() => {});
  }
  
  function pickFile() {
    fileInput.value?.click();
  }
  
  function onPick(e: Event) {
    const input = e.target as HTMLInputElement;
    const file = input.files?.[0] ?? null;
    selectedFile.value = file;
  }
  
  function onDragEnter() {
    dragging.value = true;
  }
  function onDragLeave() {
    dragging.value = false;
  }
  function onDrop(e: DragEvent) {
    dragging.value = false;
    const file = e.dataTransfer?.files?.[0] ?? null;
    if (!file) return;
    selectedFile.value = file;
  }
  
  function clearFile() {
    selectedFile.value = null;
    if (fileInput.value) fileInput.value.value = "";
  }
  
  function humanSize(bytes: number) {
    const units = ["B", "KB", "MB", "GB"];
    let v = bytes;
    let i = 0;
    while (v >= 1024 && i < units.length - 1) {
      v /= 1024;
      i++;
    }
    return `${v.toFixed(i === 0 ? 0 : 1)} ${units[i]}`;
  }
  
  /**
   * TODO: FastAPI 붙일 때
   * - POST /api/documents/upload  (multipart/form-data)
   * - 응답으로 document_id 받고 -> 비교 화면(/docs/:id)로 이동
   */
  async function startUpload() {
    if (!selectedFile.value) return;
  
    uploading.value = true;
    progress.value = 0;
  
    // ✅ 지금은 UI 데모용 "가짜" 진행률
    const timer = window.setInterval(() => {
      progress.value = Math.min(progress.value + Math.random() * 18, 96);
    }, 240);
  
    try {
      // 실제 업로드 붙일 때 예시:
      // const form = new FormData();
      // form.append("file", selectedFile.value);
      // const res = await fetch("/api/documents/upload", { method: "POST", body: form });
      // const data = await res.json();
      // router.push({ name: "documentView", params: { id: data.document_id } });
  
      await new Promise((r) => setTimeout(r, 1800));
      progress.value = 100;
  
      await new Promise((r) => setTimeout(r, 250));
      // 데모 이동: 임시 doc id
      router.push({ name: "documentView", params: { id: "doc_demo" } }).catch(() => {});
    } finally {
      window.clearInterval(timer);
      uploading.value = false;
    }
  }
  </script>
  
  <style scoped>
  /* 전체 레이아웃: (와이어프레임처럼) 사이드바 + 상단바 + 카드 */
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
  .sb-nav {
    display: grid;
    gap: 8px;
    width: 100%;
    justify-items: center;
    padding-top: 6px;
  }
  .sb-bottom {
    margin-top: auto;
    display: grid;
    gap: 8px;
    width: 100%;
    justify-items: center;
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
  .sb-item.active {
    background: rgba(255, 255, 255, 0.18);
    outline: 1px solid rgba(255, 255, 255, 0.16);
  }
  
  /* Main */
  .main {
    display: grid;
    grid-template-rows: 64px 1fr;
  }
  
  /* Topbar */
  .topbar {
    background: #ffffff;
    border-bottom: 1px solid #e5e7eb;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 18px;
  }
  .tb-title {
    display: flex;
    align-items: baseline;
    gap: 8px;
  }
  .tb-title-strong {
    font-weight: 900;
    font-size: 15px;
  }
  .tb-sub {
    color: #6b7280;
    font-size: 12px;
  }
  .tb-right {
    display: flex;
    gap: 10px;
  }
  .tb-icon {
    width: 38px;
    height: 38px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    background: #fff;
    cursor: pointer;
  }
  .tb-icon:hover {
    background: #f9fafb;
  }
  
  /* Content */
  .content {
    max-width: 980px;
    margin: 0 auto;
    padding: 22px 18px 44px;
    display: grid;
    gap: 14px;
  }
  
  .card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 16px;
  }
  .card.small {
    padding: 14px 16px;
  }
  
  /* Dropzone (와이어프레임의 큰 점선 영역 느낌) */
  .dropzone {
    border: 2px dashed #d1d5db;
    border-radius: 18px;
    padding: 36px 18px;
    text-align: center;
    background: #fafbff;
  }
  .dropzone.dragging {
    border-color: #2563eb;
    background: #eff6ff;
  }
  .dz-icon {
    font-size: 34px;
    margin-bottom: 10px;
  }
  .dz-title {
    font-weight: 900;
    font-size: 18px;
    margin-bottom: 8px;
  }
  .dz-desc {
    color: #6b7280;
    font-size: 13px;
  }
  .dz-link {
    border: none;
    background: transparent;
    color: #2563eb;
    font-weight: 900;
    cursor: pointer;
    padding: 0 2px;
  }
  .dz-actions {
    margin-top: 16px;
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
  }
  .dz-meta {
    margin-top: 14px;
    color: #9ca3af;
    font-size: 12px;
  }
  
  .hidden {
    display: none;
  }
  
  /* File row */
  .row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
  }
  .file-name {
    font-weight: 900;
  }
  .file-sub {
    color: #6b7280;
    font-size: 12px;
    margin-top: 4px;
  }
  .actions {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  
  /* Progress */
  .progress {
    margin-top: 12px;
    height: 10px;
    background: #eef2ff;
    border-radius: 999px;
    overflow: hidden;
    border: 1px solid #e5e7eb;
  }
  .bar {
    height: 100%;
    background: #2563eb;
    width: 0%;
    transition: width 140ms linear;
  }
  .hint {
    margin-top: 10px;
    color: #6b7280;
    font-size: 12px;
  }
  
  /* Next */
  .next-title {
    font-weight: 900;
    margin-bottom: 8px;
  }
  .next-list {
    margin: 0;
    padding-left: 18px;
    color: #4b5563;
    line-height: 1.7;
    font-size: 13px;
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
    border-color: #e5e7eb;
  }
  .btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  @media (max-width: 720px) {
    .app {
      grid-template-columns: 62px 1fr;
    }
    .content {
      padding: 18px 14px 30px;
    }
  }
  </style>
  