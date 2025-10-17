# 🚀 GitHub 및 Streamlit Cloud 배포 가이드

## 📋 목차
1. [GitHub 배포](#github-배포)
2. [Streamlit Cloud 배포](#streamlit-cloud-배포)
3. [문제 해결](#문제-해결)

---

## 🐙 GitHub 배포

### 1단계: Git 초기화

프로젝트 폴더에서 다음 명령어 실행:

```bash
# Git 초기화
git init

# Git 사용자 정보 설정 (최초 1회)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2단계: 파일 추가 및 커밋

```bash
# 모든 파일 추가 (.gitignore에 있는 파일은 제외됨)
git add .

# 커밋
git commit -m "Initial commit: Sales Dashboard Streamlit v2.2"
```

### 3단계: GitHub 리포지토리 생성

1. [GitHub](https://github.com) 로그인
2. 우측 상단 **"+"** → **"New repository"** 클릭
3. 리포지토리 정보 입력:
   - **Repository name**: `sales-dashboard-streamlit`
   - **Description**: "📊 판매 데이터 분석 Streamlit 대시보드 - Excel/CSV 파일 업로드 지원"
   - **Public** 또는 **Private** 선택
   - **❌ Initialize this repository with README 체크 해제** (이미 있음)
4. **"Create repository"** 클릭

### 4단계: 리포지토리 연결 및 푸시

GitHub에서 생성된 리포지토리 페이지에 표시되는 명령어 실행:

```bash
# 원격 리포지토리 추가
git remote add origin https://github.com/YOUR_USERNAME/sales-dashboard-streamlit.git

# 브랜치 이름 변경 (main으로)
git branch -M main

# GitHub에 푸시
git push -u origin main
```

---

## ☁️ Streamlit Cloud 배포

Streamlit Cloud를 사용하면 **무료로 웹에 배포**할 수 있습니다!

### 사전 요구사항
- ✅ GitHub 리포지토리에 코드 업로드 완료
- ✅ `requirements.txt` 파일 존재
- ✅ `app.py` 파일 존재

### 1단계: Streamlit Cloud 접속

1. [share.streamlit.io](https://share.streamlit.io) 접속
2. GitHub 계정으로 로그인

### 2단계: 앱 배포

1. **"New app"** 클릭
2. 배포 정보 입력:
   - **Repository**: `YOUR_USERNAME/sales-dashboard-streamlit`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. **"Deploy!"** 클릭

### 3단계: 배포 완료

- 배포 완료까지 약 2-5분 소요
- 완료되면 **공개 URL** 생성 (예: `https://your-app.streamlit.app`)
- 해당 URL로 누구나 접속 가능!

### 4단계: 데이터 파일 처리

**옵션 A**: GitHub에 샘플 데이터 포함
- `판매.xlsx` 파일을 리포지토리에 포함
- 사용자는 샘플 데이터로 테스트 가능

**옵션 B**: 파일 업로드만 사용
- `.gitignore`에 `*.xlsx` 추가
- 사용자가 직접 파일 업로드하도록 유도

---

## 🔄 업데이트 및 재배포

### 코드 수정 후 GitHub 업데이트

```bash
# 변경사항 확인
git status

# 변경된 파일 추가
git add .

# 커밋
git commit -m "Update: 기능 추가 또는 버그 수정"

# GitHub에 푸시
git push
```

### Streamlit Cloud 자동 재배포
- GitHub에 푸시하면 **자동으로 재배포**됨
- 배포 상태는 [Streamlit Cloud 대시보드](https://share.streamlit.io)에서 확인

---

## 🛠️ 문제 해결

### ❌ "Module not found" 오류

**원인**: `requirements.txt`에 패키지 누락

**해결**:
1. `requirements.txt`에 필요한 패키지 추가
2. GitHub에 커밋 & 푸시
3. Streamlit Cloud가 자동으로 재배포

### ❌ "File not found: 판매.xlsx"

**원인**: 기본 데이터 파일이 없음

**해결책 1**: GitHub에 샘플 데이터 포함
```bash
# .gitignore에서 *.xlsx 주석 처리
git add 판매.xlsx
git commit -m "Add sample data"
git push
```

**해결책 2**: app.py 수정하여 파일 업로드 필수로 변경
```python
if uploaded_file is None:
    st.warning("⚠️ 파일을 업로드해주세요.")
    st.stop()
```

### ❌ GitHub 푸시 실패 (인증 오류)

**원인**: GitHub 인증 필요

**해결**:
1. [GitHub Personal Access Token](https://github.com/settings/tokens) 생성
2. 권한: `repo`, `workflow` 선택
3. 토큰 복사
4. Git 명령어 실행 시 토큰을 비밀번호로 사용

### ❌ Streamlit Cloud 메모리 부족

**원인**: 데이터 파일이 너무 큼

**해결**:
- 샘플 데이터를 축소
- 데이터 필터링 추가
- 캐싱 최적화

---

## 📚 추가 자료

### GitHub 관련
- [GitHub 공식 문서](https://docs.github.com)
- [Git 명령어 치트시트](https://education.github.com/git-cheat-sheet-education.pdf)

### Streamlit Cloud 관련
- [Streamlit Cloud 공식 문서](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit 배포 가이드](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)

---

## 🎯 배포 체크리스트

배포 전 확인사항:

- [ ] `.gitignore` 파일 생성
- [ ] `requirements.txt` 최신 상태 확인
- [ ] `README.md` 작성 완료
- [ ] 민감한 정보(API 키 등) 제거 확인
- [ ] 샘플 데이터 준비 (선택사항)
- [ ] 로컬에서 정상 작동 확인
- [ ] Git 초기화 및 커밋
- [ ] GitHub 리포지토리 생성 및 푸시
- [ ] Streamlit Cloud 배포 (선택사항)
- [ ] 배포된 앱 테스트

---

## 📝 예시 커밋 메시지

좋은 커밋 메시지 예시:

```bash
git commit -m "feat: Add CSV file upload support"
git commit -m "fix: Resolve encoding issue for Korean CSV files"
git commit -m "docs: Update README with deployment guide"
git commit -m "style: Improve sidebar UI layout"
git commit -m "refactor: Optimize data loading function"
```

---

**버전**: v2.2  
**최종 수정일**: 2025년 10월 17일  
**작성자**: 데이터 분석팀

