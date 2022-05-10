
import { initializeApp } from "firebase/app";
import { getDatabase, ref, child, get, remove, goOffline } from "firebase/database";
import 'dotenv/config';

const firebaseConfig = {
  apiKey: process.env.API_KEY,
  authDomain: process.env.AUTH_DOMAIN,
  databaseURL: process.env.DATABASE_URL,
  projectId: process.env.PROJECT_ID,
  storageBucket: process.env.STORAGE,
  messagingSenderId: process.env.MESSAGING,
  appId: process.env.APP_ID,
  measurementId: process.env.MEASURE,
};

initializeApp(firebaseConfig);
var database = getDatabase();

async function deleteOffice() {
    var today = new Date(Date.now());
    var todayString =  today.toISOString().split('T')[0];
    const queryQuito = ref(database);

    const snapshotQuito = await get(child(queryQuito, `quito/${todayString}`));
    const dataQuito = snapshotQuito.val();

    const snapshotGuayaquil = await get(child(queryQuito, `guayaquil/${todayString}`));
    const dataGuayaquil = snapshotGuayaquil.val();

    const snapshotLoja = await get(child(queryQuito, `loja/${todayString}`));
    const dataLoja = snapshotLoja.val();
    
    await deleteReservation(dataQuito, todayString, 'quito');

    await deleteReservation(dataGuayaquil, todayString, 'guayaquil');

    await deleteReservation(dataLoja, todayString, 'loja');

    goOffline(database);
}

async function deleteReservation(data, todayString, office) {
    for (let val in data) {
        if(data[val].endAt){
            const today = new Date(Date.now());
            const day = new Date(`${todayString}T${data[val].endAt}:00`);
            if(today.getTimezoneOffset() === 0){
                day.setHours(day.getHours()+5);
            }
            if(day <= today){
                await remove(ref(database, office + '/' + todayString + '/' + val));
                console.log(`Reservacion ${val} eliminada de ${office} a las ${data[val].endAt} siendo las ${today.getHours()}:${today.getMinutes()}`);
            }
        }
    }
}

function getUTCDate() {
    var now = new Date();
    return new Date(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate(), now.getUTCHours(), now.getUTCMinutes(), now.getUTCSeconds());
}

deleteOffice();

