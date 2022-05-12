import admin from 'firebase-admin';
import 'dotenv/config';

admin.initializeApp({
    credential: admin.credential.cert({
      projectId: process.env.NEXT_PUBLIC_PROJECT_ID,
      clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
      privateKey: process.env.FIREBASE_PRIVATE_KEY,
    }),
    databaseURL: process.env.NEXT_PUBLIC_DATABASE_URL,
  });

const dbRef = admin.database();
let formatter = new Intl.DateTimeFormat('es-ec', { timeZone: "America/Bogota" });   
let todayDateString = getTodayString();

function getTodayString() {
    let today = new Date(Date.now());
    let todayFormat = formatter.format(today).split("/").reverse();
    todayFormat[1] = todayFormat[1].length === 1 ? '0' + todayFormat[1] : todayFormat[1];
    return todayFormat.join("-");
}
async function deleteOffice() {
    console.log(todayDateString);
    console.log(new Date().toLocaleTimeString("es-ec", { timeZone: "America/Bogota" }));

    const snapshotQuito = await dbRef.ref(`quito/${todayDateString}`).get();
    const dataQuito = snapshotQuito.val();

    const snapshotGuayaquil = await dbRef.ref(`guayaquil/${todayDateString}`).get();
    const dataGuayaquil = snapshotGuayaquil.val();

    const snapshotLoja = await dbRef.ref(`loja/${todayDateString}`).get();
    const dataLoja = snapshotLoja.val();
    
    await deleteReservation(dataQuito, todayDateString, 'quito');

    await deleteReservation(dataGuayaquil, todayDateString, 'guayaquil');

    await deleteReservation(dataLoja, todayDateString, 'loja');

    admin.app().delete().then(() => {
        console.log('App deleted successfully');
    });
}

async function deleteReservation(data, todayString, office) {
    for (let val in data) {
        if(data[val].endAt){
            const today = new Date(Date.now());
            const day = new Date(`${todayDateString}T${data[val].endAt}:00`);
            if(today.getTimezoneOffset() === 0){
                day.setHours(day.getHours()+5);
            }
            console.log(day);
            console.log(today);
            if(day <= today){
                const del_ref = dbRef.ref(office + '/' + todayDateString + '/' + val);
                await del_ref.remove()
                console.log(`Reservacion ${val} eliminada de ${office} a las ${data[val].endAt} siendo las ${today.toLocaleTimeString("es-ec", { timeZone: "America/Bogota" })}`);
            }
        }
    }
}
deleteOffice();

