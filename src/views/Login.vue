<template>
  <div class="login">
    <Navigator return="login" />
    <div style="margin-top: 15px;">
      用户名:<el-input
        placeholder="username"
        v-model="uname"
        style="width:60%"
        class="input-with-select"
      ></el-input>
      <br />
      <br />
      密码:
      <el-input
        placeholder="password"
        v-model="passwd"
        style="width:60%"
        class="input-with-select"
      ></el-input>
      <br />
      <br />
      <el-button type="primary" icon="el-icon-remove" @click="test_ajax">
        登录
      </el-button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Navigator from "@/components/Navigator.vue";
export default {
  name: "Login",
  components: {
    Navigator
  },
  data() {
    return {
      uname: "",
      passwd: ""
    };
  },
  methods: {
    test_ajax() {
      var that = this;
      axios
        .post("http://localhost:5000/signin", {
          username: that.uname,
          password: that.passwd
        })
        .then(function(response) {
          alert(response.data.msg);
          if (response.data.msg == "登录成功!")
            that.$router.push({ path: "/home" });
        })
        .catch(function(error) {
          alert(error);
        });
    }
  }
};
</script>

<style scoped>
.each {
  width: 30%;
  border: 1px solid black;
  margin: 5px;
  cursor: pointer;
}
</style>
