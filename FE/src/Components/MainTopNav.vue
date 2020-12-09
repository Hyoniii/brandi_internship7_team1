<template>
  <a-layout-header id="MainTopNav">
    <div class="logoWrapper">
      <img
        src="https://sadmin.brandi.co.kr/include/img/logo_2.png"
        alt="브랜디-로고"
        class="brandiLogo"
      />
      <span class="stagingInfo">staging (staging)</span>
    </div>
    <a-dropdown class="accountDropdown">
      <a class="ant-dropdown-link" @click="(e) => e.preventDefault()">
        username
        <a-icon type="down" />
      </a>
      <a-menu slot="overlay">
        <a-menu-item>
          <a href="javascript:;">Logout</a>
        </a-menu-item>
      </a-menu>
    </a-dropdown>
  </a-layout-header>
</template>

<script>
export default {
  name: "MainTopNav",
};
</script>

<style lang="scss">
@import "../styles.scss";
#MainTopNav {
  display: flex;
  justify-content: space-between;
  .logoWrapper {
    display: flex;
    justify-content: space-between;
    margin: 19px 28px 16px 0;
    float: left;
    .brandiLogo {
      width: 100%;
      width: 120px;
    }
    span {
      color: $default-white;
      margin-top: 4px;
      margin-left: 15px;
    }
  }
  .accountDropdown {
    margin-top: 22px;
    color: $default-grey;
    .ant-dropdown-link {
    }
  }
}
</style>
