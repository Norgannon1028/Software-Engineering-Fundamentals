<template>
  <div>
    <Navigator return="comment" />
    <div class="comment" v-for="item in allcomments.data" :key="item.id">
        
        <div class="user">
          <el-avatar src="item.face"></el-avatar>
          <div @click="tohisinfo(item.userid)">{{ item.userid }}</div>
        </div>
        <p>{{ item.content }}</p>
        <p class="time">{{ item.time }}</p>
        <br />
      </div>
      <el-button style="float:left;margin:10px" @click="backtothisblog(blog_id)">返回</el-button>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";
import Navigator from "@/components/Navigator.vue";
import jwt_decode from 'jwt-decode';
export default {
  name: "Blog",
  components: {
    Navigator
  },
  data() {
    return {
      blog_id:1,
      allcomments:{}
    };
  },
  created() {
    this.blog_id = parseInt(this.$route.params.id);
    if(this.$store.getters.getToken){
      const decoded = jwt_decode(this.$store.getters.getToken);
      console.log(decoded);
      global.loginflag=true;
      global.username=decoded.name;
      global.avatar=decoded.avatar;
      global.userid=decoded.id;
    }
    //alert(this.blog_id)
    this.showallcomments();
   // this.loadcomments();  

  },
  methods: {
    tohisinfo(hisname) {
      this.$router.push({
        name: "Info",
        params: {
          username: hisname
        }
      });
    },
    backtothisblog(blogid) {
        this.$router.push({
        name: "Blog",
        params: {
          id: blogid
        }
      });
    },
    showallcomments() {
       var that = this;
        axios
        .post("http://127.0.0.1:5000/allcomments", {
          blogid: this.blog_id
        })
        .then(function(response) {
          that.allcomments=response
        })
        .catch(function(error) {
          alert(error);
        });
    }
  },
  mounted(){

  },
};
</script>

<style scoped>
.each {
  width: 30%;
  border: 1px solid black;
  margin: 5px;
  cursor: pointer;
}
.comment{
    border: 1px solid #DCDFE6;
    padding: 10px 40px 0px 40px;
    margin-top: 5px;
  }
</style>