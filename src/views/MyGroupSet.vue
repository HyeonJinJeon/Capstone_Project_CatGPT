<template>
  <div class="backgroundImg">
    <div class="black-bg">
      <div class="title">
        <span style="font-size:60px;">Group Setting</span>
        <br><br><br><br>
      </div>
      <div class="center">
        <div class="white-bg">
          <p class="h4 text-center mb-4" style="color: black">그룹 설정</p>
          <hr>
          <div style="margin-top:50px;">
            <h3 class="h4 mb-4" style="color: black;">
              그룹 생성
            </h3>
            <div class="input-line">
              <input v-model="groupName" type="text" class="form-control" placeholder="생성할 그룹 이름을 입력해주세요"/>
              <button class="confirmBtn" type="submit" @click="newGroup">등록</button>
            </div>
          </div>

          <div style="margin-top: 100px;">
            <h3 class="h4 mb-4" style="color: black;">
              기존 그룹이 있다면
            </h3>
            <div class="input-line">
              <input v-model="enterCode" type="text" class="form-control" placeholder="입장코드를 입력해주세요."/>
              <button class="confirmBtn" type="submit" @click="existGroup">등록</button>
            </div>
          </div>
        </div>
        <div class="groupList">
          <ShowGroup></ShowGroup>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import {firebase} from "@/firebase/firebaseConfig";
import ShowGroup from "@/components/ShowGroup.vue";

export default {
  name: "GroupMaster",
  components: {ShowGroup},
  data() {
    return {
      fbCollection: "users",
      userId: this.$store.state.user.uid,
      groupName: "",
      newCode: '',
      enterCode: "",
      userInfo: [],
      groupInfo: [],
      randomStr: Math.random().toString(36).substring(2, 12),
      enterCodes: [],
      groups: [],
      ownerCheck: false,
      alreadyEnroll: false,
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
      self.newCode = self.randomStr;
    },
    getData() {
      const self = this;
      // console.log(userId)
      const db = firebase.firestore();
      db.collection(self.fbCollection)
          .doc(self.userId)
          .get()
          .then((snapshot) => {
            self.userInfo = snapshot.data();
            self.groups.push(self.userInfo.groups);
            for (let i = 0; i <= self.groups.length; i++) {
              self.enterCodes.push(self.groups[0][i].enterCode);
            }
            console.log("enterCodes", self.enterCodes)

          })
    },
    newGroup() {
      const self = this;
      // console.log(self.userId)
      const db = firebase.firestore();
      const _data = {
        uid: self.userId,
        name: self.userInfo.name,
      }
      const _data2 = {
        enterCode: self.newCode,
        groupName: self.groupName,
      }
      db.collection("group")
          .add({
            groupName: self.groupName,
            member: firebase.firestore.FieldValue.arrayUnion(_data),
            enterCode: self.newCode,
            owner: self.$store.state.user.uid,
          })
          .then(() => {
            db.collection(self.fbCollection)
                .doc(self.userId)
                .update({groups: firebase.firestore.FieldValue.arrayUnion(_data2)})
                .then(() => {
                  alert("그룹 생성완료")
                  delete localStorage.groupCode
                  delete localStorage.groupName
                  localStorage.groupCode = _data2.enterCode
                  localStorage.groupName = _data2.groupName
                  self.$router.go();
                })
          })
    },
    existGroup() {
      const self = this;
      const db = firebase.firestore();
      db.collection("group")
          .where("enterCode", '==', self.enterCode)  //그룹들의 입장코드와 입력된 입장코드를 비교
          .get()
          .then((querySnapshot) => {
            if (querySnapshot.size === 0) {     //없다면 알림창으로 알려주고 입장코드가 등록되지 않음
              alert("존재하지않는 입장코드입니다.")
            }
            querySnapshot.forEach((doc) => {  //있다면 groupInfo에 그룹 정보를 저장하고 setGroupMember() 호출
              const _data = doc.data();
              _data.id = doc.id
              self.groupInfo = _data;
              for (let i = 0; i < self.enterCodes.length; i++) {
                if (self.enterCodes[i] == self.enterCode) {
                  self.alreadyEnroll = true;
                  alert("이미 등록된 코드입니다.")
                  self.enterCode='';
                }
              }
              if(self.alreadyEnroll == false) {
                self.setGroupMember();
              }
            });

          })
    },
    setGroupMember() {    //기존 그룹 등록할 때 users와 group에 정보 넣어주는 함수
      const self = this;
      const db = firebase.firestore();
      const _data1 = {
        enterCode: self.enterCode,
        groupName: self.groupInfo.groupName,
      }
      const _data2 = {
        uid: self.userId,
        name: self.userInfo.engName,
      }
      db.collection("users")    //users에 등록한 그룹 정보 저장
          .doc(self.userId)
          .update({groups: firebase.firestore.FieldValue.arrayUnion(_data1)})
          .then(() => {
            db.collection("group")    //group에 유저 정보 저장
                .doc(self.groupInfo.id)
                .update({member: firebase.firestore.FieldValue.arrayUnion(_data2)})
            alert("등록 완료!")
          })

    },

  }
}
</script>

<style scoped>
.backgroundImg {
  background-color: rgba(0, 0, 0, 0.5);
  height: 100vh;
  width: 100%;
  background-size: cover;
}

.black-bg {
  width: 100%;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  position: fixed;
}

.center {
  position: absolute;
  left: 15%;
  width: 90%;
  margin: auto;
}

.title {
  font-style: normal;
  font-weight: 700;
  margin-top: 100px;
  color: #FFFFFF;
  text-shadow: 0px 8px 4px rgba(0, 0, 0, 0.25);
}

.white-bg {
  position: absolute;
  width: 45%;
  height: 500px;
  align: center;
  background-color: white;
  border-radius: 8px;
  padding: 50px;
  margin: 0 auto;
}

.input-line {
  display: flex;
  height: 38px;
}

.confirmBtn {
  font-weight: 500;
  font-size: 15px;
  width: 110px;
  height: 38px;
  border: none;
  background-color: #2c3e50;
  border-radius: 2px;
  color: white;
}

.groupList {
  position: absolute;
  background-color: rgba(255, 255, 255, 0.2);
  align: center;
  float: right;
  width: 25%;
  height: 500px;
  right: 20%;
  padding: 20px;
  border-radius: 15px;
  margin: 0 auto;
}
</style>
