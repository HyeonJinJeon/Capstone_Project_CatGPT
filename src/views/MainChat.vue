<template>
  <div>
    <AddChat v-if="modal" @childData="chatName=$event, newChat()" @closeModal ="modal = false" :modal="modal"></AddChat>
    <UploadDoc v-if="docModal" @closeModal ="docModal = false" :docModal="docModal"></UploadDoc>
    <UserInfo v-if="userInfoModal" @closeModal ="userInfoModal = false" :userInfoModal="userInfoModal"></UserInfo>
    <div class="side">
      <div>
        <br>
        <h3 style="color: #FFFFFF;">
          {{ userInfo.name }}
          <span>
<!--            <button class="logOutBtn" @click="logout">Logout</button>-->
          </span>
          <br>

        </h3>
        <h6 style="color: #FFFFFF;">
          현재 그룹 : {{firstGroupName}}
          <br>
          현재 문서집 : {{folderName}}
        </h6>
        <hr style="color: white;">
      </div>

      <select class="form-select form-select-lg mb-3" style="width: 23vh; display: inline-block;" v-model="selected">
        <option selected disabled hidden value="">그룹을 설정해주세요</option>
        <option
            v-for="(groupName, i) in groupNames"
            :key="groupName"
            v-text="groupName"
            :value="enterCodes[i]">
        </option>
      </select>
      <span> <button class="btn-outline-light-blue" @click="groupChange(selected)" style="margin-left: 1vh; width: 9vh; height: 5vh; border-radius: 10px">그룹 변경</button></span> <br>

      <select class="form-select form-select-lg mb-3" style="width: 23vh; display: inline-block;" v-model="selectedFolder">
        <option selected disabled hidden value="">문서집을 설정해주세요</option>
        <option
            v-for="(folderName) in folderNames"
            :key="folderName"
            v-text="folderName"
            :value="folderName">
        </option>
      </select>
      <span> <button class="btn-outline-light-blue" @click="changeFolder(selectedFolder)" style="margin-left: 1vh; width: 9vh; height: 5vh; border-radius: 10px">폴더 변경</button></span> <br>

      <button class="btn-outline-light-blue" style="border-radius: 10px; width: 33vh; height: 7vh; color: white; font-size: 20px; margin-bottom: 3vh" @click="modal=true">
        <i class="fas fa-comment-medical"></i> 새로운 채팅
      </button>
      <div class="sideTable" style="height:22vh; overflow:auto;">
        <table class="table" border="0" style="margin-left: auto; margin-right: auto; color: white; border-top-color:#061524;  border-color: #061524; border-radius: 10px;">
          <thead>
          <tr>
          </tr>
          </thead>
          <tbody style="max-height: 100px; overflow-y: auto;">
          <tr @click="changeChat(i)" v-for="(chatList,i) in chatList" :key="i">
            <td style="text-align: left; padding-left: 2vh">
              <i class="far fa-comment fa-lg" style="padding-right: 2vh"></i>
              <span style="font-size: 15px">{{chatList}}</span>
              <i class="fas fa-trash-can fa-lg"></i>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
      <div class="sideBottom">
        <br>
        <br>
        <p @click="userInfoModal = true">회원정보 수정</p>
        <br>
        <p @click="goGroupSet">그룹 관리</p>
        <br>
        <p @click="docModal = true">문서 업로드</p>
        <br>
        <p @click="logout">로그아웃</p>
        <br>
        <br>
        <p style="color:gray;">created by CATS</p>
      </div>
    </div>

  <div class="chat">
    <div class="messages" id="messages">
      <div v-if="messages.length==0" class="noMessage">
        <h1>Cat-GPT</h1>
        <p>채팅을 시작하세요</p>
      </div>
      <div class="existMessage" v-for="message in messages.chatArr" :key="message.id">
        <div v-if="message.userName=='Cat-GPT'" class="CatGPTMessage">
          <img src="../assets/images/catGPT.jpg" height="40px" width="40px"/>
          : &nbsp;&nbsp;&nbsp;&nbsp;{{ message.content }}
        </div>
        <div v-if="message.userName!='Cat-GPT'" class="myMessage">
           {{ message.content }}&nbsp;&nbsp;&nbsp;&nbsp; : {{ message.userName }}
        </div>
      </div>
    </div>
    <div v-if="messages.length!=0" class="input">
      <input type="text" v-model="message" placeholder="메시지 입력" v-on:keypress.enter.prevent=sendMessage>
      <button id="sendBtn" @click="sendMessage(message)">전송</button>
    </div>
  </div>
  </div>
</template>

<script>
import {firebase} from "@/firebase/firebaseConfig";
import axios from "axios";
import AddChat from "@/components/AddChat.vue";
import addChat from "@/components/AddChat.vue";
import UploadDoc from "@/components/UploadDoc.vue";
import UserInfo from "@/components/UserInfo.vue";

