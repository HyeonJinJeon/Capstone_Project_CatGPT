<template>
  <div v-if="modal === true" class="black-bg">
    <div class="white-bg">
      <input type="text" v-model="chatName" placeholder="채팅방 이름을 작성해주세요">
      <button class="addBtn" @click="sendData">추가</button>
      <button class="closeBtn" @click="$emit('closeModal')">닫기</button>
    </div>
  </div>
</template>

<script>

export default {
  name: 'AddChat',
  data() {
    return {
      chatName: ''
    }
  },
  watch : {

  },
  props : {
    modal : Boolean,
  },
  created() {

  },
  mounted() {

  },
  methods: {
    sendData(){
      this.$emit('childData',this.chatName)
    }
  }
}

</script>

<style scoped>

body {
  margin : 0;
}

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
