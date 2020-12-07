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
      <a-form :form="form" @submit="handleRegisterBtn" class="signupInfo">
        <section class="basicSellerInfo signupSection">
          <div class="sectionTitle">가입정보</div>
          <a-form-item class="inputDefault">
            <a-input
              placeholder="이메일"
              id="formInputs.email.value"
              v-decorator="[
                'email',
                {
                  rules: [
                    {
                      required: true,
                      message: '필수 입력항목입니다.',
                    },
                    {
                      pattern: /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i,
                      message: '올바른 이메일을 입력해주세요.',
                    },
                  ],
                },
              ]"
            >
              <a-icon slot="prefix" type="user" />
            </a-input>
          </a-form-item>
          <a-form-item has-feedback class="inputDefault">
            <a-input-password
              placeholder="비밀번호"
              id="formInputs.pw.value"
              v-decorator="[
                'pw',
                {
                  rules: [
                    {
                      required: true,
                      message: '필수 입력항목입니다.',
                    },
                    {
                      validator: validateToNextPassword,
                    },
                    {
                      pattern: /^(?=.*[A-Za-z])(?=.*[0-9])(?=.*[~!@#$%^&*()\-_=+,.<>/?;:[{}\]\\|]).{8,20}$/,
                      message:
                        '비밀번호는 8~20글자의 영문대소문자, 숫자, 특수문자를 조합해야 합니다.',
                    },
                  ],
                },
              ]"
              type="password"
            >
              <a-icon slot="prefix" type="lock" theme="filled" />
            </a-input-password>
          </a-form-item>
          <a-form-item has-feedback class="inputDefault">
            <a-input-password
              placeholder="비밀번호 재입력"
              id="formInputs.pwConfirm.value"
              v-decorator="[
                'pwConfirm',
                {
                  rules: [
                    {
                      required: true,
                      message: '필수 입력항목입니다.',
                    },
                    {
                      validator: compareToFirstPassword,
                    },
                  ],
                },
              ]"
              type="password"
              @blur="handleConfirmBlur"
            >
              <a-icon slot="prefix" type="lock" theme="filled" />
            </a-input-password>
          </a-form-item>
        </section>
        <section v-if="isSellerAccountType" class="managerInfo signupSection">
          <div class="sectionTitle">
            담당자 정보
            <span class="titleHelper">(*실제 샵을 운영하시는 분)</span>
          </div>
          <a-form-item class="{ hasError ? inputError : inputDefault }">
            <a-input
              placeholder="핸드폰번호"
              id="formInputs.managerNumber.value"
              v-decorator="[
                'managerNumber',
                {
                  rules: [
                    {
                      required: true,
                      message: '필수 입력항목입니다.',
                    },
                    {
                      pattern: /^([\d-]+)$/,
                      message: '전화번호를 정확히 입력해주세요.',
                    },
                  ],
                },
              ]"
            >
              <a-icon slot="prefix" type="phone" theme="filled" />
            </a-input>
            <div class="inputHelper">
              <p class="managerInstructions inputDefaultLastChild">
                입점 신청 후 브랜디 담당자가 연락을 드릴 수 있으니 정확한 정보를
                기입해주세요.
              </p>
            </div>
          </a-form-item>
        </section>
        <section v-if="accountType == 2" class="signupSection sellerInfo">
          <div class="sectionTitle">마스터 정보</div>
          <a-form-item class="inputDefault">
            <a-input
              placeholder="성명"
              id="formInputs.fullName.value"
              v-decorator="[
                'fullName',
                {
                  rules: [
                    {
                      required: true,
                      message: '필수 입력항목입니다.',
                    },
                  ],
                },
              ]"
            >
              <a-icon slot="prefix" type="bold" />
            </a-input>
          </a-form-item>
          <a-form-item has-feedback class="inputDefault">
            <a-input-password
              placeholder="마스터 시크릿코드"
              id="formInputs.masterSecretCode.value"
              v-decorator="[
                'masterSecretCode',
                {
                  rules: [
                    {
                      required: true,
                      message: '필수 입력항목입니다.',
                    },
                    {
                      validator: validateToNextMasterCode,
                    },
                  ],
                },
              ]"
              type="password"
            >
              <a-icon slot="prefix" type="question" />
            </a-input-password>
          </a-form-item>
          <a-form-item
            has-feedback
            class="{ hasError ? inputError : inputDefault }"
          >
            <a-input-password
              placeholder="마스터 시크릿코드 재입력"
              id="formInputs.masterSecretCodeConfirm.value"
              v-decorator="[
                'masterSecretCodeConfirm',
                {
                  rules: [
                    {
                      required: true,
                      message: '필수 입력항목입니다.',
                    },
                    {
                      validator: compareToFirstMasterCode,
                    },
                  ],
                },
              ]"
              type="password"
              @blur="handleConfirmBlur"
            >
              <a-icon slot="prefix" type="question" />
            </a-input-password>
            <div class="inputHelper">
              <p v-if="hasError" class="errorMessage">
                {{ formInputs.masterSecretCode.errorMessage }}
              </p>
            </div>
          </a-form-item>
        </section>
        <section v-if="isSellerAccountType" class="signupSection sellerInfo">
          <div class="sectionTitle">셀러 정보</div>
          <div class="sellerTypes">
            <a-radio-group v-model="sellerType" required>
              <a-radio
                :value="sellerTypeOption.id"
                :key="sellerTypeOption.id"
                v-for="sellerTypeOption in sellerTypeOptions"
                class="sellerTypesOptions"
                >{{ sellerTypeOption.value }}</a-radio
              >
            </a-radio-group>
          </div>
          <a-form-item class="inputDefault">
            <a-input
              placeholder="셀러명 (상호)"
              id="formInputs.sellerName.value"
              v-decorator="[
                'sellerName',
                {
                  rules: [
                    {
                      required: true,
                      message: '필수 입력항목입니다.',
                    },
                  ],
                },
              ]"
            >
              <a-icon slot="prefix" type="smile" />
            </a-input>
          </a-form-item>
          <a-form-item class="inputDefault">
            <a-input
              placeholder="영문 셀러명 (영문상호)"
              id="formInputs.sellerEnglishName.value"
              v-decorator="[
                'sellerEnglishName',
                {
                  rules: [
                    {
                      required: true,
                      message: '필수 입력항목입니다.',
                    },
                  ],
                },
              ]"
            >
              <a-icon slot="prefix" type="star" theme="filled" />
            </a-input>
          </a-form-item>
          <a-form-item class="inputDefault">
            <a-input
              placeholder="고객센터 전화번호"
              id="formInputs.customerServiceNumber.value"
              v-decorator="[
                'customerServiceNumber',
                {
                  rules: [
                    {
                      required: true,
                      message: '필수 입력항목입니다.',
                    },
                    {
                      pattern: /^([\d-]+)$/,
                      message: '전화번호를 정확히 입력해ㅐ주세요.',
                    },
                  ],
                },
              ]"
            >
              <a-icon slot="prefix" type="phone" theme="filled" />
            </a-input>
            <div class="inputHelper">
              <p v-if="hasError" class="errorMessage">
                {{ formInputs.managerNumber.errorMessage }}
              </p>
            </div>
          </a-form-item>
        </section>

        <a-form-item class="signupBtnsContainer">
          <div class="signupBtns">
            <a-button-group class="signupBtnsGroup">
              <a-button
                class="btnGrouped"
                type="danger"
                @click="handleCancelBtn"
                >취소</a-button
              >
              <a-button class="btnGrouped" type="primary" html-type="submit"
                >신청</a-button
              >
            </a-button-group>
          </div>
        </a-form-item>
      </a-form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

