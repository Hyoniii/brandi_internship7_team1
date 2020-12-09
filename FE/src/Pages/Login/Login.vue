<template>
  <div id="Login">
    <div class="brandiLogo">
      <img src="https://sadmin.brandi.co.kr/include/img/logo_seller_admin_1.png" alt="브랜디로고" />
    </div>
    <div class="loginContainer">
      <div class="loginHeader">브랜디 어드민 로그인</div>

      <a-form :form="form" @submit="handleLoginBtn" class="loginForm">
        <section class="loginInputs">
          <a-form-item
            :validate-status="userNameError() ? 'error' : ''"
            :help="userNameError() || ''"
            class="loginInfoInput"
          >
            <a-input
              v-decorator="[
                'email',
                {
                  rules: [{ required: true, message: '아이디를 입력해주세요' }],
                },
              ]"
              placeholder="아이디"
            >
              <a-icon slot="prefix" type="user" style="color: rgba(0, 0, 0, 0.25)" />
            </a-input>
          </a-form-item>
          <a-form-item
            :validate-status="passwordError() ? 'error' : ''"
            :help="passwordError() || ''"
            class="loginInfoInput"
          >
            <a-input
              v-decorator="[
                'pw',
                {
                  rules: [
                    { required: true, message: '비밀번호를 입력해주세요' },
                  ],
                },
              ]"
              type="password"
              placeholder="비밀번호"
            >
              <a-icon slot="prefix" type="lock" style="color: rgba(0, 0, 0, 0.25)" />
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
            >로그인</a-button>
          </a-form-item>

          <div class="registerOptions">
            아직 셀러가 아니신가요?
            <a class="registerStartBtn" @click="createAccount">회원가입하기</a>
          </div>
        </section>
      </a-form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const loginAPI = "http://10.251.1.127:5000/account/signin";

function hasErrors(fieldsError) {
  return Object.keys(fieldsError).some((field) => fieldsError[field]);
}

export default {
  name: "login",

  data() {
    return {
      hasErrors,
      email: "",
      pw: "",
      form: this.$form.createForm(this, { name: "horizontalLogin" }),
    };
  },
  mounted() {
    this.$nextTick(() => {
      // To disabled submit button at the beginning.
      this.form.validateFields();
    });
  },
  methods: {
    createAccount() {
      this.$router.push("/signup");
    },
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
    handleLoginBtn(e){
      e.preventDefault();
      this.form.validateFieldsAndScroll((err, values) => {
        let loginData ={
          email: values.email,
          password: values.pw,
        };
        console.log(loginData, "=================")

        axios.post(loginAPI, loginData)
        .then(res => {
          console.log("백앤드에서 오는 응답 메세지: ", res);
          if (res.status === 200) {
            alert("로그인 성공");
            console.log("token", res.data.AUTHORIZATION)
            localStorage.setItem("token", res.data.AUTHORIZATION);
            //직접 쓰면 수정 시 코드 코치기 어려워짐. alt method: vuex. 함수 만들어서 뺴야함 
            this.$router.push("/main/sellerlist");
        } else {
          alert("다시 시도해주세용! ;P");
          console.log(error)
        }
        })
      })
    },
    //이벤트에 대한 가이드 ex: 버튼 두번 누르고
    //포맷 따라 템플릿 만들기 
  }
}
</script>

<style lang="scss">
@import "../../styles.scss";

#Login {
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
          margin-bottom: 5px;
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
