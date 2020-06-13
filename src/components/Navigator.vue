<template>
  <div id="navigator">
    <el-menu
      :default-active="activeIndex"
      mode="horizontal"
      active-text-color="#ffd04b"
    >
    <!-- background-color="#545c64" -->
      <el-menu-item index="home" @click="toHome" >
        首页
      </el-menu-item>
      <el-menu-item index="write" @click="toWrite" v-if="loginflag">
        新建博文
      </el-menu-item>
      <el-menu-item index="blog" v-if="activeIndex == 'blog'">
        浏览博文
      </el-menu-item>
      <el-menu-item index="comment" v-if="activeIndex == 'comment'">
        全部评论
      </el-menu-item>
      <el-menu-item index="draft" @click="toDraft" v-if="loginflag">
        我的草稿
      </el-menu-item>
      <el-menu-item style="float:right" index="dropout" @click="drop" v-if="loginflag"
        >注销</el-menu-item
      >
      <el-menu-item style="float:right" index="changepassword" @click="toChangepwd" v-if="loginflag"
        >修改密码</el-menu-item
      >
      <el-menu-item style="float:right" index="zone" @click="toZone" v-if="loginflag"
        >用户空间</el-menu-item
      >
      <el-menu-item style="float:right" index="file" @click="toFile" v-if="loginflag"
        >资源管理</el-menu-item
      >
      <el-menu-item style="float:right" index="info" v-if="activeIndex=='info'"
        >信息修改</el-menu-item
      >
      <el-menu-item style="float:right" v-if="loginflag"
        >欢迎:{{ username }}</el-menu-item
      >
      <el-menu-item style="float:right" index="signup" @click="toSignup" v-if="!loginflag">
        注册
      </el-menu-item>
      <el-menu-item style="float:right" index="login" @click="toLogin" v-if="!loginflag">
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
    toDraft() {
      this.$router.push({ path: "/draft" });
    },
    toSignup() {
      this.$router.push({ path: "/signup" });
    },
    toLogin() {
      this.$router.push({ path: "/login" });
    },
    toZone() {
      this.$router.push({
        name: "Zone",
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
    toFile() {
      this.$router.push({ name: "File" });
    },
    drop(){
      global.username="";
      global.loginflag=false;
      this.toLogin();
      localStorage.clear();
      location. reload();
    }
  }
};
</script>

<style scoped lang="stylus"></style>
