<template>
  <div id="signup">
    <div class="signupContainer">
      <div class="brandiLogo">
        <img alt="로고이미지" src="https://sadmin.brandi.co.kr/include/img/logo_seller_admin_1.png" />
      </div>
      <div class="signupHeader">
        <div class="signupHeading">회원가입</div>
        <div class="divider"></div>
        <a-radio-group class="signupAccountTypes" v-model="accountType" button-style="solid">
          <a-radio-button
            :value="signupAccountType.id"
            :key="signupAccountType.id"
            v-for="signupAccountType in signupAccountTypes"
            class="signupAccountType"
          >{{ signupAccountType.value }}</a-radio-button>
        </a-radio-group>
      </div>
      <div class="signupInfo">
        <section class="basicSellerInfo signupSection">
          <div class="sectionTitle">가입정보</div>
          <div class="infoInputs">
            <a-input class="inputDefault" placeholder="아이디" v-model="idValue">
              <a-icon slot="prefix" type="user" />
            </a-input>
            <p v-if="errorMessage" class="[errorMessage ? errorMessage : '']">{{ idErrorMessage }}</p>
            <a-input-password class="inputDefault" placeholder="비밀번호" v-model="pwValue">
              <a-icon slot="prefix" type="lock" theme="filled" />
            </a-input-password>
            <p v-if="errorMessage" class="[errorMessage ? errorMessage : '']">{{ pwErrorMessage }}</p>
            <a-input-password
              class="inputDefault inputDefaultLastChild"
              placeholder="비밀번호 재입력"
              v-model="pwConfirmValue"
            >
              <a-icon slot="prefix" type="check" />
            </a-input-password>
          </div>
        </section>
        <section v-show="sellerAccountType" class="managerInfo signupSection">
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
              v-if="errorMessage"
              class="[errorMessage ? errorMessage : '']"
            >{{ phoneErrorMessage }}</p>
            <p
              class="managerInstructions inputDefaultLastChild"
            >입점 신청 후 브랜디 담당자가 연락을 드릴 수 있으니 정확한 정보를 기입해주세요.</p>
          </div>
        </section>
        <section v-show="!sellerAccountType" class="signupSection sellerInfo">
          <div class="sectionTitle">마스터 정보</div>
          <div class="sellerInputs">
            <a-input class="inputDefault" placeholder="마스터 시크릿코드" v-model="masterSecretCode">
              <a-icon slot="prefix" type="question" />
            </a-input>
            <p
              v-if="errorMessage"
              class="[errorMessage ? errorMessage : '']"
            >{{ secretcodeErrorMessage }}</p>
          </div>
        </section>
        <section v-show="sellerAccountType" class="signupSection sellerInfo">
          <div class="sectionTitle">셀러 정보</div>
          <div class="sellerTypes">
            <a-radio-group v-model="sellerType">
              <a-radio
                :value="sellerTypeOption.id"
                :key="sellerTypeOption.id"
                v-for="sellerTypeOption in sellerTypeOptions"
                class="sellerTypesOptions"
              >{{ sellerTypeOption.value }}</a-radio>
            </a-radio-group>
          </div>
          <div class="sellerInputs">
            <a-input class="inputDefault" placeholder="셀러명 (상호)" v-model="sellerNameValue">
              <a-icon slot="prefix" type="smile" />
            </a-input>
            <p
              v-if="errorMessage"
              class="[errorMessage ? errorMessage : '']"
            >{{ sellerNameErrorMessage }}</p>
            <a-input
              class="inputDefault"
              placeholder="영문 셀러명 (영문상호)"
              v-model="sellerEnglishNameValue"
            >
              <a-icon slot="prefix" type="star" theme="filled" />
            </a-input>
            <p
              v-if="errorMessage"
              class="[errorMessage ? errorMessage : '']"
            >{{ sellerEnglishNameErrorMessage }}</p>

            <a-input
              class="inputDefault inputDefaultLastChild"
              placeholder="고객센터 전화번호"
              v-model="customerServiceNumber"
            >
              <a-icon slot="prefix" type="phone" theme="filled" />
            </a-input>
            <p
              v-if="errorMessage"
              class="[errorMessage ? errorMessage : '']"
            >{{ customerServiceNumberErrorMessage }}</p>
          </div>
        </section>
        <div class="signupBtnsContainer">
          <div class="signupBtns">
            <a-button-group class="signupBtnsGroup">
              <a-button class="btnGrouped" type="danger" v-on:click="handleCancelBtn">취소</a-button>
              <a-button class="btnGrouped" type="primary">신청</a-button>
            </a-button-group>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sellerAccountType: true,
      idValue: "",
      pwValue: "",
      pwConfirmValue: "",
      managerNumberValue: "",
      sellerNameValue: "",
      sellerEnglishNameValue: "",
      customerServiceNumber: "",
      sellerType: "쇼핑몰",
      accountType: 1,
      masterSecretCode: "",
      hasError: false,
      idErrorMessage: "",
      pwErrorMessage: "",
      phoneErrorMessage: "",
      secretcodeErrorMessage: "",
      sellerNameErrorMessage: "",
      sellerEnglishNameErrorMessage: "",
      customerServiceNumberErrorMessage: "",
      sellerTypeOptions: [
        { id: 1, value: "쇼핑몰"},
        { id: 2, value: "마켓"},
        { id: 3, value: "로드샵"},
        { id: 4, value: "디자이너 브랜드"},
        { id: 5, value: "제너럴 브랜드"},
        { id: 6, value: "내셔널 브랜드"},
        { id: 7, value: "뷰티"},
        ],
      signupAccountTypes: [
        { id: 1, value: "셀러 가입"},
        { id: 2, value: "마스터 가입"},
        ],
    };
  },

  methods: {
  handleCancelBtn() {
    alert("브랜디 가입을 취소하시겠습니까?")
  },
  handleRegisterBtn() {
const validatePw = RegExp(/^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[~!@#$%^&*()\-_=+,.<>/?;:'"[{}\]\\|]).{8,20}$/);
let isValidPw = validatePw.test(this.pwValue);

const validateId = RegExp(/^([A-Za-z0-9\uac00-\ud7af])+(\1?)$/);
let isValidId = validateId.test(this.idValue);

const validateCustomerService = RegExp(/^([\d-]+)$/);
let isValidCustomerServiceNumber = validateCustomerServiceNumber.test(this.customerServiceNumber);

if (this.idValue.length < 1){
  idErrorMessage=""
}

  },

  //   if (idValue.length < 2  )
    
  //   } else if (idValue === /^([A-Za-z0-9])+([A-Za-z0-9_-]){4,19}$/){
  //     return errorMessage="아이디는 5-~20글자의 영문, 숫자, 언더바, 하이픈만 사용 가능하며 시작 문자는 영문 또는 숫자입니다."
  //   }
  //   if ()
  // },

  },
  
  computed: {

  },
  watch:{
    accountType(val){
      return val===1 ? this.sellerAccountType=true : this.sellerAccountType=false;
    }
  },
};
</script>

<style lang="scss">
@import "../../styles.scss";

#signup {
  background-color: $default-background;

  .signupContainer {
    width: 500px;
    height: 100vh;
    margin: 0 auto;
    margin-bottom: 0px;
    padding: 20px 30px 15px 30px;
    background-color: $default-white;
    border-radius: 4px;
    overflow: auto;

    .brandiLogo {
      margin-bottom: 40px;
      text-align: center;

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
      padding: 0px 15px;

      .signupHeading {
        display: block;
        margin-top: 10px;
        // margin-bottom: 10px;
        font-size: 24px;
        line-height: 1.1;
      }
      .divider {
        margin: 20px 0;
        height: 0;
        border-bottom: $default-border;
      }

      .signupAccountTypes {
        .signupAccountType {
          width: 50%;
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
          display: flex;
          margin: 15px 10px;

          .sellerTypesOptions {
            margin-right: 10px;
            input {
            }
          }
        }
        .sellerInputs {
          .inputDefault {
          }
        }
      }
      .signupBtnsContainer {
        margin: 30px 0;
        text-align: center;

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
}
</style>