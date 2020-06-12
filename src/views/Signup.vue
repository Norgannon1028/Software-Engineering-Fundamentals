<template>
  <div class="signup">
    <Navigator return="signup" />
    <div>
      <el-form
        :model="regist_form"
        :rules="rules"
        ref="regist_form"
        label-width="100px"
        class="signup-box"
      >
      <h3 class="box-title">注册</h3>
        <el-form-item label="用户名" prop="uname">
          <el-input v-model="regist_form.uname"></el-input>
        </el-form-item> 
        <el-form-item label="密码" prop="passwd1">
          <el-input type="password" v-model="regist_form.passwd1"></el-input>
        </el-form-item> 
        <el-form-item label="重复密码" prop="passwd2">
          <el-input type="password" v-model="regist_form.passwd2"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="regist_form.email"></el-input>
          
        </el-form-item>
        <el-form-item>
          <el-button class="button" type="primary" :disabled="send_status" @click="verify">{{send_message}}</el-button>
        </el-form-item>
        <el-form-item label="验证码" prop="code">
          <el-input v-model="regist_form.code"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button class="submitBtn" type="primary" @click="submitForm('regist_form')">注册</el-button>
        </el-form-item>
        <el-form-item>
          <el-button class="button" @click="resetForm('regist_form')">重置</el-button>
        </el-form-item>
      </el-form>
      
    </div>
  </div>

</template>

<script>
import axios from "axios";
import Navigator from "@/components/Navigator.vue";
import jwt_decode from 'jwt-decode';
export default {
  name: "Regist",
  components: {
    Navigator
  },
  created() {
    if(this.$store.getters.getToken){
      const decoded = jwt_decode(this.$store.getters.getToken);
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
        } else if (value !== this.regist_form.passwd1) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
      var checkcode = (rule, value, callback) => {
        if (value !== this.code) {
          callback(new Error('验证码错误'));
        } else {
          callback();
        }
      };
    return {
      regist_form:{
        uname: "",
        passwd1: "",
        passwd2: "",
        email: "",
        code:""
      },
      rules:{
        uname:[
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 12, message: '长度在 3 到 12 个字符', trigger: 'blur' }
        ],
        passwd1: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 5, max: 15, message: '长度在 5 到 15 个字符', trigger: 'blur' }
          ],
        passwd2: [
            { required: true, message: '请重复输入密码', trigger: 'blur' },
            { min: 5, max: 15, message: '长度在 5 到 15 个字符', trigger: 'blur' },
            { validator: checkpassword, trigger: 'blur' }
          ],
        email:[
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        ],
        code:[
          { required: true, message: '请输入验证码', trigger: 'blur' },
          { validator: checkcode, trigger: 'change'  }
        ]
      },
      send_status:false,
      send_message:"获取验证码",
      code:-1
    };
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
             console.log('yes submit!!')
             var that = this;
      axios
        .post("http://127.0.0.1:5000/regist", that.regist_form)
        .then(function(response) {
          alert(response.data.msg);
          if (response.data.msg == "注册成功!")
            that.$router.push({ path: "/login" });
        })
        .catch(function(error) {
          console.log(error);
        });
        } else {
          return false
        }
    })
      
    },
    verify(){
      var that=this;
      that.code=Math.floor(Math.random() * (999999 - 100000) + 100000);
      axios
        .post("http://127.0.0.1:5000/verification", {
          email: that.regist_form.email,
          code:that.code
        })
        .then(function(response) {
          if (response.data.msg == "发送成功，请注意查收~")
            that.send_status=true;
            that.send_message="已发送";
        })
        .catch(function(error) {
          alert(error);
        });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    randomNum(min, max) {
        return Math.floor(Math.random() * (max - min) + min)
      },
  }
};
</script>

<style scoped>
.signup-box {
    border: 1px solid #DCDFE6;
    width: 350px;
    margin: 180px auto;
    padding: 35px 70px 15px 0px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 25px #909399;
  }
.button{
  display:block;
  margin:0 auto;
}
.box-title {
    text-align: center;
    margin: 0 auto 40px auto;
    padding: 0px 0px 0px 50px;
    color: #303133;
  }
.submitBtn {
      display:block;
      margin:0 auto;
      background-color: transparent;
      color: #39f;
      width: 200px;
    }
</style>