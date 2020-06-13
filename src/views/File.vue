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
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
            :on-remove="handleRemove"
            :on-preview="handlePreview"
            :data="fileData"
            :auto-upload="true"
            multiple>
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">文件大小不能超过100M</div>
        </el-upload>
    </div>
    <div>
        <el-button type="primary" @click="test">下载<i class="el-icon-cloudy el-icon--right"></i></el-button>
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
      test(){
          var that = this;
      axios
        .post("http://127.0.0.1:5000/downloadfile", {
          filename: '44f2ef1bgy1gdmldp3ljjg20dc0dcb2d.gif',
          url:'http://127.0.0.1:5000/static/default_avatar.jpg'
        },{responseType:'blob'})
        .then(function(res) {
            const conent = res.data
          // console.log(conent);
          const blob = new Blob([conent])
          console.log(blob)
            const link = document.createElement('a')
            link.download = '44f2ef1bgy1gdmldp3ljjg20dc0dcb2d.gif'
            link.style.display = 'none'
            link.href = URL.createObjectURL(blob)
             document.body.appendChild(link)
            link.click() // 下载
            URL.revokeObjectURL(link.href) // 释放url
            document.body.removeChild(link)
        })
        .catch(function(error) {
          alert(error);
        });
          
      },
      handleAvatarSuccess(res, file) {
        console.log(res)
        this.handlePreview(file)
        this.$message('上传成功!');
      },
      beforeAvatarUpload(file) {
        const isLt2M = file.size / 1024 / 1024 < 100;

        if (!isLt2M) {
          this.$message.error('上传文件大小不能超过 100MB!');
        }
        return  isLt2M;
      },
      handleRemove(file, fileList) {
        console.log(file, fileList);
      },
      handlePreview(file) {
        console.log(file);
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
