# 웹 기반 재고 관리 및 출입고 관리 시스템, MOONSTOCK
<br/>

## 1. 프로젝트 배경 및 목표
- 중소 기업도 대기업 못지 않게 재고 관리 시스템이 필요 but 대표적인 재고관리 시스템인 ERP를 이용하기엔 비용 & 전문성 ↓
- ∴ 웹 기반 재고 관리 및 출입고 관리 시스템을 개발하여 중소기업이 가지고 있는 재고 관리에 대한 비용적, 시간적 부담을 줄이고자 했다.

## 2. AS-IS / TO-BE
- AS-IS
  - 복잡한 BOM 과 함께 ERP 구축에 비용이 발생한다는 부담을 가지고 있음
  - 따라서 대부분의 중소기업에서는 엑셀 등의 비전사적 툴을 사용
  - 이는 효율적인 재고 관리의 어려움을 야기
- TO-BE
  1. 웹 어플리케이션을 통한 저렴한 가격의 효율적인 BOM 관리
  2. 전사적 재고 관리의 구현
  3. 소상공인 및 중소기업의 효율적인 재고 관리 지원
 
## 3. 개발 일정 및 개발 도구
- 개발 일정 (2022.09.30 ~ 2022.10.23)
  - 2022.09.30 ~ 2022.10.02 : 로그인, 로그아웃, 회원가입 구현
  - 2022.10.03 ~ 2022.10.12 : Master Data 관리 구현
  - 2022.10.13 ~ 2022.10.19 : Transaction Data 관리 구현
  - 2022.10.20 ~ 2022.10.23 : 알파테스트 및 산출물 정리
- 개발 도구
  - Operating System : Window 11
  - Program Language : Python
  - Framework : Django
  - DBMS : SQLite
- 개발 인원
  - 1인 개발 : 박 예서 (010-7939-0170)
 
## 4. 용어 정리
- Master Data : 기업의 모든 비즈니스 활동 및 경영진의 비즈니스 의사결정에 근간이 되는 기준 데이터
  - End Item : 최종 생산품으로서 기업이 판매하게 되는 상품 정보
  - Material : End Item 을 생산하기 위한 재료 혹은 같은 Material 을 생산하기 위한 중간품
  - BOM : Bill of Material. 제품을 생산하는데 소요되는 원재료 또는 부분품에 대한 상세내역
  - Vendor : 자사가 End Item 혹은 Material 을 구매하는 기업
  - Customer : End Item 혹은 Material 의 판매 대상이 되는 고객 기업(혹은 사람)
- Transaction Data : 일상적인 구매 및 판매 업무 프로세스를 실행할 때 생성되는 데이터
  - Inventory : 전체 재고 입출고 내역
  - Buy : Material 혹은 End Item 을 구입한 이력 (재고 입고)
  - Produce : End Item 혹은 End Item 을 생산하기 위한 중간품을 생산한 내역 (생산한 상품은 입고, 재료로 소진된 상품은 출고)
  - Sell : End Item 혹은 Material 을 판매한 이력 (재고 출고)

## 5. 메뉴 구조도
![image](https://github.com/yeaseoPark/MOONSTOCK/assets/105956187/89ac25a5-5f18-4b78-8960-4ae8e3a7bd96)

