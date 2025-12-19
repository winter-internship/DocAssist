# GitHub에 프로젝트 업로드 가이드

## 📋 사전 준비

1. **Git 설치 확인**
   ```cmd
   git --version
   ```
   - 설치되어 있지 않다면: [Git 다운로드](https://git-scm.com/download/win)

2. **GitHub 로그인 확인**
   - 브라우저에서 GitHub에 로그인되어 있는지 확인

---

## 🚀 업로드 단계

### 1단계: Git 저장소 초기화 (처음 한 번만)

명령 프롬프트(cmd)를 열고 프로젝트 폴더로 이동:

```cmd
cd C:\Users\dream\Desktop\textProject
```

Git 저장소 초기화:

```cmd
git init
```

---

### 2단계: 파일 추가 및 커밋

모든 파일을 스테이징 영역에 추가:

```cmd
git add .
```

커밋 메시지와 함께 커밋:

```cmd
git commit -m "Initial commit: Vue 3 + Vite + TypeScript 대시보드 프로젝트"
```

---

### 3단계: GitHub 저장소 생성

**방법 1: GitHub 웹사이트에서 생성 (권장)**

1. 브라우저에서 [GitHub](https://github.com) 접속
2. Organizations의 `winter-internship` 클릭
3. "New repository" 또는 "새 저장소" 클릭
4. 저장소 이름 입력 (예: `text-project` 또는 원하는 이름)
5. **중요:** "Initialize this repository with a README" 체크 해제
6. "Create repository" 클릭

**방법 2: GitHub CLI 사용 (설치되어 있다면)**

```cmd
gh repo create winter-internship/text-project --public
```

---

### 4단계: 원격 저장소 연결 및 푸시

GitHub에서 생성한 저장소의 URL을 복사한 후:

```cmd
git remote add origin https://github.com/winter-internship/저장소이름.git
```

예시:
```cmd
git remote add origin https://github.com/winter-internship/text-project.git
```

브랜치 이름을 main으로 설정 (필요시):

```cmd
git branch -M main
```

GitHub에 푸시:

```cmd
git push -u origin main
```

**인증 요청 시:**
- Personal Access Token 사용 (권장)
- 또는 GitHub Desktop 사용

---

## 🔐 인증 방법

### Personal Access Token 사용 (권장)

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token" 클릭
3. 권한 선택: `repo` 체크
4. 토큰 생성 후 복사
5. `git push` 시 비밀번호 대신 토큰 입력

### GitHub Desktop 사용

1. [GitHub Desktop 다운로드](https://desktop.github.com/)
2. 설치 후 로그인
3. "Add" → "Add Existing Repository"
4. 프로젝트 폴더 선택
5. "Publish repository" 클릭

---

## 📝 한 번에 실행하는 명령어

명령 프롬프트(cmd)에서:

```cmd
cd C:\Users\dream\Desktop\textProject
git init
git add .
git commit -m "Initial commit: Vue 3 대시보드 프로젝트"
git branch -M main
git remote add origin https://github.com/winter-internship/저장소이름.git
git push -u origin main
```

**주의:** `저장소이름` 부분을 실제 저장소 이름으로 변경하세요!

---

## ✅ 확인

푸시가 완료되면:
- GitHub 웹사이트에서 `winter-internship` 조직의 저장소 목록 확인
- 파일들이 올라갔는지 확인

---

## 🔄 이후 업데이트 방법

코드를 수정한 후:

```cmd
git add .
git commit -m "변경 사항 설명"
git push
```

---

## ❓ 문제 해결

### 문제: "remote origin already exists"
```cmd
git remote remove origin
git remote add origin https://github.com/winter-internship/저장소이름.git
```

### 문제: "Authentication failed"
- Personal Access Token 사용 확인
- GitHub Desktop 사용 고려

### 문제: "Permission denied"
- Organizations의 저장소에 대한 권한 확인
- Organizations 관리자에게 권한 요청

