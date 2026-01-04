<template>
  <AppLayout v-slot="{ toggleSidebar }">
    <!-- Topbar -->
    <header class="topbar">
      <div class="tb-left">
        <div class="tb-title">
          <button class="hamburger" @click="toggleSidebar" aria-label="Open menu">☰</button>
          <span class="tb-title-strong">문서 업로드</span>
          <span class="tb-sub">· PDF / JPG / PNG</span>
        </div>
      </div>
    </header>

    <!-- Content -->
    <main class="content">
      <!-- Drop Zone -->
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
            또는 <button class="dz-link" type="button" @click="pickFile">파일 선택</button>
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
            <button class="btn btn-primary" type="button" @click="pickFile">파일 선택</button>
            <button class="btn btn-ghost" type="button" :disabled="!selectedFile || uploading" @click="clearFile">
              선택 해제
            </button>
          </div>

          <div class="dz-meta">지원 포맷: PDF, JPG, PNG · 최대 20MB(예시)</div>
        </div>
      </section>

      <!-- Selected File -->
      <section class="card small" v-if="selectedFile">
        <div class="row">
          <div class="file">
            <div class="file-name">{{ selectedFile.name }}</div>
            <div class="file-sub">
              {{ humanSize(selectedFile.size) }} · {{ selectedFile.type || "unknown" }}
            </div>
          </div>

          <div class="actions">
            <button class="btn btn-primary" type="button" :disabled="uploading" @click="startUpload">
              {{ uploading ? "업로드/분석 중..." : "업로드 시작" }}
            </button>
            <button class="btn btn-outline" type="button" :disabled="uploading" @click="clearFile">
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

      <!-- 안내 -->
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
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import documentService from "../api/document.service";
import AppLayout from "../components/layout/AppLayout.vue";

const router = useRouter();

// 테마 초기화 로직 (필요시 AppLayout이나 전역으로 이동 권장)
onMounted(() => {
  const savedTheme = (localStorage.getItem("theme") as "light" | "dark") || "light";
  document.documentElement.setAttribute("data-theme", savedTheme);
});

const fileInput = ref<HTMLInputElement | null>(null);
const selectedFile = ref<File | null>(null);

const dragging = ref(false);
const uploading = ref(false);
const progress = ref(0);

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
  if (uploading.value) return;
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

async function startUpload() {
  if (!selectedFile.value) return;

  uploading.value = true;
  progress.value = 0;

  // Progress simulation
  const timer = window.setInterval(() => {
    if (progress.value < 90) {
      progress.value += Math.random() * 5;
    }
  }, 200);

  try {
    const form = new FormData();
    form.append("file", selectedFile.value);
    
    const res = await documentService.uploadDocument(form);
    const docId = res.data.id;

    progress.value = 100;
    window.clearInterval(timer);
    
    await new Promise((r) => setTimeout(r, 500));

    router.push({ name: "documentView", params: { id: docId } }).catch(() => {});
  } catch (e) {
    console.error("Upload failed", e);
    alert("업로드에 실패했어요. 다시 시도해주세요.");
    window.clearInterval(timer);
  } finally {
    uploading.value = false;
  }
}
</script>

<style scoped>
/* Topbar */
.topbar {
  background: var(--topbar-bg);
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 18px;
  /* min-height handled by grid row in AppLayout but good to have flex alignment */
  height: 100%; 
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

.card {
  background: var(--card);
  border: 1px solid #e5e7eb;
  border-radius: 18px;
  padding: 16px;
}
.card.small {
  padding: 14px 16px;
}

/* Dropzone */
.dropzone {
  border: 2px dashed #d1d5db;
  border-radius: 18px;
  padding: 16px;
  text-align: center;
  background: var(--bg);
  margin-bottom: 24px;
  min-height: 360px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
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
  background: var(--card);
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

.hamburger {
  display: none;
  font-size: 20px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  margin-right: 8px;
}

@media (max-width: 820px) {
  .hamburger {
    display: inline-flex;
  }
  .content {
    padding: 18px 14px 30px;
  }
}
</style>