const signupSellerAPI = "http://10.251.1.201:5000/account/signup/seller";
const signupMasterAPI = "http://10.251.1.201:5000/account/signup/master";

export default {
  name: "signup",

  data() {
    return {
      data: null,
      signupAccountTypes: [
        { id: 1, value: "셀러 가입" },
        { id: 2, value: "마스터 가입" },
      ],
      accountType: 1,
      isSellerAccountType: true,
      sellerTypeOptions: [
        { id: 1, value: "쇼핑몰" },
        { id: 2, value: "마켓" },
        { id: 3, value: "로드샵" },
        { id: 4, value: "디자이너 브랜드" },
        { id: 5, value: "제너럴 브랜드" },
        { id: 6, value: "내셔널 브랜드" },
        { id: 7, value: "뷰티" },
      ],
      sellerType: 1,
      hasError: false,
      autoCompleteResult: [],
    };
  },
  beforeCreate() {
    this.form = this.$form.createForm(this, { name: "register" });
  },
  methods: {
    handleRegisterBtn(e) {
      e.preventDefault();
      this.form.validateFieldsAndScroll((err, values) => {
        let signupData = {
          email: values.email,
          password: values.pw,
          name: values.fullName,
          master_code: values.masterSecretCode,
          service_number: values.customerServiceNumber,
          seller_name_kr: values.sellerName,
          seller_name_en: values.sellerEnglishName,
        };

        signupData = {
          ...signupData,
          subcategory_id: this.sellerType,
          account_type_id: this.accountType === 1 ? 1 : 2,
        };

        console.log(signupData, "=================");

        axios
          .post(
            +signupData.account_type_id === 1
              ? signupSellerAPI
              : signupMasterAPI,
            signupData
          )
          .then((res) => {
            console.log("백앤드에서 오는 응답 메세지: ", res);
            if (res) {
              alert("회원가입 성공");
              this.$router.push("/");
            } else {
              alert("다시 시도해주세용! ;P");
            }
          });
      });
    },
    handleCancelBtn() {
      this.$confirm({
        title: "브랜디 가입을 취소하시겠습니까?",
        content: "OK를 누르면 1초후에 창이 자동으로 닫힙니다!",
        onOk: () => {
          this.$router.push("/");
        },
        onCancel() {},
      });
    },

    handleConfirmBlur(e) {
      const value = e.target.value;
      this.confirmDirty = this.confirmDirty || !!value;
    },

    compareToFirstPassword(rule, value, callback) {
      const form = this.form;
      if (value && value !== form.getFieldValue("pw")) {
        callback("비밀번호가 일치하지 않습니다.");
      } else {
        callback();
      }
    },
    validateToNextPassword(rule, value, callback) {
      const form = this.form;
      if (value && this.confirmDirty) {
        form.validateFields(["confirm"], { force: true });
      }
      callback();
    },
    compareToFirstMasterCode(rule, value, callback) {
      const form = this.form;
      if (value && value !== form.getFieldValue("masterSecretCode")) {
        callback("마스터 코드가 일치하지 않습니다.");
      } else {
        callback();
      }
    },
    validateToNextMasterCode(rule, value, callback) {
      const form = this.form;
      if (value && this.confirmDirty) {
        form.validateFields(["confirm"], { force: true });
      }
      callback();
    },
    // validateInput(reg, target) {
    //   target.state = reg.test(target.value);
    // },
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
      width: 100%;

      .basicSellerInfo {
        display: block;
      }
      .managerInfo {
        .sectionTitle {
          .titleHelper {
            color: $default-blue;
          }
        }
        .inputDefault {
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
