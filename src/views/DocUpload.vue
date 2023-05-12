<template>
<div>
  <label for="folderName" class="grey-text" style="margin:10px">폴더 추가</label> <br>
  <input v-model="setFolder" type="text" id="folderName">
  <select class="form-select form-select-lg mb-3" style="width: 23vh; display: inline-block;" v-model="selected">
    <option selected disabled hidden value="">폴더를 선택해주세</option>
    <option
        v-for="(folderName) in folderNames"
        :key="folderName"
        v-text="folderName"
        :value="folderName"
        @mousedown="changeFolder(selected)">
    </option>
  </select>
  <label for="uploadFile" class="grey-text" style="margin:10px">문서 저장</label> <br>
  <input name="file" type="file" class="form-control" ref="fileInput" accept=".hwp,.doc,.docx,.pdf" id="uploadFile"  multiple>
  <button @click="uploadFile">업로드 하기</button>
</div>
</template>

<script>
import {firebase} from "@/firebase/firebaseConfig";
import axios from "axios";

export default {
  name: "docUpload",
  data() {
    return {
      userId: this.$store.state.user.uid,
      userName: this.$store.state.user.displayName,
      selected:'',
      setFolder: '',
      firstGroupName: localStorage.groupName,
      fbCollection: 'documents',
      folderName: '',
      folderNames: [],
      docData: [],
    }
  },
  mounted() {
    this.getData()
  },
  methods: {
    getData() {
      const self = this;
      const db = firebase.firestore();
      db.collection(self.fbCollection)
          .where('groupName', '==', localStorage.groupName)
          .where('userName', '==', this.userName)
          .get()
          .then((querySnapshot) => {
            querySnapshot.forEach((doc) => {
              const _data = doc.data();
              self.folderNames.push(_data.folderName);
              console.log(self.groupName)
            });
          })
    },
    uploadFile() {
      const formData = new FormData();
      formData.append('file', this.file);
      axios.post('http://localhost:8002/upload', formData,{
        "index_name": this.folderName + this.firstGroupName
      }, {
        headers: {
          'Content-Type': 'multipart/form-data'
      }
      })
          .then(response => {
            console.log(response.data);
            alert("업로드 완료")
          })
          .catch(error => {
            console.log(error);
          });
    },
    changeFolder() {

    }
  }
}
</script>

<style scoped>

</style>