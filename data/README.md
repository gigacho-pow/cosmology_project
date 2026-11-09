# 자료 출처와 로컬 저장 규칙

원자료와 생성 카탈로그는 Git에서 제외한다. 이 안내, `download_manifest.json`, `galaxies/sdss_query.sql`, `galaxies/catalog_manifest.json`은 추적한다.

| 로컬 파일 | 출처·역할 |
|---|---|
| `Pantheon+SH0ES.dat` | Pantheon+ 관측 기록 |
| `Pantheon+SH0ES_STATONLY.cov` | 통계 공분산 |
| `Pantheon+SH0ES_STAT+SYS.cov` | 통계+계통 공분산 |
| `Pantheon_README.txt` | 공개 자료의 열·공분산 설명 |
| `bao/desi_gaussian_bao_ALL_GCcomb_mean.txt` | DESI DR2 통합 BAO 측정값 |
| `bao/desi_gaussian_bao_ALL_GCcomb_cov.txt` | BAO 공분산 |
| `galaxies/sdss_dr18_galaxy_strip.csv` | SDSS DR18 예비 띠 표본의 원본 응답 |
| `galaxies/sdss_galaxies_with_coordinates.csv` | Ωm=0.332로 변환한 좌표, 단위 h⁻¹ Mpc |

프로젝트 루트에서 `python scripts/download_data.py`를 실행하면 초신성과 BAO의 여섯 파일을 준비한다. 출처는 기존 노트북 다운로드 코드에 기록된 [Pantheon+ DataRelease](https://github.com/PantheonPlusSH0ES/DataRelease/tree/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR)와 [DESI DR2 BAO 자료](https://github.com/CobayaSampler/bao_data/tree/master/desi_bao_dr2)다. 기존 파일은 덮어쓰지 않으며 `.part` 파일은 성공 후 정식 이름으로 바꾼다.

은하 자료는 `03_galaxy_structure.ipynb`에서 기존 SQL과 [SDSS DR18 조회 API](https://skyserver.sdss.org/dr18/SkyServerWS/SearchTools/SqlSearch)를 사용해 준비한다. 네트워크와 `curl`이 필요하다. 기존 표본은 Dec ±5°다. 계획의 넓은 영역은 다른 파일명과 SQL로 준비하고, 분할 조회 경계·반환 제한·품질·대표 관측 선택을 확인해야 한다.

`python scripts/record_metadata.py`는 네트워크 없이 현재 파일의 SHA-256·용량과 은하 CSV의 행 수·열을 기록한다. 기존 파일의 다운로드 날짜·원격 저장소 커밋은 알 수 없어 `null`로 둔다. 해시 기록은 원격 원본과의 대조나 자료 품질 검사 완료를 의미하지 않는다. 출처 브랜치가 바뀌면 나중에 새로 받은 파일의 해시가 달라질 수 있으므로 기존 manifest와 비교한다.

`DataRelease-main/`은 기존 공개 자료 다운로드 사본으로 보존하며, 노트북은 `data/`의 파일을 읽는다. 초신성 필터는 원본 행 순서를 유지한 상태에서 공분산 행·열에 똑같이 적용한다.
