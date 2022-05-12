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

async function deleteOffice() {
    var today = new Date(Date.now());
    var todayString =  today.toISOString().split('T')[0];

    const snapshotQuito = await dbRef.ref(`quito/${todayString}`).get();
    const dataQuito = snapshotQuito.val();

    const snapshotGuayaquil = await dbRef.ref(`guayaquil/${todayString}`).get();
    const dataGuayaquil = snapshotGuayaquil.val();

    const snapshotLoja = await dbRef.ref(`loja/${todayString}`).get();
    const dataLoja = snapshotLoja.val();
    
    await deleteReservation(dataQuito, todayString, 'quito');

    await deleteReservation(dataGuayaquil, todayString, 'guayaquil');

    await deleteReservation(dataLoja, todayString, 'loja');

    admin.app().delete().then(() => {
        console.log('App deleted successfully');
    });
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
                const del_ref = dbRef.ref(office + '/' + todayString + '/' + val);
                await del_ref.remove()
                console.log(`Reservacion ${val} eliminada de ${office} a las ${data[val].endAt} siendo las ${today.getHours()}:${today.getMinutes()}`);
            }
        }
    }
}
deleteOffice();

