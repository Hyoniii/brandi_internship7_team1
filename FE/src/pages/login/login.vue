<template>
  <div id="login">
    <div class="brandiLogo">
      <img
        src="https://sadmin.brandi.co.kr/include/img/logo_seller_admin_1.png"
        alt="브랜디로고"
      />
    </div>
    <div class="loginContainer">
      <div class="loginHeader">브랜디 어드민 로그인</div>

      <a-form :form="form" @submit="handleSubmit" class="loginForm">
        <section class="loginInputs">
          <a-form-item
            :validate-status="userNameError() ? 'error' : ''"
            :help="userNameError() || ''"
            class="loginInfoInput"
          >
            <a-input
              v-decorator="[
                'userName',
                {
                  rules: [{ required: true, message: '아이디를 입력해주세요' }],
                },
              ]"
              placeholder="아이디"
            >
              <a-icon
                slot="prefix"
                type="user"
                style="color: rgba(0, 0, 0, 0.25)"
              />
            </a-input>
          </a-form-item>
          <a-form-item
            :validate-status="passwordError() ? 'error' : ''"
            :help="passwordError() || ''"
            class="loginInfoInput"
          >
            <a-input
              v-decorator="[
                'password',
                {
                  rules: [
                    { required: true, message: '비밀번호를 입력해주세요' },
                  ],
                },
              ]"
              type="password"
              placeholder="비밀번호"
            >
              <a-icon
                slot="prefix"
                type="lock"
                style="color: rgba(0, 0, 0, 0.25)"
              />
            </a-input>
          </a-form-item>
        </section>
        <section class="loginSubmit">
          <a-form-item class="loginBtnWrapper">
            <a-button
              type="primary"
              html-type="submit"
              :disabled="hasErrors(form.getFieldsError())"
              class="loginBtn"
            >
              로그인
            </a-button>
          </a-form-item>

          <div class="registerOptions">
            아직 셀러가 아니신가요?
            <a class="registerStartBtn">회원가입하기</a>
          </div>
        </section>
      </a-form>
    </div>
  </div>
</template>

<script>
const formItemLayout = {
  labelCol: { span: 20 },
  wrapperCol: { span: 20 },
};
const formTailLayout = {
  labelCol: { span: 20 },
  wrapperCol: { span: 20 },
};
function hasErrors(fieldsError) {
  return Object.keys(fieldsError).some((field) => fieldsError[field]);
}

export default {
  data() {
    return {
      hasErrors,
      form: this.$form.createForm(this, { name: "horizontal_login" }),
    };
  },
  mounted() {
    this.$nextTick(() => {
      // To disabled submit button at the beginning.
      this.form.validateFields();
    });
  },
  methods: {
    // Only show error after a field is touched.
    userNameError() {
      const { getFieldError, isFieldTouched } = this.form;
      return isFieldTouched("userName") && getFieldError("userName");
    },
    // Only show error after a field is touched.
    passwordError() {
      const { getFieldError, isFieldTouched } = this.form;
      return isFieldTouched("password") && getFieldError("password");
    },
    handleSubmit(e) {
      e.preventDefault();
      this.form.validateFields((err, values) => {
        if (!err) {
          console.log("Received values of form: ", values);
        }
      });
    },
  },
};
</script>

<style lang="scss">
@import "../../styles.scss";

#login {
  height: 100vh;
  margin: 0 auto;
  padding: 65px 0 50px;
  background-color: $default-background;

  .brandiLogo {
    display: block;
    margin-bottom: 40px;
    text-align: center;

    img {
      width: 130px;
      max-width: 100%;
      vertical-align: top;
    }
  }

  .loginContainer {
    display: flex;
    flex-direction: column;
    width: 380px;
    height: 450px;
    padding: 64px 35px 64px 35px;
    margin: 0 auto;
    background-color: $default-white;
    border-radius: 20px;
    box-shadow: 0 4px 31px 0 rgba(0, 0, 0, 0.1);

    .loginHeader {
      margin: 0 0 25px 0;
      font-size: 24px;
      font-weight: 700;
      text-align: left;
      line-height: 1.5;
      letter-spacing: -1.5px;
      text-indent: 2px;
      color: $black;
    }

    .loginForm {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      width: 100%;
      height: 100%;

      .loginInputs {
        .loginInfoInput {
          margin: 0 auto;
          width: 100%;
        }
      }

      .loginSubmit {
        display: flex;
        flex-direction: column;
        margin: 0 auto;
        width: 100%;

        .loginBtnWrapper {
          height: 100%;
          width: 100%;
          justify-content: flex-end;
          margin-bottom: 0;

          .loginBtn {
            background-color: $black;
            color: $default-white;
            width: 100%;
            font-size: 12px;
            border-radius: 8px;
            margin-bottom: 0;
          }
        }
        .registerOptions {
          font-size: 12px;
          text-align: center;

          .registerStartBtn {
            font-size: 12px;
          }
        }
      }
    }
  }
}
</style>