export default {
  computed: {
    addChat() {
      return addChat
    }
  },
  components: {UserInfo, UploadDoc, AddChat},
  data() {
    return {
      userId: this.$store.state.user.uid,
      userName: this.$store.state.user.displayName,
      fbCollection: 'users',
      modal: false,
      docModal: false,
      userInfoModal: false,
      selected:'',
      firstGroupName: localStorage.groupName,
      groups: [],
      userInfo: [],
      groupNames: [],
      groupName: [],
      enterCodes: [],
      folderName: localStorage.folderName,
      selectedFolder: '',
      folderNames: [],
      chatName: '',
      chatList: [],
      selectedChat: '',
      chatId: [],
      selectedChatId: '',
      messages: [],
      message: '',
      indexName: localStorage.indexName,
      cnt: -1
    }
  },
  mounted() {
    this.getChatList()
    this.getFolderName()
    this.getData()
  },
  methods: {
    getData() {
      const self = this;
      const db = firebase.firestore();
      db.collection(self.fbCollection)
          .doc(self.userId)
          .get()
          .then((snapshot) => {
            self.userInfo = snapshot.data();
            self.groups.push(self.userInfo.groups);
            // console.log(self.groups.length)
            for(let i=0; i < self.groups[0].length; i++) {
              // for(let j=0; j < self.groups[i].length; i++) {
              self.groupNames.push(self.groups[0][i].groupName);
              self.enterCodes.push(self.groups[0][i].enterCode)
            }
            // console.log(self.groupNames)
            // console.log(self.enterCodes)
            // }
          })
    },
    getGroupName() {
      const self = this;
      const db = firebase.firestore();
      db.collection("group")
          .where("groupCode", "==", localStorage.groupCode)
          .get()
          .then(async (querySnapshot) => {
            if (querySnapshot.size === 0) {
              return
            }
            querySnapshot.forEach((doc) => {
              const _data = doc.data();
              _data.id = doc.id
              // const date = new Date(_data.date.seconds * 1000);
              // _data.date = getDate(date);
              self.groupName.push(_data.groupName);
              console.log(self.groupName)
            });
          })
    },
    getFolderName() {
      const self = this;
      const db = firebase.firestore();
      db.collection("documents")
          .where("groupName", "==", self.firstGroupName)
          .where("userName", "==", self.userName)
          .get()
          .then(async (querySnapshot) => {
            if (querySnapshot.size === 0) {
              return
            }
            querySnapshot.forEach((doc) => {
              const _data = doc.data();
              _data.id = doc.id
              // const date = new Date(_data.date.seconds * 1000);
              // _data.date = getDate(date);
              self.folderNames.push(_data.folderName);
              console.log(self.folderNames)
            });
          })
    },
    changeFolder(folderName){
      localStorage.folderName = folderName
      this.indexName = localStorage.groupName + folderName;
      localStorage.indexName = this.indexName
      this.$router.go();
    },
    async groupChange(selected) {    //현재 그룹 변경
      const self = this;
      await this.getGroupName()
      console.log(this.groupName[0])

      for(let i =0; i<self.groups[0].length; i++) {
        if(self.enterCodes[i] == selected) {
          localStorage.groupName = self.groupNames[i]
          localStorage.groupCode = self.enterCodes[i]
        }
      }
      delete localStorage.indexName
      localStorage.folderName = '문서집을 선택해주세요'
      console.log(this.indexName)
      this.$router.go();

    },
    changeChat(i){
      this.selectedChat = this.chatList[i]
      this.selectedChatId = this.chatId[i]
      console.log('111',this.selectedChat)
      console.log('222', this.selectedChatId)
      const db = firebase.firestore();
      db.collection("messages")
          .where("chatName", '==', this.selectedChat)
          .get()
          .then((querySnapshot) => {
            if (querySnapshot.size === 0) {
              return
            }
            querySnapshot.forEach((doc) => {
              this.messages = doc.data();
              console.log(this.messages)
            });
            this.scrollToBottom()
          })
    },
    getChatList(){
      const self = this;
      const db = firebase.firestore();
      db.collection("messages")
          .where("groupName", '==', this.firstGroupName)
          .where("myName", '==', this.userId)
          .get()
          .then((querySnapshot) => {
                if (querySnapshot.size === 0) {
                  console.log('채팅 없음')
                }
                querySnapshot.forEach((doc) => {
                  const _data = doc.data();
                  _data.id = doc.id
                  self.chatId.push(_data.id);
                  console.log("아이디 확인", self.chatId)
                  self.chatList.push(_data.chatName);
                });
          })
      console.log(this.chatList)
    },
    newChat(){
      const db = firebase.firestore();
      const _data = {            // data()에 있는 데이터가 바로 들어갈 수 없다.
        chatName: this.chatName,
        groupName: this.firstGroupName,
        myName: this.userId,
        chatArr: [
          {
            content: '채팅을 시작해주세요',
            createdAt: new Date(),
            userName: 'Cat-GPT',
          }
        ]
      }
      db.collection('messages')
          .add(_data)
          .then(() => {
            this.chatList=[]
            this.chatId=[]
            this.getChatList()
            this.modal = false;
          })
    },
    sendMessage(message) {
      console.log(message)
      const target = document.getElementById('sendBtn');
      target.disabled = true;
      const data ={
        text: this.message,
        index_name: this.indexName
      }
      const path = `${'http://127.0.0.1:8002'}/chat`;
      axios
          .post(path, JSON.stringify(data), {
            headers: {
              "Content-Type": 'application/json',
            },
          }).then((res) => {
        console.log('111',res.data["result"])
        this.saveMyMessage(res.data)
      })
          .catch(error => {
            // eslint-disable-next-line
            console.log(error);
          });
    },
    saveMyMessage(res) {
      const db = firebase.firestore();
      if (this.message.trim() === '') {
        return
      }
      // const { displayName, uid } = auth.currentUser
      db.collection('messages')
          .doc(this.selectedChatId)
          .update({
            chatArr: firebase.firestore.FieldValue.arrayUnion({
              userName: this.$store.state.user.displayName,
              content: this.message,
              createdAt: new Date(),
            })
            // uid: this.uid
          })
          .then(async () => {
            this.saveGptMessage(res)
            this.created()
          })
      this.message = ''
    },
    created() {
      const db = firebase.firestore();
      db.collection('messages')
          .doc(this.selectedChatId)
          .onSnapshot(snapshot => {
            this.messages = snapshot.data()
            console.log('33', this.messages)
            const target = document.getElementById('sendBtn');
            target.disabled = false;
            // `this.messages` 값 업데이트 후, 이후 로직 처리
          })
    },
    scrollToBottom() {
      const element = document.getElementById('messages');
      element.scrollTop = element.scrollHeight - element.offsetHeight;
    },
    saveGptMessage(res) {
      console.log('222', res)
      const db = firebase.firestore();
      // const { displayName, uid } = auth.currentUser
      db.collection('messages')
          .doc(this.selectedChatId)
          .update({
            chatArr: firebase.firestore.FieldValue.arrayUnion({
              userName: 'Cat-GPT',
              content: res,
              createdAt: new Date(),
            })
            // uid: this.uid
          }).then(
          this.scrollToBottom
      )
      this.message = ''
    },
    // goUserInfo() {
    //   this.$router.push('/userInfo')
    // },
    goGroupSet() {
      this.$router.push('/myGroupSet')
    },
    // goDocUpload() {
    //   this.$router.push('/docUpload')
    // },
    logout() {
      delete localStorage.groupCode
      delete localStorage.groupName
      firebase.auth().signOut()
      this.$router.push('/')
    }
  }
}
</script>

