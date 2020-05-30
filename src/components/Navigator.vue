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
      <el-menu-item index="home" @click="toHome" >
        首页
      </el-menu-item>
      <el-menu-item index="write" @click="toWrite" v-if="loginflag == true">
        新建博文
      </el-menu-item>
      <el-menu-item index="blog" v-if="activeIndex == 'blog'">
        浏览博文
      </el-menu-item>
      <el-menu-item index="comment" v-if="activeIndex == 'comment'">
        全部评论
      </el-menu-item>
      <el-menu-item style="float:right" index="dropout" @click="drop" v-if="loginflag == true"
        >注销</el-menu-item
      >
      <el-menu-item style="float:right" index="changepassword" @click="toChangepwd" v-if="loginflag == true"
        >修改密码</el-menu-item
      >
      <el-menu-item style="float:right" index="info" @click="toInfo" v-if="loginflag == true"
        >用户空间</el-menu-item
      >
      <el-menu-item style="float:right" v-if="loginflag == true"
        >欢迎:{{ username }}</el-menu-item
      >
      <el-menu-item style="float:right" index="signup" @click="toSignup" v-if="loginflag == false">
        注册
      </el-menu-item>
      <el-menu-item style="float:right" index="login" @click="toLogin" v-if="loginflag == false">
        登录
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
import global from '@/components/global.vue';
export default {
  name: "Navigator",
  props: {
    return: String
  },
  data() {
    return {
      //returnType: this.return === "true" ? true : false,
      activeIndex: this.return,
      username: global.username,
      loginflag: global.loginflag,
      // loginflag: this.$root.loginflag,
      // username: this.$root.username
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
    },
    toInfo() {
      this.$router.push({
        name: "Info",
        params: {
          username: global.username
        }
      });
    },
    toWrite() {
      this.$router.push({ name: "Write",params: { id:0 }});
    },
    toChangepwd() {
      this.$router.push({ path: "/changepassword" });
    },
    drop(){
      global.username="",
      global.loginflag=false,
      this.toHome()
    }
  }
};
</script>

<style scoped lang="stylus"></style>
