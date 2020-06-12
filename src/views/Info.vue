<template>
  <div class="info">
    <Navigator return="info" />
    <div style="margin-top: 15px;" class="info-box" label-width="80px">
      <h3 class="info-title"> 用户名:{{uname}} </h3>
      <br />
      <br />
      <h4 class="info-title">邮箱:{{email}} </h4>
      <br />
      <br />
      <div class="img-box"> 
      <el-upload
        class="avatar-uploader"
        action="http://127.0.0.1:5000/uploadavatar"
        :http-request="customUpload"
        :show-file-list="false"
        :before-upload="beforeAvatarUpload">
        <img v-if="image_url" :src="image_url" class="avatar">
      <i v-else class="el-icon-plus avatar-uploader-icon"></i>
      </el-upload>
      </div>
      <div class="radio">
        <template>
          <el-radio v-model="sex" label="1">男</el-radio>
          <el-radio v-model="sex" label="0">女</el-radio>
        </template>
      </div>
      <br />
      <el-form
        :model="info_form"
        :rules="rules"
        ref="info_form"
        label-width="100px"
        class="changeinfo"
      >
        <el-form-item label="年龄" prop="age" style="margin-left:10px">
          <el-input style="text-align: right;" v-model="info_form.age" type="number"></el-input>
        </el-form-item> 
      </el-form>
      <el-button
        class="submitBtn"
        type="primary"
        @click="confirm()"
        >确认
      </el-button>
      <el-button style="margin-left:0px;margin-top:5px" @click="tomyinfo()">取消</el-button>
    </div>
  </div>
</template>


<script>
// @ is an alias to /src
import axios from "axios";
import Navigator from "@/components/Navigator.vue";
import global from "@/components/global.vue";
import jwt_decode from 'jwt-decode';
export default {
  name: "Info",
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
    return {
      sex:"1",
      info_form:{
        age: ""
      },
      rules:{
        age:[
          { required: true, message: '请输入0-99之间的数字', trigger: 'blur' },
          { min: 1, max: 2, message: '请输入0-99之间的数字', trigger: 'blur' }
        ],
         sex: [
           { required: true, message: '请输入0或1', trigger: 'blur' },
           { min: 0, max: 1, message: '请输入0或1', trigger: 'blur' }
           ]
        // email:[
        //   { required: true, message: '请输入邮箱地址', trigger: 'blur' },
        //   { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        // ],
      },
      loginflag: global.loginflag,
      uname: "",
      email: "",
      image_url:'',
      myinfoflag:true,
      nowusername:global.username,
      followflag: true
    };
  },
  mounted(){
    this.uname = global.username
    this.getinfo();
  },
  methods: {
    tomyinfo() {
      this.$router.push({
        name: "Zone",
        params: {
          username: this.uname
        }
      });
    },
    gethisblogs() {
      var that = this;
      axios
        .post("http://127.0.0.1:5000/allhisblog", {
          username: that.uname
        })
        .then(function(response) {
          that.hisblogs=response
        })
        .catch(function(error) {
          alert(error);
        });
    },
    getinfo(){
      var that = this;
      axios
        .post("http://127.0.0.1:5000/getinfo", {
          username: that.uname,
        })
        .then(function(response) {
          //that.$set()
          that.email=response.data.email;
          that.info_form.age=response.data.old;
          that.sex=String(response.data.sex);
          that.fansnum=response.data.fansnum;
          that.follownum=response.data.follownum;
        })
        .catch(function(error) {
          alert(error);
        });
    },
    confirm() {
      var that = this;
        axios
          .post("http://127.0.0.1:5000/info", {
            username: that.uname,
            age: that.info_form.age,
            sex: that.sex,
            avatar:that.image_url
          })
          .then(function(res) {
            alert("修改成功！");
            that.$store.commit('setToken',JSON.stringify(res.data.token));
            that.tomyinfo();
          })
          .catch(function(error) {
            alert(error);
          });
      },
    handleAvatarSuccess(response,file) {
       console.log("111")
        //this.image_url=response.data.image_url;
        //this.upload_url=response.data.image_url;
        //console.log(this.upload_url); 
        console.log(URL.createObjectURL(file.raw));
      },
      beforeAvatarUpload(file) {
        const isJPG = file.type === 'image/jpeg';
        const isLt2M = file.size / 1024 / 1024 < 2;

        if (!isJPG) {
          this.$message.error('上传头像图片只能是 JPG 格式!');
        }
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');
        }
        return isJPG && isLt2M;
      },
      customUpload(fileobj){
        const isJPG = fileobj.file.type === 'image/jpeg';
        const isLt2M = fileobj.file.size / 1024 / 1024 < 2;

        if (!isJPG) {
          this.$message.error('上传头像图片只能是 JPG 格式!');return;
        }
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');return;
        }
        let param=new FormData;
        param.append('file',fileobj.file);
        var that= this;
        axios
        .post("http://127.0.0.1:5000/uploadavatar", param)
        .then(function(res) {
          that.image_url=res.data.image_url;
          console.log(res.data.image_url);
        })
        .catch(function(error) {
          alert(error);
        });
    },
      
  }
};
</script>

<style scoped>
.avatar-uploader .el-upload {
  }
  .avatar-uploader .el-upload:hover {
    border-color: #409EFF;
  }
  .avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    line-height: 178px;
    margin:0 auto;
  }
  .avatar {
    width: 178px;
    height: 178px;
  }
  .info-box {
    border: 1px solid #DCDFE6;
    width: 60%;
    margin: 180px auto;
    text-align:center;
    padding: 35px 35px 15px 0px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 25px #909399;
  }
  .img-box {
    border: 1px solid #DCDFE6;
    width: 178px;
    margin: 10px auto;
    padding: 0px 0px 0px 0px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
  }
  .info-title {
    text-align: center;
    margin: 0 auto;
    padding: 0px 0px 0px 10px;
    color: #303133;
  }
  .submitBtn {
      display:block;
      margin: 0px auto;
      background-color: transparent;
      color: #39f;
    }
  .radio{
    display:block;
    margin: 0px auto;
  }
</style>
