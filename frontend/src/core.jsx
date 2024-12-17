import { useEffect } from "react";
import { Col, Container, Row } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";

import packInfo from "../package.json";
import DeviceList from "./comp/devs.jsx";
import RepairArea from "./comp/diag.jsx";
import SignInWindow from "./comp/door.jsx";
import BottomNavbar from "./comp/down.jsx";
import FeedList from "./comp/feed.jsx";
import SevereWindow from "./comp/free.jsx";
import HandList from "./comp/hand.jsx";
import Notify from "./comp/note.jsx";
import MainNavbar from "./comp/peak.jsx";
import ProgressList from "./comp/prog.jsx";
import SelectWindow from "./comp/talk.jsx";
import {
  hidePicker,
  hideSignIn,
  makeDevsDict,
  makeFileDict,
  makeJobsDict,
  makeJsonData,
  makeTimeData,
  pullDisconnect,
  pushDisconnect,
  showSignIn,
} from "./features/part.jsx";

function Main() {
  const dispatch = useDispatch();
  const pickerVisual = useSelector((area) => area.area.pickerVisual);
  const signinVisual = useSelector((area) => area.area.signinVisual);
  const notifyVisual = useSelector((area) => area.area.notifyVisual);
  const notifyText = useSelector((area) => area.area.notifyText);
  const disconnected = useSelector((area) => area.area.disconnected);
  const fileDict = useSelector((area) => area.area.fileDict);
  const timeData = useSelector((area) => area.area.timeData);
  const devsPick = useSelector((area) => area.area.devsPick);

  useEffect(() => {
    const intervalId = setInterval(() => {
      try {
        fetch("/read", { method: "GET", credentials: "include" }).then(async (response) => {
          if (response.status === 200) {
            let data = await response.json();
            dispatch(makeJsonData(JSON.stringify(data, null, 2)));
            dispatch(makeFileDict(data.file));
            dispatch(makeTimeData(data.time));
            dispatch(makeDevsDict(data.devs));
            dispatch(makeJobsDict(data.jobs));
            dispatch(pullDisconnect());
            dispatch(hideSignIn());
          } else if (response.status === 401) {
            dispatch(pullDisconnect());
            dispatch(showSignIn());
            dispatch(hidePicker());
          } else {
            dispatch(pushDisconnect());
            dispatch(hideSignIn());
            dispatch(hidePicker());
          }
        });
      } catch (expt) {
        console.error("Exception occurred", expt);
        dispatch(pushDisconnect());
        dispatch(hideSignIn());
        dispatch(hidePicker());
      }
    }, 1000);
    return () => clearInterval(intervalId);
  }, [dispatch]);

  useEffect(() => {
    document.title = `SyncStar v${packInfo.version}`;
  }, []);

  return (
    <>
      <MainNavbar />
      <Container>
        <Row xs={1} md={2} className="g-4">
          <Col>
            <Row xs={1} className="g-4">
              <Col>
                <HandList />
              </Col>
              <Col>
                <DeviceList />
              </Col>
              <Col>
                <ProgressList />
              </Col>
              <Col>
                <RepairArea />
              </Col>
            </Row>
          </Col>
          <Col>
            <FeedList />
          </Col>
        </Row>
      </Container>
      <SelectWindow show={pickerVisual} pick={devsPick} imejlist={fileDict} />
      <SignInWindow show={signinVisual} />
      <SevereWindow show={disconnected} />
      <Notify text={notifyText} show={notifyVisual} />
      <BottomNavbar timedata={timeData} />
    </>
  );
}

export default Main;
