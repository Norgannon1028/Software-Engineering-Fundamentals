<template>
  <div class="info">
    <Navigator return="info" />
    <div style="margin-top: 15px;">
      <span> 用户名: </span>
      <span> {{uname}} </span>
      <br />
      <br />
      <span>邮箱:</span>
      <span> {{email}} </span>
      <br />
      <br />
      <el-upload
        class="avatar-uploader"
        action="http://localhost:5000/upload"
        :on-success="handleAvatarSuccess"
        :http-request="customUpload"
        :show-file-list="false"
        :before-upload="beforeAvatarUpload">
        <img v-if="image_url" :src="image_url" class="avatar">
      <i v-else class="el-icon-plus avatar-uploader-icon"></i>
      </el-upload>
      <div>
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
        <el-form-item label="年龄" prop="age">
          <el-input v-model="info_form.age" type="number"></el-input>
        </el-form-item> 
      </el-form>
      <el-button
        type="primary"
        @click="confirm()"
        >确认
      </el-button>
      <el-button @click="tomyinfo()">取消</el-button>
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
        .post("http://localhost:5000/allhisblog", {
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
        .post("http://localhost:5000/getinfo", {
          username: that.uname,
        })
        .then(function(response) {
          //that.$set()
          that.email=response.data.email;
          that.info_form.age=response.data.old;
          that.sex=String(response.data.sex);
          that.fansnum=response.data.fansnum;
          that.follownum=response.data.follownum;
          //alert(response)
          // if (response.data.name == "登录成功!") {
          //   Navigator.data.loginflag = true;
          // }
        })
        .catch(function(error) {
          alert(error);
        });
    },
    confirm() {
      var that = this;
      axios
        .post("http://localhost:5000/info", {
          username: that.uname,
          age: that.info_form.age,
          sex: that.sex
        })
        .then(function() {
          alert("修改成功！");
          that.tomyinfo();
        })
        .catch(function(error) {
          alert(error);
        });
    },
    handleAvatarSuccess(response,file) {
        alert(response.data.code);
        this.image_url=require('../assets/'+response.image_url);
        this.image_url= URL.createObjectURL(file.raw);
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
      customUpload(fileobj) {
        let param = new FormData()
        param.append('file',fileobj.file)
        var that = this;
        var  u='';
       axios
        .post("http://localhost:5000/upload",param).then(res=>{
          if(res.data.code != 0) {
            alert('文件上传失败, code:' + res.data.code)
          } else {
            //that.image_url=res.data.image_url;
            that.image_url=res.data.image_url;
          }
        })
        .catch(function(error) {
          alert(error); 
        }); 
        that.image_url=require('../assets/'+u);
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
.avatar-uploader .el-upload {
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
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
    text-align: center;
  }
  .avatar {
    width: 178px;
    height: 178px;
    display: block;
  }
</style>
