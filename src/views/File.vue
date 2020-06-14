<template>
  <div class="file">
    <Navigator return="file" />
    <el-container>
      <el-aside class="side" width="50%" >
        <div class="img-box">
        <el-upload
            class="upload"
            ref="upload"
            drag
            action="http://175.24.53.216:5000/uploadfile"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
            :on-preview="handlePreview"
            :file-list="fileList"
            :data="fileData"
            :auto-upload="true"
            multiple>
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">文件大小不能超过100M</div>
        </el-upload>
    </div>
      </el-aside>
      <el-main class="main" v-if='update_flag'>
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
                  <el-button style="margin-top:10px" @click="test(item.filename)">下载</el-button>
                  <el-button style="margin-top:10px" @click="del(item.id)">删除</el-button>
              </div>
          </div>
        </div>
      </div>
      </el-main>
    </el-container>
    
   
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
      update_flag:true,
      userid: global.userid,
      allhisfile: {},
      fileList: [],
      fileData:{
          userid:global.userid
      }
    };
  },
  created() {
    console.log(this.$store.getters.getToken);
    if(this.$store.getters.getToken){
      const decoded = jwt_decode(this.$store.getters.getToken);
      console.log(decoded);
      global.loginflag=true;
      global.username=decoded.name;
      global.avatar=decoded.avatar;
      global.userid=decoded.id;
      
    }
    if(!global.loginflag){
      this.$router.push({ name: "Home"});
    }
    this.userid=global.userid;
    this.fileData.userid=global.userid;
    this.getallfiles();
  },
  methods: {
    del(file_id){
      this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          var that=this;
        axios
        .post("http://175.24.53.216:5000/deletefile", {
          fileid: file_id
        }).then(function(res) {
          that.getallfiles();
          if(res.data.msg=='文件删除成功'){
            that.$message({
            type: 'success',
            message: '删除成功!'
          });
          }
        }).catch(function(error) {
          alert(error);
        });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });          
        });
        
    },
    test(file_name){
      var that=this;
      axios
        .post("http://175.24.53.216:5000/downloadfile", {
          filename: file_name,
          url:"http://175.24.53.216:5000/static/"+file_name
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
        .post("http://175.24.53.216:5000/getallfiles", {
          userid: that.userid
        })
        .then(function(response) {
          that.allhisfile=response
        })
        .catch(function(error) {
          alert(error);
        });
        this.update_flag=false;
        this.update_flag=true;
      },
      handleAvatarSuccess(res, file) {
        console.log(res)
        this.handlePreview(file)
        this.$message('上传成功!');
        this.getallfiles();
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
.side { 
    border: 1px solid #DCDFE6;
    margin: 15px auto;
    padding: 10px 35px 15px 35px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border: 1px solid #DCDFE6;
    opacity: 1;
    box-shadow: 0 0 5px #909399;
  }
  .main{ 
    margin: 5px auto;
    margin-left: 10px;
    padding: 0px 5px 0px 5px;
    opacity: 1;
    width: 40%;
  }
.box { 
    border: 1px solid #DCDFE6;
    margin: 10px auto;
    padding: 10px 35px 15px 35px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    box-shadow: 0 0 5px #909399;
    opacity: 1
  }
  .img-box {
    width: 100%;
    margin: 10px auto;
    padding: 0px 0px 0px 0px;
    border-radius: 5px;
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
  }
</style>
