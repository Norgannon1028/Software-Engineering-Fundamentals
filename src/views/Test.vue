<template>
  <div>
    <Navigator return="true" />
    跳转测试
  </div>
</template>

<script>
import Navigator from "@/components/Navigator.vue";

export default {
  name: "Test",
  components: {
    Navigator
  },
  created() {
    console.log("地址栏的id：" + this.$route.query.id);
    console.log("隐式的参数id：" + this.$route.params.id);
  }
};
</script>
