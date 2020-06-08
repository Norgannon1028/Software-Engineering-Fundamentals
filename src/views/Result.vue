<template>
  <div>
    <Navigator return="true" />
    路由中的id为：{{ itemId }}
    <div v-show="itemId == 11111">邢湧喆nb！</div>
    <div v-show="itemId != 11111">错误的内容？（不知道该显示什么）</div>
    <div @click="testT">返回首页</div>
  </div>
</template>

<script>
import Navigator from "@/components/Navigator.vue";

export default {
  name: "Result",
  components: {
    Navigator
  },
  data() {
    return {
      itemId: ""
    };
  },
  created() {
    this.itemId = this.$route.params.id;
  },
  methods: {
    testT() {
      this.$router.push({ path: "/home" });
    }
  }
};
</script>

<style scoped lang="stylus"></style>
