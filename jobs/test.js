import admin from 'firebase-admin';
import 'dotenv/config';
import fs from 'fs';
import {  Blob } from 'buffer';
import { Readable } from 'stream';

admin.initializeApp({
    credential: admin.credential.cert({
      projectId: process.env.NEXT_PUBLIC_PROJECT_ID,
      clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
      privateKey: process.env.FIREBASE_PRIVATE_KEY,
    }),
    databaseURL: process.env.NEXT_PUBLIC_DATABASE_URL,
    storageBucket: process.env.NEXT_PUBLIC_STORAGE_BUCKET
  });

  const storage = admin.storage().bucket();
  const ref = storage.file('test.jpg');
  
  fs.readFile('C:/Users/Alexkt/Downloads/perfil.jpg', function(err, data) {
    if (err) {
        console.log("\n\n Oops!\n An error has occurred\n", err.message);
        throw err;
    }

    console.log(data)

    // fs.writeFile('C:/Users/Alexkt/Downloads/test.jpg', data, function(err) {
    // });

    // console.log("\n\n File read successfully\n");
    
    // const buf2 = Buffer.from(data,'utf8')
    // const buf = Buffer.from(data,'utf-8');
    // const blob = new Blob([data], { type: 'image/jpeg' });
    // console.log(blob)
    // const a = Readable.from([data]);
    // console.log(a.read())
    // save(data)
    // var string = "data:image/jpg;base64," + buf;
    // var regex = /^data:.+\/(.+);base64,(.*)$/;

    // var matches = string.match(regex);
    // var ext = matches[1];
    // var data = matches[2];
    // var buffer = Buffer.from(data, 'base64');
    // const stream = new Stream.PassThrough();
    // Create a pass through stream from a string
    // stream.end(Buffer.from(data));
    // stream.pipe(ref.createWriteStream()).on('finish', () => {
      // The file upload is complete
    // });
    ref.save(data);
  });

  async function  save(data)  {
    const blob = new Blob([data], { type: 'image/jpeg' });
    const buf = await blob.arrayBuffer()
    const a = String.fromCharCode(...new Uint8Array(buf))
    const base64String = Buffer.from(a,'base64');
    fs.writeFile('C:/Users/Alexkt/Downloads/test.jpg', base64String, function(err) {
    });
  }