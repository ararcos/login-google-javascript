import { initializeApp,  } from "firebase/app";
import { getDatabase, ref, child, get, remove, goOffline } from "firebase/database";

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
const app = initializeApp(firebaseConfig);
var database = getDatabase();

async function deleteOffice() {
    var today = new Date();
    var todayString =  today.toISOString().split('T')[0];
    const queryQuito = ref(database);

    const snapshotQuito = await get(child(queryQuito, `quito/${todayString}`));
    const snapshotGuayaquil = await get(child(queryQuito, `guayaquil/${todayString}`));
    const snapshotLoja = await get(child(queryQuito, `loja/${todayString}`));
    const dataQuito = snapshotQuito.val();
    const dataGuayaquil = snapshotGuayaquil.val();
    const dataLoja = snapshotLoja.val();
    
    await deleteReservation(dataQuito, todayString, 'quito');

    await deleteReservation(dataGuayaquil, todayString, 'guayaquil');

    await deleteReservation(dataLoja, todayString, 'loja');

    goOffline(database);
}

function deleteReservation(data, todayString, office) {
    for (let val in data) {
        if(data[val].endAt){
            const today = new Date();
            const day = new Date(`${todayString}T${data[val].endAt}:00`);
            console.log(today);
            console.log(day);
            console.log(today.getTimezoneOffset());
            console.log(day.getTimezoneOffset());
            // if(day <= today){
            //     remove(ref(database, office + '/' + todayString + '/' + val));
            //     console.log(`Reservacion ${val} eliminada de ${office} a las ${data[val].endAt} siendo las ${today.getHours()}:${today.getMinutes()}`);
            // }
        }
    }
}

deleteOffice();

