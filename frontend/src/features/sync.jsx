import { hidePicker, makeNotifyKlas, makeNotifyText, pushDisconnect, pushNotification } from "./part.jsx";

function DemandDiskSync({ dispatch, fileIden, diskIden, disconnected }) {
  dispatch(hidePicker());
  if (disconnected === false) {
    if (fileIden.trim() !== "" && diskIden.trim() !== "") {
      try {
        fetch(`/sync/${diskIden}/${fileIden}`, { method: "POST", credentials: "include" }).then(async (response) => {
          if (response.status === 201) {
            dispatch(makeNotifyText("Task has been successfully scheduled"));
            dispatch(makeNotifyKlas("success"));
          } else {
            let data = await response.text();
            if (response.status === 404 && data.includes(diskIden) === true) {
              dispatch(makeNotifyText("Requested storage device is no longer available"));
            } else if (response.status === 404 && data.includes(fileIden) === true) {
              dispatch(makeNotifyText("Requested images archive is no longer available"));
            } else if (response.status === 400) {
              dispatch(makeNotifyText("Requested storage device cannot be accessed now"));
            } else if (response.status === 422) {
              dispatch(makeNotifyText("Requested image archive exceeds the capacity"));
            }
            dispatch(makeNotifyKlas("warning"));
          }
          dispatch(pushNotification());
        });
      } catch (expt) {
        console.error("Exception occurred", expt);
        dispatch(pushDisconnect());
      }
    } else {
      dispatch(makeNotifyText("Storage devices or images archive were not selected"));
      dispatch(makeNotifyKlas("warning"));
      dispatch(pushNotification());
    }
  }
}

export default DemandDiskSync;
