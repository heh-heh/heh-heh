# V0.9 Virtual Market Arena · 12-Team Research Council

> **상태:** 기획 / 검토용 시스템 구축. 실제 12개 독립 LLM 실행과 금융 실험은 아직 수행되지 않았습니다.  
> **개발 착수 목표:** 2026-10-26 (로컬 PC). 이 프로젝트 폴더는 GitHub 프로필 README 및 실제 거래 엔진과 완전히 분리됩니다.

## 목적

서로 다른 전략·성향을 가진 수백~수천 개의 거래 AI가 **공유 시장에서 경쟁하고 진화**하는 V0.9 인공 주식시장의 설계를, 12개의 독립 전문가 팀이 먼저 제안·반박·검증하도록 구성합니다. 복잡한 가상시장에서 이기는 능력을 실제 시장 수익성으로 혼동하지 않는 것이 최우선 원칙입니다.

## 바로가기

- [프로젝트 문제정의·경계](PROJECT_BRIEF.md)
- [기존 V0.8.2의 검증된 기준](EVIDENCE_REGISTER.md)
- [12팀 명단 및 교차 심사](teams.json) · [개별 팀 지침](teams/)
- [독립 경쟁 / 반박 / 재설계 규칙](REVIEW_PROTOCOL.md)
- [평가 척도와 결론 기준](RUBRIC.md)
- [초기 위험·반증 질문 — 단일 작성자 초안](reviews/INITIAL_CHALLENGES.md)
- [기술 의사결정 초안](reviews/DECISION_LOG.md)
- [독립 실행 도구](tools/arena_review.py) 및 [테스트](tools/test_arena_review.py)

## 12팀의 작업 형태

`Round 1` : **독립** 설계 제안서 12개. 팀별 격리된 입력, 상대팀 제안 비공개.  
`Round 2` : 각 팀이 서로 다른 팀의 제안서 **2개**를 반박. 총 24개 대상 리뷰.  
`Round 3` : 각 팀이 자신에게 들어온 리뷰를 근거로 반론·수정안 제출.  
`Round 4` : 전체 평가표·쟁점·결정 기록 통합. 단일 AI 통합자가 결과를 합쳤다고 독립 제3자 검증이 끝난 것은 아닙니다.

각 결과에는 **가설 / 자료 증거 / 반증 가능 실험 / 구현 비용 / 위험**을 분리 기록합니다. Critical 안전·시장현실성 이슈를 무시한 점수 경쟁은 무효입니다.

## 실행 예시 (로컬 PC, 10월 26일 이후)

Python 3.11+ 및 OpenAI API 키가 필요합니다. **API 사용량과 요금이 발생할 수 있습니다.** 사용 가능한 모델명은 본인의 API 계정에서 확인하여 명시하세요.

```bash
cd projects/v09-virtual-market-arena
python tools/arena_review.py status
python tools/arena_review.py propose --dry-run
export OPENAI_API_KEY="..."  # 로컬 셸에서만. 파일이나 커밋에 포함하지 말 것.
python tools/arena_review.py propose --model YOUR_AVAILABLE_MODEL --max-calls 2
python tools/arena_review.py propose --model YOUR_AVAILABLE_MODEL  # 중단 시 이어서 작성
python tools/arena_review.py review --model YOUR_AVAILABLE_MODEL
python tools/arena_review.py rebut --model YOUR_AVAILABLE_MODEL
python tools/arena_review.py synthesize --model YOUR_AVAILABLE_MODEL
python tools/arena_review.py audit
python -m unittest discover -s tools -p 'test_*.py'
```

각 에이전트는 별도의 API 호출로 독립된 대화 문맥을 갖습니다. **이 채팅에서 12개의 독립 에이전트가 실행되었다는 뜻은 아닙니다.** 실행하지 않은 출력은 생성되었다고 표시하지 않습니다. 명령을 실행하면 응답 원문을 로컬 `runs/`에 저장하되 자동으로 GitHub 또는 Notion에 게시하지 않습니다. 기밀·키·실계좌 자료를 프롬프트에 포함시키지 마세요.

## 변경하지 않는 것

- `heh-heh/heh-heh`의 프로필 `README.md`, 기존 포트폴리오 웹페이지와 Pages 배포 설정
- `heh-heh/market-career-dashboard`의 V0.8.2, AWS 인스턴스, 수집기, 실거래
- 2026 Final OOS CLOSED (연구 검증 문턱은 보존)

**문서 설계 ≠ 에이전트 실행 ≠ 성과 검증 ≠ 실제 거래 승인.**
