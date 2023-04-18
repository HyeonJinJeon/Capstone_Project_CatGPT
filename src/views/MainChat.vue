<template>
  <div>
    <div class="side">
    </div>
  <div class="chat">
    <div class="messages">
      <div v-for="message in messages" :key="message.id">
        <div>{{ message.name }}: {{ message.content }}</div>
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


export default {
  data() {
    return {
      messages: [],
      message: ''
    }
  },
  created() {
    const db = firebase.firestore();
    db.collection('messages')
        .orderBy('createdAt')
        .onSnapshot(snapshot => {
          this.messages = snapshot.docs.map(doc => ({
            id: doc.id,
            name: doc.data().name,
            content: doc.data().content
          }))
        })
  },
  methods: {
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
          .add({
            name: this.$store.state.user.displayName,
            content: this.message,
            createdAt: new Date(),
            // uid: this.uid
          })
          .then(() => {
            this.saveGptMessage(res)
          })
      this.message = ''
    },
    saveGptMessage(res) {
      console.log('222', res)
      const db = firebase.firestore();
      // const { displayName, uid } = auth.currentUser
      db.collection('messages')
          .add({
            name: 'Cat-GPT',
            content: res,
            createdAt: new Date(),
            // uid: this.uid
          })
      this.message = ''
    }
  }
}
</script>

<style>
.chat {
  display: flex;
  flex-direction: column;
  width: ;
  height: 100%;
}

.messages {
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