<template>
  <div v-if="docModal === true" class="black-bg">
    <div class="white-bg">
      <br>
      <h4><b style="margin: 10px">문서집 생성 및 문서 업로드</b></h4>
      <br>
      <label for="folderName" class="grey-text" style="margin:10px">새로운 문서집 추가</label> <br>
      <div style="display: flex; justify-content: center; align-items: center;">
        <input class="form-control" v-model="setFolder" type="text" id="folderName" style="width: 23vh" placeholder="문서집 이름 작성">
        <button class="btn btn-indigo" style="color: white" @click="addFolder" >새로운 문서집 추가</button>
      </div>
      <br>
      <br>
      <label for="uploadFile" class="grey-text" style="margin:10px">문서 저장</label> <br>
      <select class="form-select form-select-lg mb-3" style="width: 23vh; display: inline-block;" v-model="folderName">
        <option selected disabled hidden value="">문서집을 선택해주세요</option>
        <option
            v-for="(folderName) in folderNames"
            :key="folderName"
            v-text="folderName"
            :value="folderName">
        </option>
      </select>
      <br>
      <!--  <input name="file" type="file" class="form-control" ref="fileInput" accept=".hwp,.doc,.docx,.pdf" id="uploadFile"  multiple>-->
      <div style="display: flex; justify-content: center; align-items: center;">
        <input type="file" class="form-control" style="width: 23vh;" multiple @change="onFileChange">
      </div>
      <br>
      <button class="btn btn-indigo" style="color: white" @click="uploadFiles">업로드 하기</button>

      <button class="btn btn-indigo" style="color: white" @click="$emit('closeModal')">닫기</button>
    </div>
  </div>
</template>
<script>
import {firebase} from "@/firebase/firebaseConfig";
import axios from "axios";

export default {
  name: "UploadDoc",
  data() {
    return {
      userId: this.$store.state.user.uid,
      userName: this.$store.state.user.displayName,
      selected:'',
      setFolder: '',
      groupName: localStorage.groupName,
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
    addFolder() {
      const self = this;         // self를 쓰는 이유는 바깥의 this들과 햇갈리지 않기 위해서
      const db = firebase.firestore();
      const _data = {            // data()에 있는 데이터가 바로 들어갈 수 없다.
        folderName: self.setFolder,
        groupName: localStorage.groupName,
        userName: self.userName
      }
      db.collection(self.fbCollection) //<- collection('컬랙션명') 바로 쓸수있다.
          .add(_data)
          .then(() => {            // 아무 문제없이 윗쪽 코드가 다 성공하면 then이 실행
            alert("저장되었습니다")
            this.$router.go();
          })  // 성공하면 무엇을 할건지 정하면 된다/ 이 코드에선 alert가 실행된다
          .catch((e) => {          // 실패하면 catch가 실행된다. e는 errer의 약자
            console.log(e)
            alert("저장에 실패했습니다.")
            this.$router.go();
          })
    },
    onFileChange(event) {
      this.files = event.target.files
    },
    async uploadFiles() {
      const formData = new FormData()
      for (let i = 0; i < this.files.length; i++) {
        formData.append('files', this.files[i])
      }
      formData.append('text', this.groupName + this.folderName)
      console.log(this.folderName)
      try {
        const response = await axios.post('http://localhost:8002/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        alert("저장되었습니다")
        console.log(response.data)
      } catch (error) {
        console.log(error)
      }
    }
  },
  props : {
    docModal : Boolean,
  },
}
</script>

<style scoped>
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