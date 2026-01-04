# Git 가이드

이 문서는 Git을 사용하여 프로젝트를 관리하고 GitHub에 업로드하는 방법을 설명합니다.

## 📋 사전 준비

1. **Git 설치 확인**
   ```bash
   git --version
   ```

2. **GitHub 로그인 확인**
   - 브라우저에서 GitHub에 로그인되어 있는지 확인

---

## 🚀 업로드 단계 (초기 설정)

### 1단계: Git 저장소 초기화

프로젝트 루트 디렉토리에서 실행:

```bash
git init
```

### 2단계: 파일 추가 및 커밋

```bash
git add .
git commit -m "Initial commit"
```

### 3단계: 원격 저장소 연결 및 푸시

GitHub에서 저장소를 생성한 후 URL을 복사하여 연결합니다.

```bash
git remote add origin https://github.com/사용자명/저장소이름.git
git branch -M main
git push -u origin main
```

---

## 🔄 일상적인 업데이트 방법

코드를 수정한 후 다음 명령어로 업데이트를 반영합니다.

```bash
# 1. 변경된 파일 확인
git status

# 2. 변경사항 스테이징
git add .

# 3. 커밋 (메시지는 변경 내용을 요약)
git commit -m "기능 추가: 로그인 페이지 구현"

# 4. GitHub에 푸시
git push
```

## ❓ 문제 해결

### "remote origin already exists"
이미 연결된 저장소가 있다는 뜻입니다. 기존 연결을 삭제하고 다시 연결하려면:
```bash
git remote remove origin
git remote add origin https://github.com/사용자명/저장소이름.git
```

### "Authentication failed"
- GitHub 패스워드 대신 **Personal Access Token**을 사용해야 할 수 있습니다.
- 또는 **GitHub Desktop**이나 **VS Code**의 Git 기능을 사용하면 인증이 더 쉽습니다.

