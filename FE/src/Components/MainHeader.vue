<template>
  <div id="MainHeader">
    <a-page-header
      style="border: 1px solid rgb(235, 237, 240)"
      title="Title"
      :breadcrumb="{ props: { routes } }"
      sub-title="This is a subtitle"
    />
  </div>
</template>

<script>
export default {
  name: "MainHeader",
  data() {
    return {};
  },
};
</script>

<style lang="scss">
#MainHeader {
}
</style>
