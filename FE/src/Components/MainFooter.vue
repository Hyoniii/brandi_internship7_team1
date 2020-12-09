<template>
  <a-layout-footer id="MainFooter">
    <div class="footerWrapper">
      <div class="footerBodyOne">
        | 상호 : (주)브랜디 | 주소 : (06223) 서울특별시 강남구 테헤란로 32길 26
        청송빌딩 | 사업자등록번호 : 220-88-93187 | 통신판매업신고 :
        2016-서울강남-00359호 | 이메일 : help@brandi.co.kr
      </div>
      <div class="footerBodyTwo">2020 © brandi inc.</div>
    </div>
    <!-- <div class="footerTool">
      <div class="topofPage"></div>
    </div> -->
  </a-layout-footer>
</template>

<script>
export default {
  name: "MainFooter",
};
</script>

<style lang="scss">
@import "../styles.scss";
#MainFooter {
  padding: 10px 20px 10px 20px;
  background-color: $default-grey-background;
  .footerWrapper {
    float: left;
    display: block;
    .footerBodyOne,
    .footerBodyTwo {
      color: $default-grey-text-onblack;
      line-height: 1.42857143;
      font-size: 12px;
    }
    // .footerTool {
    //   float: right;
    //   display: inline-block;
    //   .topOfPage {
    //   }
    // }
  }
}
</style>
