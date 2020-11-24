<template>
  <div class="signUp">
    <div class="signupContainer">
      <div class="brandiLogo">
        <img alt="로고이미지" src="https://sadmin.brandi.co.kr/include/img/logo_seller_admin_1.png" />
      </div>
      <div class="signupHeader">
        <div class="signupHeading">셀러회원 가입</div>
        <div class="divider"></div>

        <div class="signupFlow">
          <div class="signupFlowBanner">정보입력</div>
        </div>
      </div>
      <div class="signupInfo">
        <section class="basicSellerInfo signupSection">
          <div class="sectionTitle">가입정보</div>
          <div class="infoInputs">
            <a-input class="inputDefault" placeholder="아이디" v-model="idValue">
              <a-icon slot="prefix" type="user" />
            </a-input>
            <a-input class="inputDefault" placeholder="비밀번호" v-model="pwValue">
              <a-icon slot="prefix" type="lock" theme="filled" />
            </a-input>
            <a-input
              class="inputDefault inputDefaultLastChild"
              placeholder="비밀번호 재입력"
              v-model="pwConfirmValue"
            >
              <a-icon slot="prefix" type="check" />
            </a-input>
          </div>
        </section>
        <section class="managerInfo signupSection">
          <div class="sectionTitle">
            담당자 정보
            <span class="titleHelper">(*실제 샵을 운영하시는 분)</span>
          </div>
          <div class="managerInputs">
            <a-input
              class="inputDefault inputDefaultLastChild"
              placeholder="핸드폰번호"
              v-model="managerNumberValue"
            >
              <a-icon slot="prefix" type="phone" theme="filled" />
            </a-input>
            <p
              class="managerInstructions inputDefaultLastChild"
            >입점 신청 후 브랜디 담당자가 연락을 드릴 수 있으니 정확한 정보를 기입해주세요.</p>
          </div>
        </section>
        <section class="signupSection sellerInfo">
          <div class="sectionTitle">셀러 정보</div>

          <div class="sellerTypes">
            <a-radio-group v-model="sellerType" @change="onChange">
              <label class="sellerTypesOptions">
                <a-radio value="쇼핑몰">쇼핑몰</a-radio>
              </label>
              <label class="sellerTypesOptions">
                <a-radio value="마켓">마켓</a-radio>
              </label>
              <label class="sellerTypesOptions">
                <a-radio value="로드샵">로드샵</a-radio>
              </label>
              <label class="sellerTypesOptions">
                <a-radio value="디자이너 브랜드">디자이너 브랜드</a-radio>
              </label>
              <label class="sellerTypesOptions">
                <a-radio value="제너럴 브랜드">제너럴 브랜드</a-radio>
              </label>
              <label class="sellerTypesOptions">
                <a-radio value="내셔널 브랜드">내셔널 브랜드</a-radio>
              </label>
              <label class="sellerTypesOptions">
                <a-radio value="뷰티">뷰티</a-radio>
              </label>
            </a-radio-group>
          </div>
          <div class="sellerInputs">
            <a-input class="inputDefault" placeholder="셀러명 (상호)" v-model="sellerNameValue">
              <a-icon slot="prefix" type="smile" />
            </a-input>
            <a-input
              class="inputDefault inputDefaultLastChild"
              placeholder="영문 셀러명 (영문상호)"
              v-model="sellerEnglishNameValue"
            >
              <a-icon slot="prefix" type="star" theme="filled" />
            </a-input>
          </div>
        </section>
      </div>
      <div class="signupBtnsContainer">
        <div class="signupBtns">
          <a-button-group class="signupBtnsGroup">
            <a-button class="btnGrouped" type="primary">fd</a-button>
            <a-button class="btnGrouped" type="danger">취소</a-button>
          </a-button-group>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      idValue: "",
      pwValue: "",
      pwConfirmValue: "",
      managerNumberValue: "",
      sellerNameValue: "",
      sellerEnglishNameValue: "",
      sellerType: ""
    };
  }
};
</script>

<style lang="scss">
@import "../../styles.scss";

.signUp {
  height: 100vh;
  background-color: $default-background;

  .signupContainer {
    width: 500px;
    height: 100%;
    margin: 0 auto;
    margin-bottom: 0px;
    padding: 20px 30px 15px 30px;
    background-color: $default-white;
    border-radius: 4px;
    overflow: auto;

    .brandiLogo {
      margin-bottom: 40px;

      img {
        width: 130px;
        max-width: 100%;
        vertical-align: top;
      }
    }

    .signupHeader {
      display: flex;
      flex-direction: column;
      justify-content: space-around;
      width: 100%;
      text-align: center;

      .signupHeading {
        display: block;
        margin-top: 20px;
        // margin-bottom: 10px;
        font-size: 24px;
        line-height: 1.1;
      }
      .divider {
        margin: 20px 0;
        height: 0;
        border-bottom: $default-border;
      }

      .signupFlow {
        display: block;
        margin: 0 15px;

        .signupFlowBanner {
          margin: 0 auto;
          padding: 10px 0;
          color: $default-grey;
          background-color: $default-black;
          font-size: 18px;
          text-align: center;
        }
      }
    }
    .signupInfo {
      display: flex;
      flex-direction: column;
      // justify-content: space-between;
      padding: 20px 15px;

      .basicSellerInfo {
        display: block;

        // .infoInputs {
        .inputContainer {
        }
        //   .inputDefault {
        //   }
        // }
      }
      .managerInfo {
        .sectionTitle {
          .titleHelper {
            color: $default-blue;
          }
        }
        .managerInputs {
          .inputDefault {
          }
          .managerInstructions {
            color: $default-blue;
            font-size: 12px;
          }
        }
      }
      .sellerInfo {
        .sellerTypes {
          margin: 10px 10px;

          .sellerTypesOptions {
            display: inline-block;
            margin-right: 12px;
            input {
            }
          }
        }
        .sellerInputs {
          .inputDefault {
          }
        }
      }
    }

    .signupBtnsContainer {
      .signupBtns {
        .signupBtnsGroup {
          background-color: transparent;
          .btnGrouped {
            color: $default-white;
          }
        }
      }
    }
  }
}
</style>