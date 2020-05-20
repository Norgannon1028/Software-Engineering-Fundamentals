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
      <span>性别:</span>
      <span v-if="changeflag == false"> {{sex}} </span>
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
</style>
