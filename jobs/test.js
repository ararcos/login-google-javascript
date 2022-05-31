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

const firestore = admin.firestore();
var a = 0;
var b = 0;
var c = 0;
var q = 0;
var g = 0;
var l = 0;
firestore.collection('users').doc('alexander.arcos@ioet.com').onSnapshot(snapshot => {
    // snapshot.docs.forEach(doc => {
    //     console.log("dataa real => ",doc.data())
    // })
    // snapshot.docChanges().forEach(change => {
    //     console.log("type => ",change.type)
    //     if(change.type === 'added'){
    //         console.log("cambio => ",change.doc.data())
    //     }
    //     console.log("nose => ",change.doc.data())
    // });
    // snapshot.forEach(doc => {
    //     c++
    //     if(doc.data().autoSave){
    //         a++
    //     }
    //     if(doc.data().preferredOffice){
    //         b++
    //     }
    //     if(doc.data().preferredOffice === 'quito'){
    //         q++
    //     }
    //     if(doc.data().preferredOffice === 'guayaquil'){
    //         g++
    //     }
    //     if(doc.data().preferredOffice === 'loja'){
    //         l++
    //     }
    // });
    // console.log(a)
    // console.log(b)
    // console.log(c)
    // console.log(q)
    // console.log(g)
    // console.log(l)
    // console.log('total', q+g+l)
    console.log(snapshot.data().admin == true)
})
