<template>
  <div class="file">
    <Navigator return="file" />
    <div>
        <el-upload
            class="upload"
            ref="upload"
            drag
            action="http://127.0.0.1:5000/uploadfile"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
            :on-preview="handlePreview"
            :file-list="fileList"
            :data="fileData"
            :auto-upload="true"
            multiple>
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">文件大小不能超过10M</div>
        </el-upload>
    </div>
    <div
        class="allhisfile"
        v-for="item in allhisfile.data"
        :key="item.id"
      > 
        <div class="box">
          <div class="list_con">
            <h5 tag="span"  class="art-title">文件名：{{ item.filename}} </h5>
              <div class="art-more">
                  <div class="art-time"><i class="el-icon-time"></i>上传时间：{{ item.time }}</div>
                  <el-button @click="test(item.filename)">下载</el-button>
              </div>
          </div>
        </div>
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
      userid: global.userid,
      allhisfile: {},
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
    else{
      this.$router.push({ name: "Home"});
    }
    this.userid=global.userid,
    this.getallfiles()
  },
  methods: {
    test(file_name){
      var that=this;
      axios
        .post("http://127.0.0.1:5000/downloadfile", {
          filename: file_name,
          url:"http://127.0.0.1:5000/static/"+file_name
        },{ responseType: 'blob' })
        .then(function(res) {
          const conent = res.data
          // console.log(conent);
          const blob = new Blob([conent])
          console.log(blob)
            const fileName = file_name
            const link = document.createElement('a')
            link.download = fileName // a标签添加属性
            link.style.display = 'none'
            link.href = URL.createObjectURL(blob)
             document.body.appendChild(link)
            link.click() // 执行下载
            URL.revokeObjectURL(link.href) // 释放url
            document.body.removeChild(link) // 释
        })
        .catch(function(error) {
          alert(error);
        });
          
    },
      getallfiles() {
      var that = this;
      axios
        .post("http://127.0.0.1:5000/getallfiles", {
          userid: that.userid
        })
        .then(function(response) {
          that.allhisfile=response
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
