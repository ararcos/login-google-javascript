// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getDatabase, ref, onValue, remove } from 'firebase/database';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDTIi0NZlJT-Zg29UWKC9GJcR0qKu0jxA0",
  authDomain: "test-reser.firebaseapp.com",
  databaseURL: "https://test-reser-default-rtdb.firebaseio.com",
  projectId: "test-reser",
  storageBucket: "test-reser.appspot.com",
  messagingSenderId: "78756035714",
  appId: "1:78756035714:web:75635f29e70116906b089b",
  measurementId: "G-WD13C8GHLV"
};

// Initialize Firebase
initializeApp(firebaseConfig);
var database = getDatabase();
var today = new Date();
var todayString =  today.toISOString().split('T')[0];
const queryQuito = ref(database, 'quito' + '/' + todayString);
onValue(queryQuito, (snapshot) => {
    const data = snapshot.val();
    for (let val in data) {
        if(data[val].endAt){
            today = new Date();
            const day = new Date(`${todayString} ${data[val].endAt}:00`);
                if(day <= today){
                    remove(ref(database, 'quito' + '/' + todayString + '/' + val));
                    console.log(`Reservacion ${val} eliminada`);
            }
        }
    }
});