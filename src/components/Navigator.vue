<template>
  <div id="navigator">
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
    >
      <el-menu-item index="home" @click="toHome">
        首页
      </el-menu-item>
      <el-menu-item>vue-teach</el-menu-item>
      <el-menu-item style="float:right" index="signup" @click="toSignup">
        注册
      </el-menu-item>
      <el-menu-item style="float:right" index="login" @click="toLogin">
        登录
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: "Navigator",
  props: {
    return: String
  },
  data() {
    return {
      //returnType: this.return === "true" ? true : false,
      activeIndex: this.return
    };
  },
  methods: {
    toHome() {
      this.$router.push({ path: "/home" });
    },
    toSignup() {
      this.$router.push({ path: "/signup" });
    },
    toLogin() {
      this.$router.push({ path: "/login" });
    }
  }
};
</script>

<style scoped lang="stylus"></style>
