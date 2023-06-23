<template>
  <div class="backgroundImg">
    <div style="width: 750px; height: 100vh; margin: 0 auto">
      <div class = "title">
        <h2>Cat-GPT</h2>
      </div>
      <div class="smallTitle">
        <hr align = "center" width = "550px" color="white"/>
        <h3>조직의 문서를 챗봇으로 편리하게</h3>
      </div>



      <div class ="simpleLogin">
        <button class = "googleLoginButton white btn-outline-white" @click="googleLogin"><img style="float: left;" class = "googleImg" src = "@/assets/images/googleImage.png">Sign in with Google</button>
        <button class = "kakaoLoginButton btn-outline-yellow" @click="kakaoLogin"><img style="float: left;" class = "kakaoImg" src = "@/assets/images/kakaologo.png">Sign in with kakao</button>
      </div>

      <div class="textLink">
        <router-link to="login" class="loginLink">로그인</router-link>
        <router-link to="signUp" class="signUpLink">회원가입</router-link>
      </div>

    </div>
  </div>
</template>

<script>
import {firebase} from "@/firebase/firebaseConfig";

export default {
  name: 'login',
  data() {
    return {
      fbCollection: 'users',
    }
  },
  methods: {
    googleLogin() {
      const self = this;
      const db = firebase.firestore();
      const provider = new firebase.auth.GoogleAuthProvider();
      provider.setCustomParameters({
        'login_hint': 'user@example.com'
      });
      // 로그인 팝업창 띄우기
      firebase.auth().signInWithPopup(provider)
          .then(function(result) {
            const token = result.credential.accessToken;  //eslint-disable-line no-unused-vars
            const user = result.user;
            console.log(user);
            db.collection(self.fbCollection)
                .where("gmail",'==',result.user.email)
                .get()
                .then((querySnapshot) => {
                  if (querySnapshot.size === 0) {
                    alert('회원가입 필요')
                    console.log('회원가입 안됨')
                    self.$router.push("/signUp/google");
                  }
                  if (querySnapshot.size !== 0) {
                    alert('구글 로그인 성공!')
                    self.$router.push('/mainMap');
                  }
                  // self.$router.push("/mainMAp");
                })
          }).catch(function(error) {
        // Handle Errors here.
        const errorCode = error.code; //eslint-disable-line no-unused-vars
        const errorMessage = error.message; //eslint-disable-line no-unused-vars
        // The email of the user's account used.
        const email = error.email;  //eslint-disable-line no-unused-vars
        // The firebase.auth.AuthCredential type that was used.
        const credential = error.credential;    //eslint-disable-line no-unused-vars
        // ...
      });
    },
    kakaoLogin() {
      const self = this;
      window.Kakao.Auth.login({
        scope: 'account_email',   //동의 항목
        success: self.getKakaoAccount
      });
    },
    getKakaoAccount() {
      const self = this;
      const db = firebase.firestore();
      window.Kakao.API.request({
        url: '/v2/user/me',
        success: res => {
          const kakao_account = res.kakao_account;
          console.log(kakao_account);

          db.collection(self.fbCollection)
              .where("id",'==',kakao_account.email)
              .get()
              .then((querySnapshot) => {
                if (querySnapshot.size === 0) {
                  alert('회원가입 필요')
                  console.log('회원가입 안됨')
                  self.$router.push({name: 'KakaoSignUp', params: {id: kakao_account.email}})
                }
                if (querySnapshot.size !== 0) {
                  const id = kakao_account.email
                  this.login(id);
                }
              })

        },
        fail: error => {
          console.log(error)
        }
      })
    },
    login(id) {
      const self = this;
      firebase.auth().signInWithEmailAndPassword(id , id + 'tmi')
          .then(() => {
            alert('카카오 로그인 성공!')
            self.$router.push('/mainMap')
          })
          .catch((error) => {
            alert(error)
          })
    },
  },
}
</script>

<style scoped>
.backgroundImg {
  background-image: url("../assets/images/startBackground.jpg");
  background-color:rgba(0, 0, 0, 0.5);
  height: 100vh;
  width: 100%;
  background-size: cover;
}
a {
  text-decoration:none;
  color: white;
  font-weight: 600;

}
.title {
  position: absolute;
  width: 30%;
  margin-left: 0;
  top: 25vh;

  font-style: normal;
  font-weight: 700;
  font-size: 500px;
  line-height: 59px;
  color: #FFFFFF;

  text-shadow: 0px 8px 4px rgba(0, 0, 0, 0.25);
}
.smallTitle  {
  position: relative;
  top: 6vh;
  padding-bottom: 30px;
  padding-top: 10px;
}
h2{
  font-style: normal;
  font-weight: 700;
  font-size: 75px;
  line-height: 59px;
}
hr {
  position: relative;
  top: 30vh;
  height: 3px;
  color: #ffffff;
  float: right;
}
h3{
  position: relative;
  top: 29vh;
  font-style: normal;
  font-weight: 500;
  font-size: 27px;
  color: white;
  line-height: 59px;
  float: right;
  padding-right: 15px;
}
.text-red {
  color: rgba(105, 120, 168, 0.99);
}
.googleLoginButton{
  position: relative;
  width: 300px;
  height: 60px;
  top:60vh;
  font-size:23px;
  line-height: 50px;
  text-align: center;
  background: white;
  color: gray;
  border-radius: 12px;
}
.kakaoLoginButton {
  position: relative;
  width: 300px;
  height: 60px;
  top:61vh;
  font-size:23px;
  line-height: 50px;
  text-align: center;
  background: #fdd101;
  color: saddlebrown;
  border-radius: 12px;
}
.googleImg {
  width: 40px;
  height: 40px;
}
.kakaoImg {
  width: 40px;
  height: 40px;
}
.loginLink {
  position: relative;
  font-size:23px;
  color: white;
  padding:15px;
  top: 65vh;
}
.signUpLink {
  position: relative;
  font-size:23px;
  color: white;
  padding:15px;
  top: 65vh;
}
.simpleLogin {
  position: relative;
  width: 330px;
  top: -4vh;
  margin: 0 auto;
  padding:10px;
}
.textLink {
  position: relative;
  top: -4vh;
  text-align: center;
}
</style>
