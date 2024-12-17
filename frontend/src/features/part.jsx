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
  fileDict: {},
  timeData: "",
  devsDict: {},
  jobsDict: {},
  jsonData: null,
  devsPick: {
    iden: "",
    data: { iden: 0, name: { handle: "", vendor: "" }, node: "", size: 0 },
  },
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
    makeFileDict: (area, dict) => {
      area.fileDict = dict.payload;
    },
    makeTimeData: (area, time) => {
      area.timeData = time.payload;
    },
    makeDevsDict: (area, devs) => {
      area.devsDict = devs.payload;
    },
    makeJobsDict: (area, jobs) => {
      area.jobsDict = jobs.payload;
    },
    makeJsonData: (area, json) => {
      area.jsonData = json.payload;
    },
    makeDevsPick: (area, pick) => {
      area.devsPick = pick.payload;
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
  makeFileDict,
  makeTimeData,
  makeDevsDict,
  makeJobsDict,
  makeJsonData,
  makeDevsPick,
} = makeunit.actions;

export default makeunit.reducer;
