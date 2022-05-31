'use strict';
const admin = require('firebase-admin');
require('dotenv/config');

function getTodayString() {
    let formatter = new Intl.DateTimeFormat('es-ec', { timeZone: "America/Bogota" });   
    let today = new Date(Date.now());
    let todayFormat = formatter.format(today).split("/").reverse();
    todayFormat[1] = todayFormat[1].length === 1 ? '0' + todayFormat[1] : todayFormat[1];
    return todayFormat.join("-");
}

async function deleteOffice() {
    admin.initializeApp({
      credential: admin.credential.cert({
        projectId: process.env.NEXT_PUBLIC_PROJECT_ID,
        clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
        privateKey: process.env.FIREBASE_PRIVATE_KEY,
      }),
      databaseURL: process.env.NEXT_PUBLIC_DATABASE_URL,
    });

    const dbRef = admin.database();
    let todayDateString = getTodayString();
    const snapshotQuito = await dbRef.ref(`quito/${todayDateString}`).get();
    const dataQuito = snapshotQuito.val();

    const snapshotGuayaquil = await dbRef.ref(`guayaquil/${todayDateString}`).get();
    const dataGuayaquil = snapshotGuayaquil.val();

    const snapshotLoja = await dbRef.ref(`loja/${todayDateString}`).get();
    const dataLoja = snapshotLoja.val();
    
    await deleteReservation(dataQuito, 'quito');

    await deleteReservation(dataGuayaquil, 'guayaquil');

    await deleteReservation(dataLoja, 'loja');

    admin.app().delete().then(() => {
        console.log('App deleted successfully');
    });
}

async function deleteReservation(data, office) {
    for (let val in data) {
        if(data[val].endAt){
            const today = new Date(Date.now());
            const day = new Date(`${todayDateString}T${data[val].endAt}:00`);
            if(today.getTimezoneOffset() === 0){
                day.setHours(day.getHours()+5);
            }
            if(day <= today){
                const del_ref = dbRef.ref(office + '/' + todayDateString + '/' + val);
                await del_ref.remove()
                console.log(`Reservacion ${val} eliminada de ${office} a las ${data[val].endAt} siendo las ${today.toLocaleTimeString("es-ec", { timeZone: "America/Bogota" })}`);
            }
        }
    }
}



module.exports.delete = async (event)  => {
  
  await deleteOffice();

  return {
    statusCode: 200,
    body: JSON.stringify(
      {
        message: 'Delete successfully!',
        input: event,
      },
      null,
      2
    ),
  };
};
