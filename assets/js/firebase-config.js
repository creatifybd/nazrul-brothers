// Firebase web configuration, NOT privileged service credentials.
// Fill public Firebase Web App config after connecting the dedicated company project.
export const firebaseConfig = {
  apiKey: "",
  authDomain: "",
  projectId: "",
  appId: "",
  measurementId: ""
};
export const firebaseConfigured = Boolean(firebaseConfig.apiKey && firebaseConfig.authDomain && firebaseConfig.projectId && firebaseConfig.appId);
