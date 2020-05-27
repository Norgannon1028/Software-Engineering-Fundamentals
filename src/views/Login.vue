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
        type="password"
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
        <el-button v-if="showrepassword==true" @click="toRepassword">
          忘记密码？
        </el-button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Navigator from "@/components/Navigator.vue";
import global from "@/components/global.vue";
export default {
  name: "Login",
  components: {
    Navigator
  },
  data() {
    return {
      uname: "",
      passwd: "",
      showrepassword: false
    };
  },
  created()
  {
    this.showrepassword=false
    global.loginflag=false
  },
  methods: {
    toRepassword(){
      this.$router.push({ path: "/repassword" });
    },
    test_ajax() {
      var that = this;
      axios
        .post("http://localhost:5000/signin", {
          username: that.uname,
          password: that.passwd
        })
        .then(function(response) {
          alert(response.data.msg);
          if (response.data.msg == "登录成功!") {
            //alert(Navigator.username );
            global.loginflag = true;
            global.username = that.uname;
            global.userid = response.data.id;
            //alert(Navigator.username );
            //this.forceUpdate();
            //this.$root.username = that.uname;
            //this.$root.loginflag = true;
            that.$router.push({
              path: "/home"
            });
          }
          else if(response.data.msg == "用户名或密码错误!")
          {
            that.showrepassword=true;
          }
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
