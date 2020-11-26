<template>
  <div id="signup">
    <div class="signupContainer">
      <div class="brandiLogo">
        <img
          alt="로고이미지"
          src="https://sadmin.brandi.co.kr/include/img/logo_seller_admin_1.png"
        />
      </div>
      <div class="signupHeader">
        <div class="signupHeading">회원가입</div>
        <div class="divider"></div>
        <a-radio-group
          class="signupAccountTypes"
          v-model="accountType"
          button-style="solid"
        >
          <a-radio-button
            :value="signupAccountType.id"
            :key="signupAccountType.id"
            v-for="signupAccountType in signupAccountTypes"
            class="signupAccountType"
            >{{ signupAccountType.value }}</a-radio-button
          >
        </a-radio-group>
      </div>
      <div class="signupInfo">
        <section class="basicSellerInfo signupSection">
          <div class="sectionTitle">가입정보</div>
          <div class="infoInputs">
            <a-input
              class="{ hasError ? inputError : inputDefault }"
              placeholder="아이디"
              id="formInputs.id.value"
              v-model="formInputs.id.value"
              allowClear
              @change="
                () =>
                  validateInput(
                    RegExp(/^([A-Za-z0-9])([A-Za-z0-9_-]){4,19}$/),
                    this.formInputs.id
                  )
              "
            >
              <a-icon slot="prefix" type="user" />
            </a-input>
            <div class="inputHelper">
              <p v-if="hasError" class="errorMessage">
                {{ formInputs.id.errorMessage }}
              </p>
            </div>

            <a-input-password
              class="{ hasError ? inputError : inputDefault }"
              placeholder="비밀번호"
              id="formInputs.pw.value"
              v-model="formInputs.pw.value"
              @change="
                () =>
                  validateInput(
                    RegExp(
                      /(?=.*[A-Za-z])(?=.*[0-9])(?=.*[~!@#$%^&*()\-_=+,.<>/?;:'[{}\]\\|]).{8,20}$/
                    ),
                    this.formInputs.pw
                  )
              "
            >
              <a-icon slot="prefix" type="lock" theme="filled" />
            </a-input-password>
            <div class="inputHelper">
              <p v-if="hasError" class="errorMessage">
                {{ formInputs.pw.errorMessage }}
              </p>
            </div>

            <a-input-password
              class="{ hasError ? inputError : inputDefault}"
              placeholder="비밀번호 재입력"
              id="formInputs.pwConfirm.value"
              v-model="formInputs.pwConfirm.value"
              @change="clearErrorMsg"
            >
              <a-icon slot="prefix" type="check" />
            </a-input-password>
            <div class="inputHelper">
              <p v-if="hasError" class="errorMessage">
                {{ formInputs.pwConfirm.errorMessage }}
              </p>
            </div>
            <div class="inputHelper"></div>
          </div>
        </section>
        <section v-show="isSellerAccountType" class="managerInfo signupSection">
          <div class="sectionTitle">
            담당자 정보
            <span class="titleHelper">(*실제 샵을 운영하시는 분)</span>
          </div>
          <div class="managerInputs">
            <a-input
              class="{ hasError ? inputError : inputDefault}"
              placeholder="핸드폰번호"
              id="formInputs.managerNumber.value"
              v-model="formInputs.managerNumber.value"
              @change="
                () =>
                  validateInput(
                    RegExp(/^([\d-]+)$/),
                    this.formInputs.managerNumber
                  )
              "
            >
              <a-icon slot="prefix" type="phone" theme="filled" />
            </a-input>
            <div class="inputHelper">
              <p v-if="hasError" class="errorMessage">
                {{ formInputs.managerNumber.errorMessage }}
              </p>
              <p class="managerInstructions inputDefaultLastChild">
                입점 신청 후 브랜디 담당자가 연락을 드릴 수 있으니 정확한 정보를
                기입해주세요.
              </p>
            </div>
          </div>
        </section>
        <section v-show="!isSellerAccountType" class="signupSection sellerInfo">
          <div class="sectionTitle">마스터 정보</div>
          <div class="sellerInputs">
            <a-input
              class="inputDefault"
              placeholder="성명"
              id="formInputs.fullName.value"
              v-model="formInputs.fullName.value"
              @change="
                () =>
                  validateInput(RegExp(/^[가-힣]+$/), this.formInputs.fullName)
              "
            >
              <a-icon slot="prefix" type="bold" />
            </a-input>
            <div class="inputHelper">
              <p v-if="hasError" class="errorMessage">
                {{ formInputs.fullName.errorMessage }}
              </p>
            </div>
            <a-input-password
              class="inputDefault"
              placeholder="마스터 시크릿코드"
              id="formInputs.masterSecretCode.value"
              v-model="formInputs.masterSecretCode.value"
              @change="
                () =>
                  validateInput(
                    RegExp(/^[0-9a-z]+$/),
                    this.formInputs.masterSecretCode
                  )
              "
            >
              <a-icon slot="prefix" type="question" />
            </a-input-password>
            <div class="inputHelper">
              <p v-if="hasError" class="errorMessage">
                {{ formInputs.masterSecretCode.errorMessage }}
              </p>
            </div>
          </div>
        </section>
        <section v-show="isSellerAccountType" class="signupSection sellerInfo">
          <div class="sectionTitle">셀러 정보</div>
          <div class="sellerTypes">
            <a-radio-group v-model="sellerType">
              <a-radio
                :value="sellerTypeOption.id"
                :key="sellerTypeOption.id"
                v-for="sellerTypeOption in sellerTypeOptions"
                class="sellerTypesOptions"
                >{{ sellerTypeOption.value }}</a-radio
              >
            </a-radio-group>
          </div>
          <div class="sellerInputs">
            <a-input
              class="inputDefault"
              placeholder="셀러명 (상호)"
              id="formInputs.sellerName.value"
              v-model="formInputs.sellerName.value"
              @change="
                () =>
                  validateInput(
                    RegExp(/^([A-Za-z0-9\uac00-\ud7af])+(\1?)$/),
                    this.formInputs.sellerName
                  )
              "
            >
              <a-icon slot="prefix" type="smile" />
            </a-input>
            <div class="inputHelper">
              <p v-if="hasError" class="errorMessage">
                {{ formInputs.sellerName.errorMessage }}
              </p>
            </div>

            <a-input
              class="inputDefault"
              placeholder="영문 셀러명 (영문상호)"
              id="formInputs.sellerEnglishName.value"
              v-model="formInputs.sellerEnglishName.value"
              @change="
                () =>
                  validateInput(
                    RegExp(/^[a-zA-Z]+$/),
                    this.formInputs.sellerEnglishName
                  )
              "
            >
              <a-icon slot="prefix" type="star" theme="filled" />
            </a-input>
            <div class="inputHelper">
              <p v-if="hasError" class="errorMessage">
                {{ formInputs.sellerEnglishName.errorMessage }}
              </p>
            </div>

            <a-input
              class="inputDefault inputDefaultLastChild"
              placeholder="고객센터 전화번호"
              id="formInputs.customerServiceNumber.value"
              v-model="formInputs.customerServiceNumber.value"
              @change="
                () =>
                  validateInput(
                    RegExp(/^([\d-]+)$/),
                    this.formInputs.customerServiceNumber
                  )
              "
            >
              <a-icon slot="prefix" type="phone" theme="filled" />
            </a-input>
            <div class="inputHelper">
              <p v-if="hasError" class="errorMessage">
                {{ formInputs.customerServiceNumber.errorMessage }}
              </p>
            </div>
          </div>
        </section>

        <div class="signupBtnsContainer">
          <div class="signupBtns">
            <a-button-group class="signupBtnsGroup">
              <a-button
                class="btnGrouped"
                type="danger"
                v-on:click="handleCancelBtn"
                >취소</a-button
              >
              <a-button
                class="btnGrouped"
                type="primary"
                @click="handleRegisterBtn"
                >신청</a-button
              >
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
      accountType: 1,
      isSellerAccountType: true,
      formInputs: {
        id: { value: "", state: false, errorMessage: "" },
        pw: { value: "", state: false, errorMessage: "" },
        pwConfirm: { value: "", state: false, errorMessage: "" },
        managerNumber: { value: "", state: false, errorMessage: "" },
        sellerName: { value: "", state: false, errorMessage: "" },
        sellerEnglishName: { value: "", state: false, errorMessage: "" },
        customerServiceNumber: { value: "", state: false, errorMessage: "" },
        masterSecretCode: { value: "", state: false, errorMessage: "" },
        fullName: { value: "", state: false, errorMessage: "" },
      },
      idValue: "",
      pwValue: "",
      pwConfirmValue: "",
      managerNumberValue: "",
      sellerNameValue: "",
      sellerEnglishNameValue: "",
      customerServiceNumber: "",
      sellerType: "쇼핑몰",
      masterSecretCode: "",
      hasError: false,
      sellerTypeOptions: [
        { id: 1, value: "쇼핑몰" },
        { id: 2, value: "마켓" },
        { id: 3, value: "로드샵" },
        { id: 4, value: "디자이너 브랜드" },
        { id: 5, value: "제너럴 브랜드" },
        { id: 6, value: "내셔널 브랜드" },
        { id: 7, value: "뷰티" },
      ],
      signupAccountTypes: [
        { id: 1, value: "셀러 가입" },
        { id: 2, value: "마스터 가입" },
      ],
    };
  },

  methods: {
    validateInput(reg, target) {
      const isValid = (target.state = reg.test(target.value));

      if (isValid === false) {
        return (hasError = true);
        target.errorMessage = "l;sjkdfl;skjdf;kds";
      }
    },
    handleCancelBtn() {
      alert("브랜디 가입을 취소하시겠습니까?");
    },
    // clearErrorMsg(e) {
    //   console.log(e.target.id);
    //   if (e.target.id === "idValue") return (this.idErrorMessage = "");
    //   if (e.target.id === "pwValue") return (this.pwErrorMessage = "");
    //   if (e.target.id === "pwConfirmValue")
    //     return (this.pwConfirmErrorMessage = "");
    //   if (e.target.id === "managerNumberValue")
    //     return (this.phoneErrorMessage = "");
    //   if (e.target.id === "masterSecretCode")
    //     return (this.secretcodeErrorMessage = "");
    //   if (e.target.id === "sellerNameValue")
    //     return (this.sellerNameErrorMessage = "");
    //   if (e.target.id === "sellerEnglishNameValue")
    //     return (this.sellerEnglishNameErrorMessage = "");
    //   if (e.target.id === "customerServiceNumber")
    //     return (this.customerServiceNumberErrorMessage = "");

    handleRegisterBtn() {
      if (this.formInputs.id.value.length < 1) {
        this.hasError = true;
        this.formInputs.id.errorMessage = "필수 입력항목입니다.";
      }
      if (this.formInputs.pw.value.length < 1) {
        this.hasError = true;
        this.formInputs.pw.errorMessage = "필수 입력항목입니다.";
      }
      if (this.formInputs.pwConfirm.value.length < 1) {
        this.hasError = true;
        this.formInputs.pwConfirm.errorMessage = "필수 입력항목입니다.";
      }
      if (this.formInputs.managerNumber.value.length < 1) {
        this.hasError = true;
        this.formInputs.managerNumber.errorMessage = "필수 입력항목입니다.";
      }
      if (this.formInputs.sellerName.value.length < 1) {
        this.hasError = true;
        this.formInputs.sellerName.errorMessage = "필수 입력항목입니다.";
      }
      if (this.formInputs.sellerEnglishName.value.length < 1) {
        this.hasError = true;
        this.formInputs.sellerEnglishName.errorMessage = "필수 입력항목입니다.";
      }
      if (this.formInputs.customerServiceNumber.value.length < 1) {
        this.hasError = true;
        this.formInputs.customerServiceNumber.errorMessage =
          "필수 입력항목입니다.";
      }
      if (this.formInputs.masterSecretCode.value.length < 1) {
        this.hasError = true;
        this.formInputs.masterSecretCode.errorMessage = "필수 입력항목입니다.";
      }
      if (this.formInputs.masterSecretCode.value.length < 1) {
        this.hasError = true;
        this.formInputs.masterSecretCode.error = "필수 입력항목입니다.";
      }
    },
  },
  computed: {},
  watch: {
    accountType(val) {
      return val === 1
        ? (this.isSellerAccountType = true)
        : (this.isSellerAccountType = false);
    },
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
      padding: 20px 15px;

      .basicSellerInfo {
        display: block;
      }
      .managerInfo {
        .sectionTitle {
          .titleHelper {
            color: $default-blue;
          }
        }
        .managerInputs {
          .inputHelper {
            .managerInstructions {
              color: $default-blue;
              font-size: 12px;
            }
          }
        }
      }
      .sellerInfo {
        .sellerTypes {
          display: flex;
          margin: 15px 10px;

          .sellerTypesOptions {
            margin-right: 10px;
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
