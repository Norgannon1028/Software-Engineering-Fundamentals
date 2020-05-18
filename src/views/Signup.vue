<template>
  <div class="signup">
    <Navigator return="signup" />
    <div style="margin-top: 15px;">
      用户名：<el-input
        placeholder="username"
        v-model="uname"
        style="width:60%"
        class="input-with-select"
      ></el-input>
      <br />
      <br />
      密码：<el-input
        placeholder="password"
        v-model="passwd1"
        style="width:60%"
        class="input-with-select"
      ></el-input>
      <br />
      <br />
      重复密码：<el-input
        placeholder="password"
        v-model="passwd2"
        style="width:60%"
        class="input-with-select"
      ></el-input>
      <br />
      <br />
      邮箱：<el-input
        placeholder="e-mail"
        v-model="email"
        style="width:60%"
        class="input-with-select"
      ></el-input>
      <br />
      <br />
      <el-button type="primary" icon="el-icon-remove" @click="test_ajax"
        >注册
      </el-button>
    </div>
    <div>
      <el-form :model="regist_form" :rules="rules" ref="regist_form" label-width="100px" class="signup">
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
          <el-button type="primary" @click="test_ajax()">注册</el-button>
          <el-button @click="resetForm('regist_form')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>

</template>

<script>
import axios from "axios";
import Navigator from "@/components/Navigator.vue";
export default {
  name: "Regist",
  components: {
    Navigator
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
    return {
      regist_form:{
        uname: "",
        passwd1: "",
        passwd2: "",
        email: ""
      },
      rules:{
        uname:[
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 12, message: '长度在 3 到 12 个字符', trigger: 'blur' }
        ],
        passwd1: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur' }
          ],
        passwd2: [
            { required: true, message: '请重复输入密码', trigger: 'blur' },
            { min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur' },
            { validator: checkpassword, trigger: 'blur' }
          ],
        email:[
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        ]
      }
      
    };
  },
  methods: {
    test_ajax() {
      var that = this;
      axios
        .post("http://localhost:5000/regist", that.regist_form)
        .then(function(response) {
          alert(response.data.msg);
          if (response.data.msg == "注册成功!")
            that.$router.push({ path: "/login" });
        })
        .catch(function(error) {
          alert(error);
        });
    },
    resetForm(formName) {
        this.$refs[formName].resetFields();
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
