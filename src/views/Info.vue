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
      <span>性别:</span>
      <span v-if="changeflag == false">{{image_url}} {{sex}} </span>
      <el-input
        placeholder="sex"
        v-model="sex"
        style="width:60%"
        class="input-with-select"
        v-if="changeflag == true"
      ></el-input>
      <br />
      <br />
      <span>年龄:</span>
      <span v-if="changeflag == false"> {{age}} </span>
      <el-input
        placeholder="age"
        v-model="age"
        style="width:60%"
        class="input-with-select"
        v-if="changeflag == true"
      ></el-input>
      <br />
      <br />
      <el-button type="primary" @click="changeinfo()" v-if="changeflag == false"
        >修改
      </el-button>
      <el-button
        type="primary"
        @click="test_ajax()"
        v-if="changeflag == true"
        >确认
      </el-button>
      <el-button @click="resetForm()" v-if="changeflag == true">取消</el-button>
    </div>
  </div>
</template>


<script>
// @ is an alias to /src
import axios from "axios";
import Navigator from "@/components/Navigator.vue";
import global from "@/components/global.vue";

export default {
  name: "Info",
  components: {
    Navigator
  },
  data() {
    return {
      changeflag: false,
      uname: global.username,
      email: "",
      sex: "",
      age: "",
      image_url:''
    };
  },
  mounted(){
    //alert("hi!");
    this.getinfo();
  },
  methods: {
    getinfo(){
      var that = this;
      axios
        .post("http://localhost:5000/getinfo", {
          username: that.uname,
        })
        .then(function(response) {
          //that.$set()
          that.email=response.data.email;
          that.age=response.data.old;
          that.sex=response.data.sex;
          //alert(response)
          // if (response.data.name == "登录成功!") {
          //   Navigator.data.loginflag = true;
          // }
        })
        .catch(function(error) {
          alert(error);
        });
    },
    test_ajax() {
      var that = this;
      axios
        .post("http://localhost:5000/info", {
          username: that.uname,
          age: that.age,
          sex: that.sex
        })
        .then(function(response) {
          that.age=response.data.old;
          that.sex=response.data.sex;
          that.changeflag = false;
          // if (response.data.name == "登录成功!") {
          //   Navigator.data.loginflag = true;
          // }
        })
        .catch(function(error) {
          alert(error);
        });
    },
    changeinfo(){
      this.changeflag = true;
      //alert(this.changeflag);
    },
    resetForm() {
      this.changeflag = false;
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
