<template>
  <div class="login">
    <Navigator return="login" />
      <el-form ref="loginForm" :model="form" :rules="rules" label-width="80px" class="login-box">
      <h3 class="login-title">要登陆了咕咕</h3>
      <el-form-item label="账号" prop="username">  
      <el-input
        placeholder="username"
        v-model="uname"
        class="input-with-select"
      ></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
      <el-input
        type="password"
        placeholder="password"
        v-model="passwd"
        class="input-with-select"
      ></el-input>
      </el-form-item>
      <el-form-item >
        <el-button class="submitBtn" type="primary" @click="test_ajax">登录</el-button>
        </el-form-item>
        <el-button v-if="showrepassword==true" @click="toRepassword">
          忘记密码？
        </el-button>
        </el-form>
        
  </div>
</template>

<script>
import axios from "axios";
import Navigator from "@/components/Navigator.vue";
import global from "@/components/global.vue";
import jwt_decode from 'jwt-decode';
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
      this.$router.push({ path: "/Forget" });
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
            const decoded = jwt_decode(response.data.token);
            console.log(decoded);
            global.loginflag = true;
            global.username = decoded.name;
            global.userid = decoded.id;
            global.avatar=decoded.avater;
            that.$store.commit('setToken',JSON.stringify(response.data.token));
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
.login-box {
    border: 1px solid #DCDFE6;
    width: 350px;
    margin: 180px auto;
    padding: 35px 35px 15px 0px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 25px #909399;
  }

.login-title {
    text-align: center;
    margin: 0 auto 40px auto;
    padding: 0px 0px 0px 10px;
    color: #303133;
  }

.submitBtn {
      
      background-color: transparent;
      color: #39f;
      width: 200px;
    }
</style>
