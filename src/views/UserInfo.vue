<template>
<div>
  <h4><b style="margin: 10px">{{userInfo.nickName}}</b></h4>
  <button class="btn-mdb-color" @click="confirmEdit">
    <b-icon icon="pencil-fill" aria-hidden="true"></b-icon> Settings
  </button>
  <!--        <b-icon icon="pencil-fill" font-scale="1" @click="editInfo"></b-icon>-->

  <div>
    <label for="name" class="grey-text" style="margin:10px">Name</label>
    <input v-model="userInfo.name" type="text" id="name" class="form-control" >
    <label for="name" class="grey-text" style="margin:10px">Phone</label>
    <input v-model="userInfo.phoneNum" type="text" id="name" class="form-control">
    <label for="name" class="grey-text" style="margin:10px">로그인 방식</label>
    <input v-model="userInfo.howLogin" type="text" id="name" class="form-control" disabled/>
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
        // gmail: self.userInfo.gmail,

      }
      db.collection(self.fbCollection)
          .doc(self.userId)
          .set(_data, {merge: true} )
          .then(() => {
            alert("수정 완료!")
          })
    },
    codeInput() {   //입장코드 등록 함수
      const self = this;
      const db = firebase.firestore();
      // const _data = {
      //   otherCode: self.codeAdd,
      // }
      db.collection("users")
          .where("code",'==',self.codeAdd)  //유저들의 입장코드와 입력된 입장코드를 비교
          .get()
          .then((querySnapshot) => {
            if (querySnapshot.size === 0) {     //없다면 알림창으로 알려주고 입장코드가 등록되지 않음
              alert("존재하지않는 입장코드입니다.")
            }else { //있다면 입장코드를 배열로 저장
              db.collection("users")
                  .doc(self.userId)
                  .update({otherCode: firebase.firestore.FieldValue.arrayUnion(self.codeAdd)})
                  .then(() => {
                    alert("등록 완료!")
                    this.$router.go();
                  })
            }
          })

    },
    goOtherMap(otherCode){    //다른사람 맵으로 이동
      localStorage.otherCode = otherCode
      this.$router.push('/otherMap')
    },

    // getDatalist() {
    //   const self = this;
    //   const db = firebase.firestore();
    //   console.log(self.whatData)
    //   db.collection("memory")
    //       .where("userId",'==',self.$store.state.user.uid)
    //       .get()
    //       .then((querySnapshot) => {
    //         if (querySnapshot.size === 0) {
    //           self.whatData = true
    //           console.log(self.whatData)
    //         }
    //         querySnapshot.forEach((memory) => {
    //           const _data = memory.data();
    //           _data.id = memory.id
    //           self.memoryList.push(_data);
    //           console.log(self.memoryList)
    //         });
    //       })
    // },

  },
}

</script>

<style scoped>

</style>