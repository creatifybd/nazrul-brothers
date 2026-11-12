// Nazrul & Brothers Firebase Web App (public client identifiers; no private credentials).
// Hostinger is the website host; Firebase provides Authentication and Firestore.
export const firebaseConfig = Object.freeze({
  apiKey: "AIzaSyD9v5DLJnas93kMMuEoVpZQU40Uvo_32JY",
  authDomain: "nazrul-and-brothers.firebaseapp.com",
  projectId: "nazrul-and-brothers",
  storageBucket: "nazrul-and-brothers.firebasestorage.app",
  messagingSenderId: "339695277980",
  appId: "1:339695277980:web:6fc9ee2ecf3b8cf5d81a59",
  measurementId: "G-2RLGWXPF2S"
});
export const firebaseConfigured = Boolean(
  firebaseConfig.apiKey &&
  firebaseConfig.authDomain &&
  firebaseConfig.projectId &&
  firebaseConfig.appId
);
