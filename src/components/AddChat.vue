<template>
  <div v-if="modal === true" class="black-bg">
    <div class="white-bg">
      <br>
      <h4><b style="margin: 10px">새로운 채팅</b></h4>
      <br><br><br><br><br><br><br>
      <div style="display: flex; justify-content: center; align-items: center;">
        <input class="form-control" type="text" v-model="chatName" style="width: 400px" placeholder="채팅방 이름을 작성해주세요">
      </div>
      <br><br><br><br><br><br><br>
      <button class="btn btn-indigo addBtn" style="color: white;" @click="sendData">추가</button>
      <button class="btn btn-indigo closeBtn" style="color: white" @click="$emit('closeModal')">닫기</button>
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
  props : {
    modal : Boolean,
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
