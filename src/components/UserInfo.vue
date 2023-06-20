<template>
  <div v-if="userInfoModal === true" class="black-bg">
    <div class="white-bg">
      <br>
    <h4><b style="margin: 10px">회원정보 수정</b></h4>
      <br>
      <label for="name" class="grey-text" style="margin:10px">Name</label>
    <div style="display: flex; justify-content: center; align-items: center;">
      <input v-model="userInfo.name" style="width: 400px;" type="text" id="name" class="form-control" >
    </div>
      <label for="name" class="grey-text" style="margin:10px">Phone</label>
    <div style="display: flex; justify-content: center; align-items: center;">
      <input v-model="userInfo.phoneNum" style="width: 400px;" type="text" id="name" class="form-control">
    </div>
      <label for="name" class="grey-text" style="margin:10px">로그인 방식</label>
    <div style="display: flex; justify-content: center; align-items: center;">
      <input v-model="userInfo.howLogin" style="width: 400px;" type="text" id="name" class="form-control" disabled/>
    </div>
      <br><br>
      <button class="btn btn-indigo" style="color: white" @click="confirmEdit">
        <b-icon icon="pencil-fill" aria-hidden="true"></b-icon> 수정완료
      </button>
      <button class="btn btn-indigo" style="color: white" @click="$emit('closeModal')">닫기</button>
    </div>
  </div>
</template>

<script>
import {firebase} from "@/firebase/firebaseConfig";

export default {
  name: "userInfo",

  data() {
    return {
      fbCollection: 'users',
      userInfo: [],
      memoryList: [],
      whatData : false,
      googleEmail: '',
      connCode: false,
      otherCodes: [],
      userId: this.$store.state.user.uid,
      codeAdd: '',
    }
  },
  mounted() {
    const self = this;
    self.init();
  },
  methods: {
    init() {
      const self = this;
      self.getData();
    },
    getData() {
      const self = this;
      const db = firebase.firestore();
      db.collection(self.fbCollection)
          .doc(self.$store.state.user.uid)
          .get()
          .then((snapshot) => {
            self.userInfo = snapshot.data();
            if(self.userInfo.otherCode.length> 1) {
              self.connCode = true
            }
            for(var i = 0; i < self.userInfo.otherCode.length; i++) {   //otherCodes에 자신의 입장코드를 제외한 다른사람들의 입장코드를 저장
              if(self.userInfo.otherCode[i] != self.userInfo.code) {
                self.otherCodes.push(self.userInfo.otherCode[i])
              }
            }

          })
    },
    confirmEdit() {   //버튼 클릭시 수정된 유저정보가 firebase에 저장됨
      const self = this;
      const db = firebase.firestore();

      const _data = {
        name: self.userInfo.name,
        phoneNum: self.userInfo.phoneNum,
      }
      db.collection(self.fbCollection)
          .doc(self.userId)
          .set(_data, {merge: true} )
          .then(() => {
            alert("수정 완료!")
            this.$router.go();
          })
    },
  },
  props : {
    userInfoModal : Boolean,
  },
}

</script>

<style scoped>
.black-bg {
  width: 100%; height: 100vh;
  background: rgba(0,0,0,0.5);
  position: absolute; padding: 20px;
}

.white-bg {
  width: 700px; background: white;
  height: 500px;
  border-radius: 8px;
  position: absolute;
  top: 50%;
  left: 60%;
  transform: translate(-50%, -50%);
}
</style>