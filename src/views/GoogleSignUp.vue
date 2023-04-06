<template>
  <div class="black-bg">
    <div class="white-bg">
      <p class="h4 text-center mb-4">회원정보 입력</p>
      <div>
        <label for="defaultFormRegisterNameEx" class="grey-text">이름</label>
        <input v-model="name" type="text" id="defaultFormRegisterNameEx" class="form-control" maxlength=10 readonly/>
      </div>
      <div>
        <label for="defaultFormRegisterNameEx" class="grey-text">닉네임</label>
        <input v-model="nickName" type="text" id="defaultFormRegisterNameEx" class="form-control" maxlength="10"
               @change="validateNickName(nickName)"/>
      </div>
      <div>
        <label for="defaultFormRegisterConfirmEx" class="grey-text">전화번호</label>
        <input v-model="phoneNum" type="text" id="defaultFormRegisterConfirmEx" class="form-control" maxlength="13"
               oninput="javascript: this.value = this.value.replace(/[^0-9]/, '').replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`);"/>
      </div>
      <div>
        <label for="defaultFormRegisterEmailEx" class="grey-text">아이디</label>
          <input  v-model="id" type="text" id="defaultFormRegisterEmailEx" class="form-control" readonly/>
      </div>

      <div class="text-center mt-4">
        <button class="btn btn-indigo" type="submit" @click="signup" style="color: white;">저장하기</button>
        <button class="btn btn-indigo" type="submit" @click="goMain" style="color: white;">뒤로가기</button>
      </div>
    </div>
  </div>
</template>

<script>
import {firebase} from '@/firebase/firebaseConfig';
export default {
  name: "GoogleSignUp",
  data() {
    return {
      fbCollection: "users",
      name: this.$store.state.user.displayName,
      nickName: '',
      phoneNum: '',
      id: this.$store.state.user.email,
      password: '',
      comparePassword: '',
      autoHyphen: '',
      compare: '',
      openBtn: false,
      closeInput: false,
      randomStr: Math.random().toString(36).substring(2, 12)
    }
  },
  methods: {
    signup() {
      const self = this;
      const db = firebase.firestore();
      if ((self.nickName != '') && (self.phoneNum != '')) {
                db.collection(self.fbCollection)
                    .doc(self.$store.state.user.uid)
                    .set({
                      name: self.name,
                      nickName: self.nickName,
                      phoneNum: self.phoneNum,
                      id: '',
                      howLogin: 'google 로그인',
                      gmail: self.$store.state.user.email,
                      code: self.randomStr,
                      otherCode: [self.randomStr]
                    })
                alert('정보입력 완료!');
                this.$router.push('/mainMap');
        } else {
          alert('모든 항목을 입력해주세요')
          return false
        }

    },
    validateName(name) {
      const nameRegExp = /^[가-힣]{2,4}$/;
      if (!nameRegExp.test(name)) {
        alert("이름이 올바르지 않습니다.");
        this.name = ''
        return false;
      } else {
        return true; //확인이 완료되었을 때
      }
    },
    validateNickName(nickName) {
      const checkSpecial = /[~₩!@#$%^&*()+=,/?"':;'><]/gi;
      if (nickName.length < 2) {
        alert("닉네임은 최소 2글자 이상 10글자 이하입니다.")
        this.nickName = ''
        return false
      } else if (nickName.search(/\s/) !== -1) {
        alert("닉네임에 공백은 불가능합니다.")
        this.nickName = ''
        return false
      } else if (checkSpecial.test(nickName)) {
        alert(".과 _과 -를 제외한 특수문자는 사용할 수 없습니다.");
        this.nickName = ''
        return false;
      } else {
        return true; //확인이 완료되었을 때
      }
    },

    goMain() {
      this.$router.push('/')
    }
  },
}
</script>

<style scoped>
body {
  background-image: url("../assets/images/bgPhoto.jpg");
  background-size: cover;
}
.black-bg {
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  position: fixed;
  padding: 20px;
}
.white-bg {
  width: 60%;
  background: white;
  border-radius: 8px;
  padding: 50px;
  position: absolute;
  top: 17%;
  left: 24%;
  margin: -50px 0 0 -50px;
}
.ImButton {
  height: 38px !important;
  white-space: nowrap;
  margin: 0 0 0 10px !important;
  display: flex;
  align-items: center;
}
.input-line {
  display: flex;
  height: 38px;
}
</style>
