# 소스 근거 장부 (작성 시점: 2026-10-17)

> 아래는 GitHub 소스에서 직접 확인한 **현 구현 사실** 또는 대화에서 확정한 요구사항입니다. CPU·금융성과·독립 재현성에 대한 새로운 실험 결과를 뜻하지 않습니다.

## 소스 확인

| ID | 검증 가능한 기준 | 참조 |
|---|---|---|
| SRC-01 | V0.8.2는 별도 연구 전용 50개체 버전, 자동 인원 증가 차단 | [run_v082.py](https://github.com/heh-heh/market-career-dashboard/blob/strategy-engine-v3/research/evolution/run_v082.py) |
| SRC-02 | `50 bots`, 유효한 연속 5세션, 1일 $100 계좌, 최대 3포지션, 2026 OOS CLOSED | [V082_INDICATOR.md](https://github.com/heh-heh/market-career-dashboard/blob/strategy-engine-v3/research/evolution/V082_INDICATOR.md) |
| SRC-03 | 공통 1분봉/지표 및 연구 전용 포트폴리오, 네트워크·브로커 제외 | [indicator_engine.py](https://github.com/heh-heh/market-career-dashboard/blob/strategy-engine-v3/research/evolution/indicator_engine.py) |
| SRC-04 | 수익 봇 우선 부모 풀, 수익 없을 때 유효 봇 원금보존 상위 2개 | [survival_breeding.py](https://github.com/heh-heh/market-career-dashboard/blob/strategy-engine-v3/research/evolution/survival_breeding.py) |
| SRC-05 | 연구용 관리자 컨트롤러는 소스 커밋 검증 및 별도 실행 경로 사용 | [v082_web_jobs.py](https://github.com/heh-heh/market-career-dashboard/blob/strategy-engine-v3/v082_web_jobs.py) |
| SRC-06 | 가상시장 16h 거래+8h 평가 및 10월 26일 로컬 개발은 사용자 계획; 구현 검증 아님 | [PROJECT_BRIEF.md](PROJECT_BRIEF.md) |

## 관측 기록 (참고, 정식 실험 아님)

- 현재 EC2 `t8i.small` 2 vCPU, 약 2 GB RAM 기반 V0.8.2 연구: 50개체, 2개 세대 시험 기록; 50개 최신 자식은 마지막 평가 개체와 다를 수 있음. 계정·엔드포인트 정보는 여기에 저장하지 않음.
- 이전 V0.8.1 100개체 자원 산정에서 CPU 최대 75.5%로 75% 기준 초과. **V0.9 로컬 성능 근거로 외삽 금지.**
- V0.8.2는 지표·포트폴리오 계산 비용 증가로 작은 합성 비교에서 더 느린 사례가 있었다는 개발 검토 기록 존재. 반복 측정 전까지 개선/악화를 단정하지 않음.

## 근거 수준 분류

- **E0 요구사항:** 사용자가 원하는 기능, 일정.
- **E1 코드 관찰:** 특정 저장소/커밋의 소스 구현.
- **E2 테스트 증거:** 테스트명·환경·입력·결과가 있는 재현 가능 실행.
- **E3 실증 데이터:** 고정된 데이터·서로 다른 seed·설정/코드 해시·CI/실기기 결과.
- **E4 독립 재현:** 별도 검증자 또는 별도 재현 환경에서 성립한 결과.

팀마다 주장을 E0~E4로 라벨링하고, E2 이상은 실제 로그·수치·재현 명령이 없는 경우 붙이지 말 것. 자료가 없으면 **UNVERIFIED**로 표기.

## 금지

- 2026 Final OOS 임의 개방 또는 새 가격 데이터 조회/학습.
- 실계좌 자료 / API Key / 토큰 / 고객 개인 정보 기재.
- 블로그 링크만으로 거래 규칙의 공식 사실 단정.
- 코드 존재 = 성능 개선 또는 실거래 수익 발생이라고 주장.
