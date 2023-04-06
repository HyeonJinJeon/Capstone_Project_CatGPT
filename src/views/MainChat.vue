<template>
  <div class="chat">
    <div class="messages">
      <div v-for="message in messages" :key="message.id">
        <div>{{ message.name }}: {{ message.content }}</div>
      </div>
    </div>
    <div class="input">
      <input type="text" v-model="message" placeholder="메시지 입력">
      <button @click="sendMessage">전송</button>
    </div>
  </div>
</template>

<script>
import {firebase} from "@/firebase/firebaseConfig";


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
    sendMessage() {
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
      this.message = ''
    }
  }
}
</script>

<style>
.chat {
  display: flex;
  flex-direction: column;
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