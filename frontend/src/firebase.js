import { initializeApp } from "firebase/app";
import { getDatabase, ref, onValue } from "firebase/database";

// These values come from Firebase Console → Project Settings → General → Web App config
const firebaseProjectId = import.meta.env.VITE_FIREBASE_PROJECT_ID || 'votesaathi-bcf9e';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: `${firebaseProjectId}.firebaseapp.com`,
  // IMPORTANT: RTDB URL uses the Firebase project ID, NOT the GCP project ID
  databaseURL: `https://${firebaseProjectId}-default-rtdb.firebaseio.com`,
  projectId: firebaseProjectId,
  storageBucket: `${firebaseProjectId}.firebasestorage.app`,
  messagingSenderId: import.meta.env.VITE_FIREBASE_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const db = getDatabase(app);

/**
 * Hook-like function to subscribe to realtime updates
 */
export const subscribeToElectionData = (path, callback) => {
  const dataRef = ref(db, path);
  return onValue(dataRef, (snapshot) => {
    const data = snapshot.val();
    callback(data);
  });
};
