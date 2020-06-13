<template>
  <div class="write">
    <Navigator return="write" />
    <div>
        <el-upload
            class="upload"
            ref="upload"
            drag
            action="http://127.0.0.1:5000/uploadfile"
            :file-list="fileList"
            :http-request="customUpload"
            :data="fileData"
            :auto-upload="true"
            multiple>
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">文件大小不能超过10M</div>
        </el-upload>
    </div>
    <div>
        <el-button type="primary">下载<i class="el-icon-cloudy el-icon--right"></i></el-button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Navigator from "@/components/Navigator.vue";
import global from "@/components/global.vue";
import jwt_decode from 'jwt-decode';
export default {
  name: "File",
  components: {
    Navigator
  },
  data() {
    return {
      fileList: [],
      fileData:{
          userid:global.userid
      }
    };
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
  methods: {
      handleAvatarSuccess(res, file) {
        console.log(res)
        this.handlePreview(file)
        this.$message('上传成功!');
      },
      beforeAvatarUpload(file) {
        const isLt2M = file.size / 1024 / 1024 < 10;

        if (!isLt2M) {
          this.$message.error('上传文件大小不能超过 10MB!');
        }
        return  isLt2M;
      },
      handleRemove(file, fileList) {
        console.log(file, fileList);
      },
      handlePreview(file) {
        console.log(file);
      },
      customUpload(fileobj){
        const isLt2M = fileobj.file.size / 1024 / 1024 < 10;
        if (!isLt2M) {
          this.$message.error('上传文件大小不能超过 10MB!');return;
        }
        let param=new FormData;
        param.append('file',fileobj.file);
        param.append('userid',global.userid);
        var that= this;
        axios
        .post("http://127.0.0.1:5000/uploadfile", param)
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
.each {
  width: 30%;
  border: 1px solid black;
  margin: 5px;
  cursor: pointer;
}
.editor{
  height: 1000px;
}
.form{
  
}
.white-space {
       white-space:pre
}
</style>
