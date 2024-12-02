import { createSlice } from "@reduxjs/toolkit";

const initstet = {
  pickerVisual: false,
  signinVisual: false,
  disconnected: false,
  fileName: "",
  fileIden: "",
  diskIden: "",
  notifyText: "",
  notifyKlas: "",
  notifyVisual: false,
};

export const makeunit = createSlice({
  name: "area",
  initialState: initstet,
  reducers: {
    showPicker: (area) => {
      area.pickerVisual = true;
    },
    hidePicker: (area) => {
      area.pickerVisual = false;
    },
    showSignIn: (area) => {
      area.signinVisual = true;
    },
    hideSignIn: (area) => {
      area.signinVisual = false;
    },
    makeFileName: (area, name) => {
      area.fileName = name.payload;
    },
    makeFileIden: (area, iden) => {
      area.fileIden = iden.payload;
    },
    makeDiskIden: (area, iden) => {
      area.diskIden = iden.payload;
    },
    makeNotifyText: (area, text) => {
      area.notifyText = text.payload;
    },
    makeNotifyKlas: (area, klas) => {
      area.notifyKlas = klas.payload;
    },
    pushDisconnect: (area) => {
      area.disconnected = true;
    },
    pullDisconnect: (area) => {
      area.disconnected = false;
    },
    pushNotification: (area) => {
      area.notifyVisual = true;
    },
    pullNotification: (area) => {
      area.notifyVisual = false;
    },
  },
});

export const {
  showPicker,
  hidePicker,
  showSignIn,
  hideSignIn,
  makeFileName,
  makeFileIden,
  makeDiskIden,
  makeNotifyText,
  makeNotifyKlas,
  pushDisconnect,
  pullDisconnect,
  pushNotification,
  pullNotification,
} = makeunit.actions;

export default makeunit.reducer;
