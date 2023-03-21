<template>
  <div class="backgroundImg">
    <div class="black-bg">
      <div class="white-bg">

        <p class="h4 text-center mb-4">Sign in</p>
        <label for="idIn" class="grey-text" >Your id</label>
        <input type="text" id="idIn" class="form-control" v-model = "id">
        <br />
        <label for="pwIn" class="grey-text">Your password</label>
        <input type="password" id="pwIn" class="form-control" v-model = "password" v-on:keypress.enter.prevent=login>
        <div class="text-center mt-4">
          <button class="btn btn-indigo" type="submit" @click="login" style="color: white;">Login</button>
          <button class="btn btn-indigo" type="submit" @click="goMain" style="color: white;">뒤로가기</button>
        </div>
        <!-- Default form login -->
      </div>
    </div>
  </div>
</template>

<script>
import {firebase} from "@/firebase/firebaseConfig";

export default {
  name: 'SignIn',
  components: {},
  data() {
    return {
      id: '',
      password: '',
    }
  },
  methods: {
    login() {
      const self = this;
      firebase.auth().signInWithEmailAndPassword(self.id + '@timproject.co.kr', self.password)
          .then(() => {
            alert('로그인 완료')
            self.$router.push('/mainMap')
          })
          .catch((error) => {
            alert(error)
          })
    },
    goMain(){
      this.$router.push('/')
    }
  },
}
</script>

<style scoped>
.backgroundImg {
  /*background-image: url("../assets/images/startBackground.jpg");*/
  background-color:rgba(0, 0, 0, 0.5);
  height: 100vh;
  width: 100%;
  background-size: cover;
}
.black-bg {
  width: 100%; height: 100%;
  background: rgba(0,0,0,0.5);
  position: fixed; padding: 20px;
}
.white-bg {
  width: 35%;
  background: white;
  border-radius: 8px;
  padding: 50px;
  position: absolute;
  top: 30%;
  left: 37%;
  margin: -50px 0 0 -50px;
}
</style>
