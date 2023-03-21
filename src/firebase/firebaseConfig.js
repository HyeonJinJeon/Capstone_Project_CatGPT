import firebase from 'firebase/app'
import 'firebase/auth'
import 'firebase/analytics'
import 'firebase/firestore'
import 'firebase/functions'
import 'firebase/storage';
import "firebase/firestore";
import "firebase/auth";

firebase.initializeApp({
    apiKey: "AIzaSyCEuKmQQIrglqkKH-EGhVHwirn6ZJjcQAY",
    authDomain: "catgpt-project-f2e04.firebaseapp.com",
    projectId: "catgpt-project-f2e04",
    storageBucket: "catgpt-project-f2e04.appspot.com",
    messagingSenderId: "411290520425",
    appId: "1:411290520425:web:2fe2caed8cd6241459cbf8",
    measurementId: "G-R847ECTN68"
});

firebase.auth().languageCode = 'ko'

const auth = firebase.auth()
const firestore = firebase.firestore()
const functions = firebase.app().functions('asia-northeast3')

export {auth, firestore, functions, firebase}