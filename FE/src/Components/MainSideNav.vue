<template>
  <a-layout-sider width="170" style="background: #fff" id="MainSideNav">
    <a-menu
      mode="inline"
      :default-selected-keys="['sub1']"
      :style="{ height: '100%', borderRight: 0 }"
    >
      <a-menu-item key="sub1">
        <a-icon type="home" />
        <span>홈</span>
      </a-menu-item>
      <a-sub-menu key="sub2">
        <span slot="title"> <a-icon type="shopping-cart" />주문관리 </span>
        <a-menu-item key="2">전체주문 관리</a-menu-item>
        <a-menu-item key="3">결제대기관리</a-menu-item>
        <a-menu-item key="4">결제완료관리</a-menu-item>
        <a-menu-item key="5">상품준비관리</a-menu-item>
        <a-menu-item key="6">배송준비관리</a-menu-item>
        <a-menu-item key="7">배송중관리</a-menu-item>
        <a-menu-item key="8">배송완료관리</a-menu-item>
        <a-menu-item key="9">구매확정관리</a-menu-item>
      </a-sub-menu>
      <a-sub-menu key="sub3">
        <span slot="title"> <a-icon type="skin" />상품관리 </span>
        <a-menu-item key="10">상품관리</a-menu-item>
        <a-menu-item key="11">상품등록</a-menu-item>
      </a-sub-menu>
      <a-sub-menu key="sub4">
        <span slot="title"> <a-icon type="user" />회원관리 </span>
        <a-menu-item key="12">셀러계정관리</a-menu-item>
      </a-sub-menu>
    </a-menu>
  </a-layout-sider>
</template>

<script>
export default {
  name: "MainSideNav",
  components: {},
  data() {
    return {};
  },
};
</script>

<style lang="scss">
@import "../styles.scss";

#MainSideNav {
  height: 100%;
}
</style>
