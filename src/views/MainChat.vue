<template>
  <div>
    <AddChat v-if="modal" @childData="chatName=$event, newChat()" @closeModal ="modal = false" :modal="modal"></AddChat>
    <div class="side">
      <button @click="modal=true">새로운 채팅</button>
      <table class="table" border="1" style="margin-left: auto; margin-right: auto; color: white">
        <thead>
        <tr>
        </tr>
        </thead>
        <tbody>
        <tr @click="changeChat(i)" v-for="(chatList,i) in chatList" :key="i">
          <td>{{chatList}}</td>
        </tr>
        </tbody>
      </table>
    </div>

  <div class="chat">
    <div class="messages" id="messages">
      <div v-if="messages.length==0" class="noMessage">
        <h1>Cat-GPT</h1>
        <p>채팅을 시작하세요</p>
      </div>
      <div v-for="message in messages.chatArr" :key="message.id">
        <div v-if="message.userName=='Cat-GPT'" class="CatGPTMessage">
          {{ message.userName }}: &nbsp;&nbsp;&nbsp;&nbsp;{{ message.content }}
        </div>
        <div v-if="message.userName!='Cat-GPT'" class="myMessage">
          {{ message.userName }}: &nbsp;&nbsp;&nbsp;&nbsp;{{ message.content }}
        </div>
      </div>
    </div>
    <div class="input">
      <input type="text" v-model="message" placeholder="메시지 입력" v-on:keypress.enter.prevent=sendMessage>
      <button @click="sendMessage(message)">전송</button>
    </div>
  </div>
  </div>
</template>

<script>
import {firebase} from "@/firebase/firebaseConfig";
import axios from "axios";
import AddChat from "@/components/AddChat.vue";
import addChat from "@/components/AddChat.vue";

export default {
  computed: {
    addChat() {
      return addChat
    }
  },
  components: {AddChat},
  data() {
    return {
      modal: false,
      chatName: '',
      chatList: [],
      selectedChat: '',
      chatId: [],
      selectedChatId: '',
      messages: [],
      message: '',
      cnt: -1
    }
  },
  mounted() {
    this.getChatList()
  },
  methods: {
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
          .where("groupName", '==', 'CATS')
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
        groupName: 'CATS',
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
      const data ={
        text: this.message
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
          .then(() => {
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
    }
  }
}
</script>

<style>
.chat {
  display: flex;
  flex-direction: column;
  margin-left: 40vh;
  height: 100%;
}

.side {
  position: absolute;
  background-color: #2c3e50;
  width: 40vh;
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
  background-color: #cfd9df;
  padding: 30px;
  text-align: left;
}

.myMessage {
  padding: 30px;
  text-align: left;
}

.messages {
  height: 93vh;
  flex-grow: 1;
  overflow-y: scroll;
  padding: 10px;
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
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.input button:hover {
  background-color: #3e8e41;
}
</style>