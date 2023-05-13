<template>
  <div class="firstDiv">
    <div style="overflow:auto;">
      <table class="table" style="margin-left: auto; margin-right: auto;">
        <thead>
        <tr></tr>
        </thead>
        <tbody>

        <tr v-for="(group,i) in groupNames" :key="i">
          <td style="font-weight: 400;"><span style="font-weight: bold">{{ group }}</span><br> 입장코드: {{ enterCodes[i] }}</td>
          <!--        <td><img class="img1" :src="memoryList.image"/></td>-->
          <i style="margin-top: 40px" class="fas fa-trash" @click="deleteGroup(group, enterCodes[i])"></i>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script>
import {firebase} from "@/firebase/firebaseConfig";

export default {
  name: "ShowGroup",
  data() {
    return {
      userId: this.$store.state.user.uid,
      userInfo: [],
      groupInfo: [],
      enterCodes: [],
      groupNames: [],
      groups: [],
      groupUid: ''
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
      db.collection("users")
          .doc(self.userId)
          .get()
          .then((snapshot) => {
            self.userInfo = snapshot.data();
            self.groups.push(self.userInfo.groups);
            self.groupNames = [];
            self.enterCodes = [];
            for(let i=0; i <= self.groups[0].length; i++) {
              self.groupNames.push(self.groups[0][i].groupName);
              // console.log("groupNames",self.groupNames)
              self.enterCodes.push(self.groups[0][i].enterCode)
              // console.log("enterCodes",self.enterCodes)
              // console.log("groups",self.groups)
            }
          })
    },
    async deleteGroup(group, enterCode) {
      // const self = this;
      // const db = firebase.firestore();
      const self = this;
      const db = firebase.firestore();
      await db.collection("group")
          .where('groupName', '==', group)
          .get()
          .then(async (querySnapshot) => {
            await querySnapshot.forEach((doc) => {
              // const _data = doc.data();
              self.groupUid = doc.id
              console.log(self.groupUid)
            });
          })
      await console.log(this.groupUid)
      const _data = {
        enterCode : enterCode,
        groupName : group
      }
      await db.collection('group')
          .doc(this.groupUid)
          .delete()
          .then(async () => {
            db.collection('users')
                .doc(this.userId)
                .update({
                  groups : firebase.firestore.FieldValue.arrayRemove(_data)
                })
                .then(() => {
                  db.collection('users')
                      .doc(this.userId)
                      .update({
                        // groups :
                      })
                })
            alert("삭제 완료")
            self.$router.go();
          })
    },
    getGroupUid(group){
      console.log('111',group)
      const self = this;
      const db = firebase.firestore();
      db.collection("group")
          .where('groupName', '==', group)
          .get()
          .then((querySnapshot) => {
            querySnapshot.forEach((doc) => {
              // const _data = doc.data();
              self.groupUid = doc.id
              console.log(self.groupUid)
            });
          })
    }
    // 그룹 uid 가져와야됨!!!!!!!!!! 그래야 그룹 삭제할 수 있음 그니까 이거 코드부터 작성할것
  },
}
</script>

<style scoped>

table {
  background-color: rgba(255,255,255,0.9);
  color: black;
}

.firstDiv {
  height: 450px;
  overflow: auto;
}

.white-bg {
  max-width: 700px;
  height: 500px;
  align: center;
  border-radius: 8px;
  padding: 50px;
  position: relative;
  /*top: 25%;*/
  /*left: 24vh;*/
  margin: 0 auto;
}

.groupList {
  position: relative;
  background-color: rgba(255, 255, 255, 0.2);
  float: right;
  width: 500px;
  height: 800px;
  right: 200px;
  top: 100px;
  /*overflow: auto;*/
  padding: 20px;
  border-radius: 15px;
}
</style>
