<template>
  <a-layout-sider width="170" style="background: #fff" id="MainSideNav">
    <a-menu
      mode="inline"
      :default-selected-keys="['1']"
      :style="{ height: '100%', borderRight: 0 }"
    >
      <a-menu-item :key="homeSection.key" :id="homeSection.id">
        <a-icon type="home" />
        <span>홈</span>
      </a-menu-item>
      <a-sub-menu key="sub2">
        <span slot="title">
          <a-icon type="shopping-cart" />주문관리
        </span>
        <a-menu-item
          v-for="section in orderMenuSections"
          style="font-size: 13px"
          :key="section.key"
          :id="section.id"
        >{{ section.value }}</a-menu-item>
      </a-sub-menu>
      <a-sub-menu key="sub3">
        <span slot="title">
          <a-icon type="skin" />상품관리
        </span>
        <a-menu-item
          v-for="section in productMenuSections"
          style="font-size: 13px"
          :key="section.key"
          :id="section.id"
        >{{ section.value }}</a-menu-item>
      </a-sub-menu>
      <a-sub-menu key="sub4">
        <span slot="title">
          <a-icon type="user" />회원관리
        </span>
        <a-menu-item
          style="font-size: 13px"
          :key="sellerSection.key"
          :id="sellerSection.id"
        >{{ sellerSection.value }}</a-menu-item>
      </a-sub-menu>
    </a-menu>
  </a-layout-sider>
</template>

<script>
export default {
  name: "MainSideNav",
  components: {},
  data() {
    return {
      homeSection: { id: 1, key: "1", value: "홈" },
      orderMenuSections: [
        { id: 2, key: 2, value: "전체주문관리" },
        { id: 3, key: 3, value: "결제대기관리" },
        { id: 4, key: 4, value: "결제완료관리" },
        { id: 5, key: 5, value: "상품준비관리" },
        { id: 6, key: 6, value: "배송준비관리" },
        { id: 7, key: 7, value: "배송중관리" },
        { id: 8, key: 8, value: "배송완료관리" },
        { id: 9, key: 9, value: "구매확정관리" },
      ],
      productMenuSections: [
        { id: 10, key: 10, value: "상품관리" },
        { id: 11, key: 12, value: "상품등록" },
      ],
      sellerSection: { id: 12, key: 12, value: "셀러계정관리" },
    };
  },
};
</script>

<style lang="scss">
@import "../styles.scss";
#MainSideNav {
  height: 100%;
}
</style>
