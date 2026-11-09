# 초신성·BAO 기반 거리 추정과 은하 거대구조 분석

초신성과 BAO로 평탄한 ΛCDM의 물질 밀도 비율 Ωm을 추정하고, 그 거리 모형을 은하의 3차원 지도와 공간 통계에 적용하는 빅데이터 물리 수업 프로젝트다. 상세 계획은 로컬 `우주론_프로젝트_계획.md`에 보관하며 Git에서 제외한다.

## 파일과 실행 순서

| 파일·폴더 | 역할 |
|---|---|
| `01_supernova.ipynb` | 초신성 허블도표·공분산·Ωm 피팅·잔차 (기존 `sn_ana.ipynb`) |
| `02_bao.ipynb` | DESI DR2 BAO 단독 피팅 (기존 `bao_ana.ipynb`) |
| `03_galaxy_structure.ipynb` | SDSS 예비 표본 다운로드·좌표·지도·단면 (기존 `stuc_ana.ipynb`) |
| `scripts/download_data.py` | 초신성·BAO 자료 다운로드, 기존 파일은 건너뜀 |
| `scripts/record_metadata.py` | 로컬 자료 SHA-256·용량·은하 행 수와 현재 Python 환경 기록 |
| `data/` | 원자료·카탈로그, [출처와 재준비 안내](data/README.md) |
| `results/figures/` | 그림 |
| `results/tables/` | 결과표 |
| `results/runs/` | 환경·실행 설정·검증 기록 |

프로젝트 루트에서 아래 명령을 실행한다. 기존 분석 환경을 계속 사용해도 되며, 새 환경은 다음처럼 준비한다.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/download_data.py
python scripts/record_metadata.py
python -m jupyterlab
```

노트북에서 방금 설치한 Python 커널을 선택한다. 세 노트북은 각각 독립적으로 실행할 수 있으며, 각 파일의 셀은 위에서 아래로 실행한다. 초신성 노트북의 마지막 다운로드 셀은 재사용 편의를 위한 것이므로, 최초 실행에서는 위의 자료 준비 명령을 먼저 실행한다. 은하 예비 지도는 Ωm=0.332를 사용하므로 피팅 완료 전에도 실행할 수 있다.

`record_metadata.py`는 명령을 실행한 Python의 환경을 `results/runs/environment.json`에 기록한다. 기존 노트북의 저장 메타데이터는 Python 3.12.13이며, 시스템의 `python3`와 커널이 다를 수 있다. `requirements.txt`는 필요한 패키지 목록이며 정확한 버전을 고정한 잠금 파일은 아니다. 노트북에서 기록하려면 다음 셀을 실행한다.

```python
import subprocess
import sys
subprocess.run([sys.executable, str(PROJECT_ROOT / "scripts/record_metadata.py")], check=True)
```

## 현재 상태와 다음 작업

기존 노트북의 실행 출력과 로컬 자료·그림을 보존했다. 구조 정리 후 Python 3.14.3에서 초신성·BAO 계산 코드를 재실행해 아래 중심값·구간·χ²가 기존 출력과 일치함을 확인했다. 세 노트북의 코드 문법과 자료 경로도 검사했다. 은하 노트북 전체 재실행, 수치 수렴 검사, 대화형 창 검증은 아직 수행하지 않았다.

- 저장된 초신성 출력: Ωm=0.332, 근사 68% 구간 0.314–0.350.
- 저장된 BAO 출력: Ωm=0.297, 근사 68% 구간 0.289–0.306.
- 기존 은하 표본: 73,016행, RA 120–250°, **Dec −5–5°**, 0.01 < z < 0.2. 이 표본의 3차원 그림과 단면이 `results/figures/`에 있다.
- 다음 작업: 계획의 Dec 0–60° 영역 확보·품질 검사, 별도 회전형 뷰어, 초신성 재검증·결합 피팅, 이웃 통계·모형 민감도 분석.

은하 노트북은 카탈로그가 이미 있으면 다운로드를 생략한다. 조회 범위를 바꿀 때는 CSV 파일명·SQL 파일명을 함께 바꾸고, 새 카탈로그와 기존 띠 표본을 구별한다. 현재 `sdss_query.sql`과 manifest는 기존 표본을 설명한다. 서버 반환 완전성, 관측 경계, 중복 천체와 품질 검사는 후속 작업이다. 정지 PNG를 확인한 것과 대화형 회전 창의 작동을 확인한 것은 별개다.

## Git 관리

안내 문서, 분석 노트북, 스크립트, 의존성, SQL, 자료 manifest를 추적한다. 계획 문서(`*계획*.md`)·원자료·생성 CSV·결과·환경 파일·다운로드 사본(`DataRelease-main/`)·캐시·가상환경은 제외한다. `results/`의 폴더 구조는 `.gitkeep`으로 유지한다. 기존 노트북 출력은 유지했으므로, 앞으로 커밋 전에는 불필요하게 큰 출력이 추가됐는지 확인한다.

```sh
git status --short
git diff
```

자료를 갱신한 뒤에는 `python scripts/record_metadata.py`로 해시와 행 수를 갱신하고, 노트북·SQL·manifest가 같은 표본을 설명하는지 확인한다. 기존 자료의 다운로드 날짜와 원격 커밋은 확인되지 않아 manifest에 `null`로 남긴다. 로컬 파일 확인 시각과 다운로드 시각을 구별한다.

현재 원격 저장소는 설정돼 있지 않다. 원격 주소가 정해지면 `git remote add origin <저장소_URL>`로 연결하고 `git push -u origin main`으로 올릴 수 있다. 대용량 자료는 이 Git 저장소에 포함되지 않는다.
