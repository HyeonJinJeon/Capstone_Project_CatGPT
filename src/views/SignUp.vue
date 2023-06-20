<template>
  <div class="backgroundImg">
    <div class="black-bg">
      <div class="white-bg">
        <p class="h4 text-center mb-4">회원가입 하기</p>
        <div>
          <label for="defaultFormRegisterNameEx" class="grey-text">이름</label>
          <input v-model="name" type="text" id="defaultFormRegisterNameEx" class="form-control" maxlength=10
                 @change="validateName(name)"/>
          <br>
        </div>
        <div>
          <label for="defaultFormRegisterNameEx" class="grey-text">닉네임</label>
          <input v-model="nickName" type="text" id="defaultFormRegisterNameEx" class="form-control" maxlength="10"
                 @change="validateNickName(nickName)"/>
          <br>
        </div>
        <div>
          <label for="defaultFormRegisterConfirmEx" class="grey-text">전화번호</label>
          <input v-model="phoneNum" type="text" id="defaultFormRegisterConfirmEx" class="form-control" maxlength="13"
                 oninput="javascript: this.value = this.value.replace(/[^0-9]/, '').replace(/^(\d{2,3})(\d{3,4})(\d{4})$/, `$1-$2-$3`);"/>
          <br>
        </div>
        <div>
          <label for="defaultFormRegisterEmailEx" class="grey-text">아이디</label>
          <div class="input-line">
            <input v-bind:disabled="closeInput==true" v-model="id" type="text" id="defaultFormRegisterEmailEx"
                   class="form-control" @change="validateId(id)" placeholder="영문자+숫자 조합" />
            <button class="btn btn-indigo" type="submit" @click="overlapCheckId(id)" style="color: white; width: 90px; height: 35px;">중복확인</button>
          </div>
          <br>
        </div>
        <div>
          <label for="defaultFormRegisterConfirmEx" class="grey-text">비밀번호</label>
          <input v-model="password" type="password" id="defaultFormRegisterConfirmEx" class="form-control"
                 @change="validatePw(password)" placeholder="영문자+숫자+특수문자 조합"/>
          <br>
        </div>
        <div>
          <label for="defaultFormRegisterPasswordEx" class="grey-text">비밀번호 확인</label>
          <input v-model="comparePassword" type="password" id="defaultFormRegisterPasswordEx" class="form-control"
                 @change="passwordConfirm" v-on:keypress.enter.prevent=signup>
          <h10>{{ compare }}</h10>
          <br>
        </div>
        <div class="text-center mt-4">
          <button class="btn btn-indigo" type="submit" @click="signup" style="color: white;">회원가입</button>
          <button class="btn btn-indigo" type="submit" @click="goMain" style="color: white;">뒤로가기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {firebase} from '@/firebase/firebaseConfig';
export default {
  name: "SignUp",
  data() {
    return {
      fbCollection: "users",
      name: "",
      nickName: '',
      phoneNum: '',
      id: '',
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
      if ((self.name != '') && (self.nickName != '') && (self.phoneNum != '') && (self.id != '') && (self.password != '') && (self.comparePassword != '')) {
        if (self.closeInput == true) {
          firebase.auth().createUserWithEmailAndPassword(this.id + '@timproject.co.kr', this.password)
              .then((result) => {
                let user = result.user;
                db.collection(self.fbCollection)
                    .doc(result.user.uid)
                    .set({
                      name: self.name,
                      nickName: self.nickName,
                      phoneNum: self.phoneNum,
                      id: self.id,
                      howLogin: '일반 로그인',
                      groups: [],
                      code: self.randomStr,
                      otherCode: [self.randomStr]
                    })
                alert('회원가입 완료!');
                user.updateProfile({displayName: self.name, photoURL: self.randomStr})
                // firebase.auth().signOut()
                this.$router.push('/');
              }).catch(err => {
            console.error(err);
            alert('에러 : ' + err.message)
          })
        } else {
          alert('아이디 중복을 확인해주세요')
          return false
        }
      } else {
        alert('모든 항목을 입력해주세요.')
        return false
      }
    },
    overlapCheckId(id) {
      const self = this;
      const db = firebase.firestore();
      db.collection(self.fbCollection)
          .where("id", "==", id)
          .get()
          .then((querySnapshot) => {
            console.log(querySnapshot.size)
            if (querySnapshot.size >= 1) {
              alert('중복된 아이디가 있습니다')
              self.id = ''
              self.openBtn = false
              self.closeInput = false
            } else {
              alert('사용 가능합니다')
              self.openBtn = true
              self.closeInput = true
            }
          })
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
    validateId(id) {
      let checkId = /[ㄱ-ㅎㅏ-ㅣ가-힣~₩!@#$%^&*()+._=,/?"':;'><]/
      if (id.length < 6) {
        alert("아이디는 최소 6자리 이상입니다.")
        this.id = ''
        return false
      } else if (id.search(/\s/) !== -1) {
        alert("아이디에 공백은 불가능합니다.")
        this.id = ''
        return false
      } else if (checkId.test(id)) {
        alert("올바른 아이디 형식이 아닙니다.");
        this.id = ''
        return false;
      } else {
        return true
      }
    },
    validatePw(pw) {
      let number = pw.search(/[0-9]/g);
      let english = pw.search(/[a-z]/ig);
      let specialCharacter = pw.search(/[`~!@@#$%^&*|₩₩₩'₩";:₩/?]/gi);
      if (pw.length < 8 || pw.length > 20) {
        alert("8자리 ~ 20자리 이내로 입력해주세요.");
        this.password = ''
        return false;
      } else if (pw.search(/\s/) !== -1) {
        alert("비밀번호는 공백 없이 입력해주세요.");
        this.password = ''
        return false;
      } else if (number < 0 || english < 0 || specialCharacter < 0) {
        alert("영문,숫자, 특수문자를 혼합하여 입력해주세요.");
        this.password = ''
        return false;
      } else {
        console.log("통과");
        return true;
      }
    },
    passwordConfirm() {
      if (this.password === this.comparePassword) {
        this.compare = '비밀번호가 일치합니다.'
        return true
      } else {
        this.compare = '비밀번호 일치하지 않습니다.'
        this.comparePassword = ''
      }
    },
    goMain() {
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
  top: 14%;
  left: 24%;
  margin: -50px 0 0 -50px;
  text-align: left;
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
