<template>
  <div class="repassword">
    <Navigator return="repassword" />
    <div>
      <el-form
        :model="rep_form"
        :rules="rules"
        ref="rep_form"
        label-width="100px"
        class="repassword"
      >
        <el-form-item label="用户名" prop="uname">
          <el-input v-model="rep_form.uname"></el-input>
        </el-form-item> 
        <el-form-item label="注册邮箱" prop="email">
          <el-input v-model="rep_form.email"></el-input>
          <el-button type="primary" :disabled="send_status" @click="verify">{{send_message}}</el-button>
        </el-form-item>
        <el-form-item label="验证码" prop="code">
          <el-input v-model="rep_form.code"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="repassword()">重置密码</el-button>
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
      var checkcode = (rule, value, callback) => {
        if (value !== this.code) {
          callback(new Error('验证码错误'));
        } else {
          callback();
        }
      };
    return {
      rep_form:{
        uname: "",
        email: "",
        code:""
      },
      rules:{
        uname:[
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 12, message: '长度在 3 到 12 个字符', trigger: 'blur' }
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
    repassword() {
      var that = this;
      axios
        .post("http://localhost:5000/repassword", {
          username: that.rep_form.uname,
          email: that.rep_form.email
        })
        .then(function(response) {
          alert(response.data.message);
          if (response.data.message == "新的密码已经发至您的邮箱，请注意查收并及时修改～")
            that.$router.push({ path: "/login" });
        })
        .catch(function(error) {
          alert(error);
        });
    },
    verify(){
      var that=this;
      that.code=Math.floor(Math.random() * (999999 - 100000) + 100000);
      axios
        .post("http://localhost:5000/verification", {
          email: that.rep_form.email,
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
    randomNum(min, max) {
        return Math.floor(Math.random() * (max - min) + min)
      },
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