<style>
.chat {
  display: flex;
  flex-direction: column;
  margin-left: 35vh;
  height: 100%;
}

.side {
  position: absolute;
  background-color: #0e2842;
  width: 35vh;
  height: 100vh;
}

.noMessage {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.CatGPTMessage {
  background-color: #f6f6f6;
  padding-top: 30px;
  padding-bottom: 30px;
  /*padding-left: 35vh;*/
  /*padding-right: 35vh;*/
  width: 750px;
  margin: 0 auto;
  text-align: left;
}

.myMessage {
  padding-top: 50px;
  padding-bottom: 50px;
  /*padding-left: 35vh;*/
  /*padding-right: 35vh;*/
  width: 750px;
  margin: 0 auto;
  text-align: right;
}

.messages {
  height: 93vh;
  flex-grow: 1;
  overflow-y: scroll;
  padding: 10px;
}

.existMessage{
  text-align: right;
}

.messages div {
  margin-bottom: 10px;
}

.messages div:nth-child(odd) {
  font-weight: bold;
  color: #666;
}

.input {
  width: 80vh;
  margin: auto;
  display: flex;
  align-items: center;
  padding: 10px;
}

.input input {
  flex-grow: 1;
  padding: 10px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  margin-right: 10px;
}

.input button {
  background-color: #0e2842;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.input button:hover {
  background-color: #0e2842;
}

.sideTable td:hover{
  background-color: #2c3e50;
  border-radius: 20px;
  cursor: pointer;
}

button:hover{
  background-color: #2c3e50;
}

.table td, .table th {
  padding: 0.75rem;
  vertical-align: top;
  border-top: 1px solid #061524;
}
.sideBottom{
  position: absolute;
  top: 60vh;
  background-color: #061524;
  color: white;
  width: 35vh;
  height: 40vh;
  border-top-left-radius: 30px;
  border-top-right-radius: 30px;
}
.sideBottom p:hover {
  color: gray;
  cursor: pointer;
}
/* 스크롤바의 전체 영역 */
.sideTable::-webkit-scrollbar {
  width: 10px; /* 스크롤바의 너비 */
}

/* 스크롤바의 트랙(배경) */
.sideTable::-webkit-scrollbar-track {
  background-color: #0e2842; /* 스크롤바의 배경색 */
}

/* 스크롤바의 색상 */
.sideTable::-webkit-scrollbar-thumb {
  background-color: #aaa; /* 스크롤바의 색상 */
  border-radius: 5px; /* 스크롤바의 모서리를 둥글게 만듦 */
}

/* 스크롤바가 활성화(마우스 클릭)된 상태 */
.sideTable::-webkit-scrollbar-thumb:hover {
  background-color: #999; /* 스크롤바의 색상 */
}

#sendBtn[disabled] {
  opacity: 0.1;
}

</style>