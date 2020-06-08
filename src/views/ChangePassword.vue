<template>
  <div class="changepassword">
    <Navigator return="changepassword" />
    <div>
      <el-form
        :model="change_form"
        :rules="rules"
        ref="change_form"
        label-width="100px"
        class="box"
      >
      <h3 class="box-title">修改密码</h3>
        <el-form-item label="用户名" prop="uname">
          <el-input v-model="change_form.uname"></el-input>
        </el-form-item> 
        <el-form-item label="旧密码" prop="oldpassword">
          <el-input type="password" v-model="change_form.oldpassword"></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="passwd1">
          <el-input type="password" v-model="change_form.passwd1"></el-input>
        </el-form-item> 
        <el-form-item label="重复新密码" prop="passwd2">
          <el-input type="password" v-model="change_form.passwd2"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button class="submitBtn" type="primary" @click="change()">确认修改</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>

</template>

<script>
import axios from "axios";
import Navigator from "@/components/Navigator.vue";
import jwt_decode from 'jwt-decode'
export default {
  name: "Changepassword",
  components: {
    Navigator
  },
  created(){
    if(this.$store.getters.getToken){
      const decoded=jwt_decode(this.$store.getters.getToken);
      console.log(decoded);
      global.loginflag=true;
      global.username=decoded.name;
      global.avatar=decoded.avatar;
      global.userid=decoded.id;
    }
  },
  data() {
      var checkpassword = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请重复输入密码'));
        } else if (value !== this.change_form.passwd1) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
    return {
      change_form:{
        uname: "",
        oldpassword: "",
        passwd1: "",
        passwd2: "",
      },
      rules:{
        uname:[
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 12, message: '长度在 3 到 12 个字符', trigger: 'blur' }
        ],
        oldpassword: [
          { required: true, message: '请输入旧密码', trigger: 'blur' },
          { min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur' }
          ],
        passwd1: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur' }
          ],
        passwd2: [
            { required: true, message: '请重复输入新密码', trigger: 'blur' },
            { min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur' },
            { validator: checkpassword, trigger: 'blur' }
          ],

      },
      send_status:false,
      send_message:"获取验证码",
      code:-1
    };
  },
  methods: {
    change() {
      var that = this;
      axios
        .post("http://localhost:5000/changepassword", {
          username: that.change_form.uname,
          oldpassword: that.change_form.oldpassword,
          password: that.change_form.passwd1,
        })
        .then(function(response) {
          alert(response.data.msg);
          if (response.data.msg == "密码修改成功！")
            that.$router.push({ path: "/home" });
        })
        .catch(function(error) {
          alert(error);
        });
    }
  }
};
</script>

<style scoped>box
.box-title {
    text-align: center;
    margin: 0 auto ;
    padding: 0px 0px 0px 0px;
    color: #303133;
  }
.box {
    border: 1px solid #DCDFE6;
    width: 350px;
    margin: 180px auto;
    padding: 35px 35px 15px 35px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 25px #909399;
  }
.submitBtn {
      
      background-color: transparent;
      color: #39f;
      width: 200px;
    }
</style>