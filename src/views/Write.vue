<template>
  <div class="write">
    <Navigator return="write" />
    <el-form class="form" style="margin-top: 15px" label-width="80px">
      <el-form-item label="标题:">
        <label slot="label">标题:</label>
      <el-input
        placeholder="title"
        v-model="title"
        style="width:60%;text-align: center;"
        class="input-with-select"
      ></el-input>
      <br/>
      </el-form-item>
      <el-form-item label="关键词:">
      <el-input
        type="keyword"
        placeholder="keyword"
        v-model="keyword"
        style="width:60%;text-align: center;"
        class="input-with-select"
      ></el-input>
      </el-form-item>
      <div id="md">
	      <mavon-editor class="editor" ref=md @imgAdd="$imgAdd" v-model="mdStr" @save="$save"></mavon-editor>
	    </div>
      <br />
      <el-button type="primary" @click="blog_post">
        发表
      </el-button>
      <el-button @click="$save">
        保存
      </el-button>
    </el-form>
  </div>
</template>

<script>
import axios from "axios";
import Navigator from "@/components/Navigator.vue";
import global from "@/components/global.vue";
export default {
  name: "Write",
  components: {
    Navigator
  },
  data() {
    return {
      draft_id:0,
      username: global.username,
      userid: global.userid,
      text: "",
      title: "",
      keyword: "",
      time:"",
      mdStr:""
    };
  },
  created() {
    this.draft_id = parseInt(this.$route.params.id);
    var that=this;
    if(this.draft_id!=0){
      axios
        .post("http://localhost:5000/getdraft", {
          draftid: that.draft_id,
          userid: global.userid
        })
        .then(function(response) {
          if(response.data.draft_flag){
          that.title=response.data.draft.title;
          that.time=response.data.draft.time;
          that.mdStr=response.data.draft.link;
          that.keyword=response.data.draft.keyword;
          }
          else{
            that.$router.push({ name: "Write",params: { id:0 }});
          }
        })
        .catch(function(error) {
          alert(error);
        });
    }
    
  },
  methods: {
    blog_post() {
      var that = this;
      axios
        .post("http://127.0.0.1:5000/write", {
          userid: that.userid,
          md: that.mdStr,
          title: that.title,
          keyword: that.keyword,
          draftid: that.draft_id
        })
        .then(function(response) {
          alert(response.data.msg);
          if (response.data.msg == "发布成功!") {
            that.$router.push({
              path: "/home"
            });
          }
        })
        .catch(function(error) {
          alert(error);
        });
    },
    $imgAdd(pos, $file){
          var that=this;
           var formdata = new FormData();
           formdata.append('userid',that.userid);
           formdata.append('file', $file);
           axios
          .post("http://127.0.0.1:5000/upload", formdata)
          .then(function(response) {
            that.$refs.md.$img2Url(pos,response.data.image_url);
          })
          .catch(function(error) {
            alert(error);
          });
      },
      $save(){
        var that = this;
        axios
        .post("http://127.0.0.1:5000/savedraft", {
          userid: that.userid,
          md: that.mdStr,
          title: that.title,
          keyword: that.keyword,
          draftid: that.draft_id
        })
        .then(function(response) {
          alert(response.data.msg);
        })
        .catch(function(error) {
          alert(error);
        });
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
.editor{
  height: 1000px;
}
.form{
  
}
.white-space {
       white-space:pre
}
</style>
