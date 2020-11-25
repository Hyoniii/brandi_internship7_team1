<template>
  <div id="login">
    <div class="brandiLogo">
      <img src="https://sadmin.brandi.co.kr/include/img/logo_seller_admin_1.png" alt="브랜디로고" />
    </div>
    <div class="loginContainer">
      <section class="loginForm">
        <div class="loginHeader">브랜디 어드민 로그인</div>
        <div class="loginInputWrapper">
          <a-input style="height: 50%" class="loginInfoInput" placeholder="아이디" />
          <a-input style="height: 50%" class="loginInfoInput" placeholder="비밀번호" />
        </div>
      </section>

      <section class="loginSubmit">
        <div class="loginBtnWrapper">
          <a-button style="height: 100%" class="loginBtn" v-on:click="handleSignupBtn">로그인</a-button>
        </div>
        <div class="registerOptions">
          아직 셀러가 아니신가요?
          <a class="registerStartBtn">회원가입하기</a>
        </div>
      </section>
      <SellerList />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      idValue: "",
      pwValue: "",
    };
  },

}
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
    justify-content: space-between;
    width: 380px;
    height: 470px;
    padding: 64px 35px 64px 35px;
    margin: 0 auto;
    background-color: $default-white;
    border-radius: 20px;
    box-shadow: 0 4px 31px 0 rgba(0, 0, 0, 0.1);

    .loginForm {
      display: flex;
      flex-direction: column;

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

      .loginInputWrapper {
        margin-bottom: 15px;

        .loginInfoInput {
          margin-bottom: 10px;
          border-radius: 8px;
        }
      }
    }
    .loginSubmit {
      .loginBtnWrapper {
        height: 100%;
        .loginBtn {
          background-color: $black;
          color: $default-white;
          width: 100%;
          font-size: 12px;
          border-radius: 8px;
        }
      }
      .registerOptions {
        padding-top: 10px;
        font-size: 12px;
        text-align: center;

        .registerStartBtn {
          font-size: 12px;
        }
      }
    }
  }
}
</style>